#!/usr/bin/env -S uv run python3
"""
Generate HTML statistics dashboard for blog post quality metrics.
Reads from portfolio-assessment.json and generates an interactive dashboard.
"""

import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter
import argparse

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.logging_config import setup_logger

def load_json_file(filename):
    """Load JSON file from docs/reports/ directory."""
    report_path = Path(__file__).parent.parent.parent / "docs" / filename
    with open(report_path) as f:
        return json.load(f)

def load_all_metrics():
    """Load metrics from all data sources."""
    return {
        'portfolio': load_json_file('reports/portfolio-assessment.json'),
        'internal_links': load_json_file('reports/internal-link-metrics.json'),
        'tags': load_json_file('reports/tag-metrics.json'),
        'paragraphs': load_json_file('compliance-report.json')
    }

def get_score_class(score):
    """Return CSS class based on score."""
    if score >= 90:
        return "excellent"
    elif score >= 75:
        return "good"
    elif score >= 60:
        return "warning"
    else:
        return "fail"

def get_distribution_data(data):
    """Extract distribution data for chart."""
    dist = data['score_distribution']
    return [
        dist.get('excellent', 0),
        dist.get('good', 0),
        dist.get('needs_improvement', 0),
        dist.get('failing', 0)
    ]

def calculate_internal_link_metrics(data):
    """Extract internal link metrics for dashboard."""
    dist = data.get('link_distribution', {})
    return {
        'total_links': data.get('total_links', 0),
        'avg_per_post': data.get('avg_links_per_post', 0),
        'in_target': data.get('posts_in_target', 0),
        'total_posts': sum([
            dist.get('0_links', 0),
            dist.get('1_2_links', 0),
            dist.get('3_5_links', 0),
            dist.get('6_10_links', 0),
            dist.get('10plus_links', 0)
        ]),
        'progress': data.get('progress_to_target', '0%'),
        'distribution': [
            dist.get('0_links', 0),
            dist.get('1_2_links', 0),
            dist.get('3_5_links', 0),
            dist.get('6_10_links', 0),
            dist.get('10plus_links', 0)
        ]
    }

def calculate_tag_metrics(data):
    """Extract tag distribution metrics."""
    return {
        'unique_tags': data.get('total_unique_tags', 0),
        'avg_per_post': data.get('avg_tags_per_post', 0),
        'compliance_rate': data.get('compliance_rate', 0),
        'top_tags': data.get('top_10_tags', [])[:5],  # Top 5 for dashboard
        'distribution': [
            data.get('posts_with_0_tags', 0),
            data.get('posts_with_1_2_tags', 0),
            data.get('posts_with_3_5_tags', 0),
            data.get('posts_with_6plus_tags', 0)
        ]
    }

def calculate_paragraph_metrics(data):
    """Extract paragraph structure metrics."""
    total_posts = data.get('total_posts', 0)
    meeting_target = data.get('posts_meeting_80_percent', 0)
    avg_compliance = data.get('avg_paragraph_compliance', 0)

    # Calculate distribution buckets
    distribution = [0, 0, 0]  # 0-59%, 60-79%, 80-100%
    for post in data.get('posts', []):
        compliance = post.get('paragraphs', {}).get('compliance_rate', 0)
        if compliance >= 80:
            distribution[2] += 1
        elif compliance >= 60:
            distribution[1] += 1
        else:
            distribution[0] += 1

    return {
        'avg_compliance': avg_compliance,
        'posts_meeting_target': meeting_target,
        'total_posts': total_posts,
        'distribution': distribution
    }

def get_top_posts(data, limit=10):
    """Get top performing posts."""
    all_results = data.get('all_results', [])
    # Sort by score descending
    sorted_results = sorted(all_results, key=lambda x: x['score'], reverse=True)
    return sorted_results[:limit]

def get_bottom_posts(data, limit=10):
    """Get lowest performing posts."""
    all_results = data.get('all_results', [])
    # Sort by score ascending
    sorted_results = sorted(all_results, key=lambda x: x['score'])
    return sorted_results[:limit]

def extract_post_title(post_path):
    """Extract readable title from post path."""
    filename = Path(post_path).stem
    # Remove date prefix (YYYY-MM-DD-)
    title = filename[11:] if len(filename) > 10 else filename
    # Replace hyphens with spaces and title case
    return title.replace('-', ' ').title()

def get_common_violations(data):
    """Analyze most common violations across all posts."""
    violation_counter = Counter()
    all_results = data.get('all_results', [])

    for result in all_results:
        for violation in result.get('violations', []):
            violation_type = violation.get('type', 'unknown')
            violation_counter[violation_type] += 1

    return violation_counter.most_common(5)

