#!/usr/bin/env python3
"""Analyze blog post coverage to identify weeks without posts."""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from lib.logging_config import setup_logger

logger = setup_logger(__name__)

def extract_dates_from_posts():
    """Extract dates from blog post filenames."""
    posts_dir = Path("src/posts")
    dates = []

    for post_file in posts_dir.glob("*.md"):
        filename = post_file.name
        # Skip welcome post and other non-date posts
        if not filename[:4].isdigit():
            continue

        # Extract date from filename (YYYY-MM-DD format)
        try:
            date_str = "-".join(filename.split("-")[:3])
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            dates.append(date_obj)
        except ValueError:
            continue

    return sorted(dates)

def get_week_number(date):
    """Get week number (Monday as start of week)."""
    return date.isocalendar()[1]

def get_year_week(date):
    """Get year and week tuple."""
    iso = date.isocalendar()
    return (iso[0], iso[1])

def analyze_weekly_coverage(dates):
    """Analyze which weeks have blog posts."""
    if not dates:
        return {}, []

    # Group posts by year-week
    posts_by_week = defaultdict(list)
    for date in dates:
        year_week = get_year_week(date)
        posts_by_week[year_week].append(date)

    # Find the range of dates we need to cover
    start_date = min(dates)
    end_date = max(dates)

    # Generate all weeks in the range
    missing_weeks = []
    current_date = start_date - timedelta(days=start_date.weekday())  # Start from Monday

    while current_date <= end_date:
        year_week = get_year_week(current_date)
        if year_week not in posts_by_week:
            # This week has no posts
            week_start = current_date
            week_end = current_date + timedelta(days=6)
            missing_weeks.append({
                'year': year_week[0],
                'week': year_week[1],
                'start': week_start,
                'end': week_end
            })
        current_date += timedelta(days=7)

    return posts_by_week, missing_weeks

def main():
    """Main analysis function."""
    dates = extract_dates_from_posts()

    logger.info(f"Total blog posts found: {len(dates)}")
    logger.info(f"Date range: {min(dates).strftime('%Y-%m-%d')} to {max(dates).strftime('%Y-%m-%d')}")
    logger.info("")

    posts_by_week, missing_weeks = analyze_weekly_coverage(dates)

    logger.info(f"Weeks with posts: {len(posts_by_week)}")
    logger.info(f"Weeks missing posts: {len(missing_weeks)}")
    logger.info("")

    # Show recent missing weeks (last 3 months)
    three_months_ago = datetime.now() - timedelta(days=90)
    recent_missing = [w for w in missing_weeks if w['start'] >= three_months_ago and w['start'] <= datetime.now()]

    if recent_missing:
        logger.info(f"Recent weeks missing posts (last 3 months): {len(recent_missing)}")
        for week in recent_missing:
            logger.info(f"  - Week {week['week']}, {week['year']}: {week['start'].strftime('%Y-%m-%d')} to {week['end'].strftime('%Y-%m-%d')}")
    else:
        logger.info("All recent weeks have posts!")

    logger.info("")

    # Show upcoming weeks that need posts
    today = datetime.now()
    upcoming_weeks = []
    current = today - timedelta(days=today.weekday())  # Start of current week

    for i in range(8):  # Check next 8 weeks
        year_week = get_year_week(current)
        if year_week not in posts_by_week:
            week_start = current
            week_end = current + timedelta(days=6)
            upcoming_weeks.append({
                'year': year_week[0],
                'week': year_week[1],
                'start': week_start,
                'end': week_end
            })
        current += timedelta(days=7)

    if upcoming_weeks:
        logger.info(f"Upcoming weeks needing posts: {len(upcoming_weeks)}")
        for week in upcoming_weeks:
            logger.info(f"  - Week {week['week']}, {week['year']}: {week['start'].strftime('%Y-%m-%d')} to {week['end'].strftime('%Y-%m-%d')}")

    # Summary statistics
    logger.info("")
    logger.info("Summary Statistics:")
    total_weeks = len(posts_by_week) + len(missing_weeks)
    coverage_percent = (len(posts_by_week) / total_weeks) * 100 if total_weeks > 0 else 0
    logger.info(f"  Coverage: {coverage_percent:.1f}% ({len(posts_by_week)}/{total_weeks} weeks)")

    # Weeks with multiple posts
    multi_post_weeks = {k: v for k, v in posts_by_week.items() if len(v) > 1}
    if multi_post_weeks:
        logger.info(f"  Weeks with multiple posts: {len(multi_post_weeks)}")

if __name__ == "__main__":
    main()