#!/usr/bin/env -S uv run python3
"""
SCRIPT: token-usage-monitor.py
PURPOSE: Monitor and analyze token usage across operations
CATEGORY: optimization
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-11-01

DESCRIPTION:
    Real-time token usage monitoring and optimization recommendations.
    Tracks token consumption across different operation types and identifies
    optimization opportunities.

USAGE:
    # Start monitoring session
    uv run python3 scripts/utilities/token-usage-monitor.py --start-session blog-post-1

    # Log operation
    uv run python3 scripts/utilities/token-usage-monitor.py --log "read MANIFEST.json" --tokens 2500

    # End session and generate report
    uv run python3 scripts/utilities/token-usage-monitor.py --end-session blog-post-1

    # Analyze historical usage
    uv run python3 scripts/utilities/token-usage-monitor.py --analyze

    # Get optimization recommendations
    uv run python3 scripts/utilities/token-usage-monitor.py --recommend

MANIFEST_REGISTRY: scripts/utilities/token-usage-monitor.py
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict


@dataclass
class TokenUsage:
    """Token usage record"""
    timestamp: str
    operation: str
    tokens: int
    category: str
    session_id: Optional[str] = None
    metadata: Optional[Dict] = None


@dataclass
class Session:
    """Monitoring session"""
    session_id: str
    started: str
    ended: Optional[str]
    operations: List[TokenUsage]
    total_tokens: int


class TokenUsageMonitor:
    """Track and analyze token usage"""

    def __init__(self, data_dir: Path = Path("docs/metrics/token-usage")):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.sessions_file = self.data_dir / "sessions.json"
        self.usage_log = self.data_dir / "usage-log.jsonl"

        # Operation categories for analysis
        self.categories = {
            'manifest': ['manifest', 'MANIFEST', 'registry'],
            'context': ['CLAUDE.md', 'context', 'module', 'INDEX'],
            'blog': ['blog', 'post', 'article', 'writing'],
            'scripts': ['script', 'python', '.py'],
            'validation': ['validate', 'check', 'verify'],
            'git': ['git', 'commit', 'push'],
            'docs': ['docs', 'documentation', '.md']
        }

    def categorize_operation(self, operation: str) -> str:
        """Categorize an operation based on keywords"""
        operation_lower = operation.lower()

        for category, keywords in self.categories.items():
            if any(kw in operation_lower for kw in keywords):
                return category

        return 'other'

    def start_session(self, session_id: str) -> Session:
        """Start a new monitoring session"""
        session = Session(
            session_id=session_id,
            started=datetime.now().isoformat(),
            ended=None,
            operations=[],
            total_tokens=0
        )

        self._save_session(session)
        print(f"✓ Started session: {session_id}")
        return session

    def log_usage(self, operation: str, tokens: int, session_id: Optional[str] = None,
                  metadata: Optional[Dict] = None) -> TokenUsage:
        """Log token usage for an operation"""

        category = self.categorize_operation(operation)

        usage = TokenUsage(
            timestamp=datetime.now().isoformat(),
            operation=operation,
            tokens=tokens,
            category=category,
            session_id=session_id,
            metadata=metadata or {}
        )

        # Append to usage log
        with open(self.usage_log, 'a') as f:
            f.write(json.dumps(asdict(usage)) + '\n')

        # Update session if provided
        if session_id:
            session = self._load_session(session_id)
            if session:
                session.operations.append(usage)
                session.total_tokens += tokens
                self._save_session(session)

        print(f"✓ Logged: {operation} ({tokens:,} tokens, category: {category})")
        return usage

    def end_session(self, session_id: str) -> Session:
        """End a monitoring session and generate report"""
        session = self._load_session(session_id)

        if not session:
            raise ValueError(f"Session not found: {session_id}")

        session.ended = datetime.now().isoformat()
        self._save_session(session)

        # Generate session report
        report = self._generate_session_report(session)
        report_file = self.data_dir / f"session-{session_id}.md"

        with open(report_file, 'w') as f:
            f.write(report)

        print(f"✓ Ended session: {session_id}")
        print(f"  Total tokens: {session.total_tokens:,}")
        print(f"  Operations: {len(session.operations)}")
        print(f"  Report: {report_file}")

        return session

    def analyze_usage(self, days: int = 30) -> Dict:
        """Analyze historical token usage"""

        all_usage = self._load_all_usage()

        if not all_usage:
            return {
                'total_operations': 0,
                'total_tokens': 0,
                'message': 'No usage data available'
            }

        # Basic statistics
        total_tokens = sum(u.tokens for u in all_usage)
        total_operations = len(all_usage)

        # By category
        by_category = defaultdict(lambda: {'count': 0, 'tokens': 0})
        for usage in all_usage:
            by_category[usage.category]['count'] += 1
            by_category[usage.category]['tokens'] += usage.tokens

        # Top operations
        operation_tokens = defaultdict(int)
        for usage in all_usage:
            operation_tokens[usage.operation] += usage.tokens

        top_operations = sorted(
            operation_tokens.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        # Average tokens per operation
        avg_tokens = total_tokens / total_operations if total_operations > 0 else 0

        return {
            'total_operations': total_operations,
            'total_tokens': total_tokens,
            'average_tokens': avg_tokens,
            'by_category': dict(by_category),
            'top_operations': top_operations
        }

    def generate_recommendations(self) -> List[str]:
        """Generate optimization recommendations based on usage patterns"""

        analysis = self.analyze_usage()

        if analysis.get('total_operations', 0) == 0:
            return ["No usage data available for recommendations"]

        recommendations = []

        # Check manifest usage
        manifest_usage = analysis['by_category'].get('manifest', {})
        if manifest_usage.get('tokens', 0) > 5000:
            recommendations.append(
                f"🔴 HIGH: Manifest operations using {manifest_usage['tokens']:,} tokens. "
                "Consider implementing optimized MANIFEST.json structure (83% reduction)"
            )

        # Check context loading
        context_usage = analysis['by_category'].get('context', {})
        if context_usage.get('tokens', 0) > 10000:
            recommendations.append(
                f"🟡 MEDIUM: Context loading using {context_usage['tokens']:,} tokens. "
                "Consider implementing progressive context loading"
            )

        # Check documentation reads
        docs_usage = analysis['by_category'].get('docs', {})
        if docs_usage.get('count', 0) > 20:
            recommendations.append(
                f"🟡 MEDIUM: {docs_usage['count']} documentation reads. "
                "Consider caching frequently accessed docs"
            )

        # Check average operation cost
        avg_tokens = analysis.get('average_tokens', 0)
        if avg_tokens > 3000:
            recommendations.append(
                f"🟡 MEDIUM: Average operation uses {avg_tokens:,.0f} tokens. "
                "Target should be <1500 tokens per operation"
            )

        # Check for repeated operations
        top_ops = analysis.get('top_operations', [])
        if top_ops and top_ops[0][1] > 10000:
            recommendations.append(
                f"🔴 HIGH: '{top_ops[0][0]}' executed frequently ({top_ops[0][1]:,} total tokens). "
                "Consider optimization or caching"
            )

        if not recommendations:
            recommendations.append(
                "✓ Token usage looks optimal. Continue monitoring for trends."
            )

        return recommendations

    def _save_session(self, session: Session):
        """Save session to file"""
        sessions = self._load_sessions()
        sessions[session.session_id] = asdict(session)

        with open(self.sessions_file, 'w') as f:
            json.dump(sessions, f, indent=2)

    def _load_session(self, session_id: str) -> Optional[Session]:
        """Load session from file"""
        sessions = self._load_sessions()

        if session_id not in sessions:
            return None

        data = sessions[session_id]
        return Session(
            session_id=data['session_id'],
            started=data['started'],
            ended=data.get('ended'),
            operations=[TokenUsage(**op) for op in data['operations']],
            total_tokens=data['total_tokens']
        )

    def _load_sessions(self) -> Dict:
        """Load all sessions"""
        if not self.sessions_file.exists():
            return {}

        with open(self.sessions_file, 'r') as f:
            return json.load(f)

    def _load_all_usage(self) -> List[TokenUsage]:
        """Load all usage records"""
        if not self.usage_log.exists():
            return []

        usage_records = []
        with open(self.usage_log, 'r') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    usage_records.append(TokenUsage(**data))

        return usage_records

    def _generate_session_report(self, session: Session) -> str:
        """Generate detailed session report"""

        # Calculate statistics
        by_category = defaultdict(lambda: {'count': 0, 'tokens': 0})
        for op in session.operations:
            by_category[op.category]['count'] += 1
            by_category[op.category]['tokens'] += op.tokens

        # Sort by tokens
        sorted_categories = sorted(
            by_category.items(),
            key=lambda x: x[1]['tokens'],
            reverse=True
        )

        # Generate report
        report = f"""# Token Usage Report: {session.session_id}