def generate_top_posts_rows(posts):
    """Generate HTML table rows for top posts."""
    rows = []
    for i, post in enumerate(posts, 1):
        score = post.get('score', 0)
        path = post.get('post_path', post.get('post', ''))
        title = extract_post_title(path)
        score_class = get_score_class(score)

        rows.append(f"""
                    <tr>
                        <td>{i}</td>
                        <td>{title}</td>
                        <td class="score-{score_class}">{score}</td>
                        <td><span class="badge badge-{score_class}">{'Excellent' if score >= 90 else 'Good'}</span></td>
                    </tr>""")

    return ''.join(rows)

def generate_bottom_posts_rows(posts):
    """Generate HTML table rows for bottom posts."""
    rows = []
    for i, post in enumerate(posts, 1):
        score = post.get('score', 0)
        path = post.get('post_path', post.get('post', ''))
        title = extract_post_title(path)
        score_class = get_score_class(score)

        # Get top 2 violations
        violations = post.get('violations', [])
        key_issues = ', '.join([v.get('type', 'unknown').replace('_', ' ').title()
                               for v in violations[:2]])
        if not key_issues:
            key_issues = 'None'

        rows.append(f"""
                    <tr>
                        <td>{i}</td>
                        <td>{title}</td>
                        <td class="score-{score_class}">{score}</td>
                        <td>{key_issues}</td>
                    </tr>""")

    return ''.join(rows)

def generate_violations_section(data):
    """Generate common violations section."""
    violations = get_common_violations(data)
    if not violations:
        return "<p>No violations found across all posts.</p>"

    items = []
    for violation_type, count in violations:
        readable_name = violation_type.replace('_', ' ').title()
        items.append(f"""
            <div class="violation-item">
                <span class="violation-name">{readable_name}</span>
                <span class="violation-count">{count} occurrences</span>
            </div>""")

    return ''.join(items)

def generate_html_dashboard(all_data):
    """Generate HTML dashboard from all metrics data."""

    # Extract individual datasets
    portfolio_data = all_data['portfolio']
    link_data = all_data['internal_links']
    tag_data = all_data['tags']
    paragraph_data = all_data['paragraphs']

    # Calculate portfolio metrics
    total = portfolio_data.get('total_posts', 0)
    dist = portfolio_data.get('score_distribution', {})
    passing = dist.get('excellent', 0) + dist.get('good', 0)
    passing_rate = (passing / total * 100) if total > 0 else 0

    # Get top and bottom posts
    top_posts = get_top_posts(portfolio_data, 10)
    bottom_posts = get_bottom_posts(portfolio_data, 10)

    # Calculate new metrics
    link_metrics = calculate_internal_link_metrics(link_data)
    tag_metrics = calculate_tag_metrics(tag_data)
    paragraph_metrics = calculate_paragraph_metrics(paragraph_data)

    # Generate timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog Quality Dashboard - William Zujkowski</title>
    <meta name="description" content="Quality metrics and statistics for blog posts">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #1f2937;
            background: #f3f4f6;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        h1 {{
            font-size: 2.5em;
            font-weight: 700;
            color: #111827;
            margin-bottom: 10px;
        }}

        .subtitle {{
            color: #6b7280;
            font-size: 1em;
        }}

        .card {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        .card h2 {{
            font-size: 1.5em;
            font-weight: 600;
            color: #111827;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e5e7eb;
        }}

        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .metric {{
            text-align: center;
            padding: 20px;
            background: #f9fafb;
            border-radius: 8px;
        }}

        .metric-value {{
            font-size: 2.5em;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 8px;
        }}

        .metric-label {{
            font-size: 0.875em;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .score-excellent {{ color: #10b981; }}
        .score-good {{ color: #3b82f6; }}
        .score-warning {{ color: #f59e0b; }}
        .score-fail {{ color: #ef4444; }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}

        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }}

        th {{
            background: #f9fafb;
            font-weight: 600;
            color: #374151;
            text-transform: uppercase;
            font-size: 0.75em;
            letter-spacing: 0.5px;
        }}

        tr:hover {{
            background: #f9fafb;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.875em;
            font-weight: 500;
        }}

        .badge-excellent {{
            background: #d1fae5;
            color: #065f46;
        }}

        .badge-good {{
            background: #dbeafe;
            color: #1e40af;
        }}

        .badge-warning {{
            background: #fef3c7;
            color: #92400e;
        }}

        .badge-fail {{
            background: #fee2e2;
            color: #991b1b;
        }}

        .chart {{
            height: 300px;
            margin: 20px 0;
        }}

        .violation-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            margin: 8px 0;
            background: #f9fafb;
            border-radius: 6px;
        }}

        .violation-name {{
            font-weight: 500;
            color: #374151;
        }}

        .violation-count {{
            color: #6b7280;
            font-size: 0.875em;
        }}

        .back-link {{
            display: inline-block;
            margin-top: 20px;
            color: #3b82f6;
            text-decoration: none;
            font-weight: 500;
        }}

        .back-link:hover {{
            color: #2563eb;
            text-decoration: underline;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}

            h1 {{
                font-size: 1.75em;
            }}

            .card {{
                padding: 20px;
            }}

            .metrics {{
                grid-template-columns: 1fr;
            }}

            table {{
                font-size: 0.875em;
            }}

            th, td {{
                padding: 8px;
            }}
        }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Blog Quality Dashboard</h1>
            <p class="subtitle">Last updated: {timestamp}</p>
            <a href="/" class="back-link">← Back to Home</a>
        </header>

        <!-- Portfolio Overview -->
        <div class="card">
            <h2>Portfolio Overview</h2>
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value score-{get_score_class(portfolio_data['average_score'])}">{portfolio_data['average_score']:.1f}</div>
                    <div class="metric-label">Average Score</div>
                </div>
                <div class="metric">
                    <div class="metric-value score-{get_score_class(passing_rate)}">{passing_rate:.1f}%</div>
                    <div class="metric-label">Passing Rate (≥75)</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{portfolio_data['total_posts']}</div>
                    <div class="metric-label">Total Posts</div>
                </div>
            </div>
        </div>

        <!-- Internal Links Card -->
        <div class="card">
            <h2>🔗 Internal Linking Strategy</h2>
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value">{link_metrics['avg_per_post']:.2f}</div>
                    <div class="metric-label">Avg Links/Post (Target: 6-10)</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{link_metrics['in_target']}/{link_metrics['total_posts']}</div>
                    <div class="metric-label">Posts Meeting Target</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{link_metrics['progress']}</div>
                    <div class="metric-label">Progress to Goal</div>
                </div>
            </div>
            <canvas id="linkDistributionChart" class="chart"></canvas>
        </div>

        <!-- Tag Distribution Card -->
        <div class="card">
            <h2>🏷️ Tag Strategy</h2>
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value">{tag_metrics['unique_tags']}</div>
                    <div class="metric-label">Canonical Tags</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{tag_metrics['compliance_rate']:.1f}%</div>
                    <div class="metric-label">3-5 Tags Compliance</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{tag_metrics['avg_per_post']:.1f}</div>
                    <div class="metric-label">Avg Tags/Post</div>
                </div>
            </div>
            <canvas id="tagDistributionChart" class="chart"></canvas>
            <div style="margin-top: 20px;">
                <h3 style="font-size: 1.1em; margin-bottom: 10px;">Top 5 Tags</h3>
                <div style="display: grid; gap: 8px;">
                    {''.join([f'<div class="violation-item"><span class="violation-name">{tag["tag"]}</span><span class="violation-count">{tag["count"]} posts</span></div>' for tag in tag_metrics['top_tags']])}
                </div>
            </div>
        </div>

        <!-- Paragraph Structure Card -->
        <div class="card">
            <h2>📝 Paragraph Structure</h2>
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value">{paragraph_metrics['avg_compliance']:.1f}%</div>
                    <div class="metric-label">Avg Compliance</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{paragraph_metrics['posts_meeting_target']}/{paragraph_metrics['total_posts']}</div>
                    <div class="metric-label">Meeting 80%+ Target</div>
                </div>
            </div>
            <canvas id="paragraphComplianceChart" class="chart"></canvas>
        </div>

        <!-- Score Distribution Chart -->
        <div class="card">
            <h2>Score Distribution</h2>
            <canvas id="distributionChart" class="chart"></canvas>
        </div>

        <!-- Common Violations -->
        <div class="card">
            <h2>Most Common Issues</h2>
            {generate_violations_section(portfolio_data)}
        </div>

        <!-- Top 10 Posts -->
        <div class="card">
            <h2>🏆 Top 10 Posts (Excellent Performance)</h2>
            <table>
                <thead>
                    <tr>
                        <th style="width: 60px;">Rank</th>
                        <th>Post Title</th>
                        <th style="width: 80px;">Score</th>
                        <th style="width: 120px;">Status</th>
                    </tr>
                </thead>
                <tbody>
{generate_top_posts_rows(top_posts)}
                </tbody>
            </table>
        </div>

        <!-- Bottom 10 Posts -->
        <div class="card">
            <h2>⚠️ Posts Needing Attention</h2>
            <table>
                <thead>
                    <tr>
                        <th style="width: 60px;">Rank</th>
                        <th>Post Title</th>
                        <th style="width: 80px;">Score</th>
                        <th>Key Issues</th>
                    </tr>
                </thead>
                <tbody>
{generate_bottom_posts_rows(bottom_posts)}
                </tbody>
            </table>
        </div>

        <div class="card">
            <h2>About This Dashboard</h2>
            <p style="color: #6b7280;">
                This dashboard tracks blog post quality metrics based on automated validation.
                Scores range from 0-100, with posts scoring ≥75 considered passing.
                The scoring system evaluates authenticity, readability, and adherence to style guidelines.
            </p>
        </div>
    </div>

    <script>
        // Chart.js implementation for score distribution
        const ctxDist = document.getElementById('distributionChart');
        const distributionData = {json.dumps(get_distribution_data(portfolio_data))};

        new Chart(ctxDist, {{
            type: 'bar',
            data: {{
                labels: ['Excellent (90-100)', 'Good (75-89)', 'Needs Improvement (60-74)', 'Failing (<60)'],
                datasets: [{{
                    label: 'Number of Posts',
                    data: distributionData,
                    backgroundColor: [
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(59, 130, 246, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(239, 68, 68, 0.8)'
                    ],
                    borderColor: [
                        'rgb(16, 185, 129)',
                        'rgb(59, 130, 246)',
                        'rgb(245, 158, 11)',
                        'rgb(239, 68, 68)'
                    ],
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    title: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 5
                        }}
                    }}
                }}
            }}
        }});

        // Link distribution chart
        const ctxLink = document.getElementById('linkDistributionChart');
        const linkDistData = {json.dumps(link_metrics['distribution'])};

        new Chart(ctxLink, {{
            type: 'bar',
            data: {{
                labels: ['0 links', '1-2 links', '3-5 links', '6-10 links (Target)', '10+ links'],
                datasets: [{{
                    label: 'Number of Posts',
                    data: linkDistData,
                    backgroundColor: [
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(59, 130, 246, 0.8)'
                    ],
                    borderColor: [
                        'rgb(239, 68, 68)',
                        'rgb(245, 158, 11)',
                        'rgb(245, 158, 11)',
                        'rgb(16, 185, 129)',
                        'rgb(59, 130, 246)'
                    ],
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    title: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 5
                        }}
                    }}
                }}
            }}
        }});

        // Tag distribution pie chart
        const ctxTag = document.getElementById('tagDistributionChart');
        const tagDistData = {json.dumps(tag_metrics['distribution'])};

        new Chart(ctxTag, {{
            type: 'pie',
            data: {{
                labels: ['0 tags', '1-2 tags', '3-5 tags (Target)', '6+ tags'],
                datasets: [{{
                    label: 'Posts',
                    data: tagDistData,
                    backgroundColor: [
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(59, 130, 246, 0.8)'
                    ],
                    borderColor: [
                        'rgb(239, 68, 68)',
                        'rgb(245, 158, 11)',
                        'rgb(16, 185, 129)',
                        'rgb(59, 130, 246)'
                    ],
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }},
                    title: {{
                        display: false
                    }}
                }}
            }}
        }});

        // Paragraph compliance chart
        const ctxPara = document.getElementById('paragraphComplianceChart');
        const paraDistData = {json.dumps(paragraph_metrics['distribution'])};

        new Chart(ctxPara, {{
            type: 'bar',
            data: {{
                labels: ['0-59% (Failing)', '60-79% (Needs Work)', '80-100% (Target)'],
                datasets: [{{
                    label: 'Number of Posts',
                    data: paraDistData,
                    backgroundColor: [
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(16, 185, 129, 0.8)'
                    ],
                    borderColor: [
                        'rgb(239, 68, 68)',
                        'rgb(245, 158, 11)',
                        'rgb(16, 185, 129)'
                    ],
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    title: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 5
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""

    return html

def save_dashboard(html, logger=None):
    """Save dashboard to _site/ directory."""
    output_path = Path(__file__).parent.parent.parent / "_site/stats.html"
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(html)
    if logger:
        logger.info(f"✅ Dashboard saved to {output_path}")
        logger.info(f"📊 Dashboard will be accessible at: /stats.html")

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Generate blog quality dashboard with optimization metrics')
    parser.add_argument('--version', action='version', version='%(prog)s 2.0.0')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable debug output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress info messages')
    parser.add_argument('--log-file', type=Path, help='Write logs to file')

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(__name__, level=level, log_file=args.log_file, quiet=args.quiet)

    try:
        logger.info("📊 Generating blog quality dashboard v2.0.0...")
        logger.info("Loading metrics from 4 data sources...")
        all_data = load_all_metrics()
        logger.info("✅ Loaded: portfolio, internal-links, tags, paragraph-compliance")
        html = generate_html_dashboard(all_data)
        save_dashboard(html, logger)
        logger.info("✅ Dashboard generation complete with blog optimization metrics!")
    except Exception as e:
        logger.error(f"❌ Error generating dashboard: {e}")
        raise

if __name__ == "__main__":
    main()