**Started**: {session.started}
**Ended**: {session.ended or 'In progress'}
**Total tokens**: {session.total_tokens:,}
**Operations**: {len(session.operations)}

## Breakdown by Category

"""

        for category, stats in sorted_categories:
            pct = (stats['tokens'] / session.total_tokens * 100) if session.total_tokens > 0 else 0
            report += f"- **{category}**: {stats['tokens']:,} tokens ({pct:.1f}%) - {stats['count']} operations\n"

        report += "\n## Operation Timeline\n\n"

        for i, op in enumerate(session.operations, 1):
            report += f"{i}. [{op.category}] {op.operation} - {op.tokens:,} tokens\n"

        report += "\n## Optimization Opportunities\n\n"

        # Session-specific recommendations
        if by_category['manifest']['tokens'] > 2000:
            report += "- 🔴 Manifest operations are heavy. Consider optimized structure.\n"

        if by_category['context']['tokens'] > 8000:
            report += "- 🟡 Context loading is extensive. Consider progressive loading.\n"

        if len(session.operations) > 20:
            report += f"- 🟡 Many operations ({len(session.operations)}). Consider batching.\n"

        avg_tokens = session.total_tokens / len(session.operations) if session.operations else 0
        report += f"\n**Average tokens per operation**: {avg_tokens:,.0f}\n"
        report += f"**Target**: <1500 tokens per operation\n"

        return report


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Monitor token usage'
    )
    parser.add_argument(
        '--start-session',
        metavar='SESSION_ID',
        help='Start new monitoring session'
    )
    parser.add_argument(
        '--end-session',
        metavar='SESSION_ID',
        help='End monitoring session'
    )
    parser.add_argument(
        '--log',
        metavar='OPERATION',
        help='Log operation'
    )
    parser.add_argument(
        '--tokens',
        type=int,
        help='Token count for operation'
    )
    parser.add_argument(
        '--session',
        metavar='SESSION_ID',
        help='Session ID for operation logging'
    )
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Analyze historical usage'
    )
    parser.add_argument(
        '--recommend',
        action='store_true',
        help='Generate optimization recommendations'
    )

    args = parser.parse_args()

    monitor = TokenUsageMonitor()

    if args.start_session:
        monitor.start_session(args.start_session)

    elif args.end_session:
        monitor.end_session(args.end_session)

    elif args.log and args.tokens:
        monitor.log_usage(args.log, args.tokens, args.session)

    elif args.analyze:
        analysis = monitor.analyze_usage()
        print("\n=== TOKEN USAGE ANALYSIS ===\n")
        print(f"Total operations: {analysis['total_operations']:,}")
        print(f"Total tokens: {analysis['total_tokens']:,}")
        print(f"Average per operation: {analysis.get('average_tokens', 0):,.0f}")
        print("\nBy category:")

        for category, stats in sorted(
            analysis['by_category'].items(),
            key=lambda x: x[1]['tokens'],
            reverse=True
        ):
            print(f"  {category}: {stats['tokens']:,} tokens ({stats['count']} ops)")

        print("\nTop operations:")
        for op, tokens in analysis.get('top_operations', [])[:5]:
            print(f"  {op}: {tokens:,} tokens")

    elif args.recommend:
        recommendations = monitor.generate_recommendations()
        print("\n=== OPTIMIZATION RECOMMENDATIONS ===\n")
        for rec in recommendations:
            print(f"{rec}\n")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
