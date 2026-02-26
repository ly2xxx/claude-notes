#!/usr/bin/env python3
"""
GitLab Pipeline Status Checker

Fetches and summarizes GitLab pipeline status from gitlab.com or self-hosted instances.
"""

import argparse
import sys
import io
import requests
from datetime import datetime
from typing import Optional, Dict, Any

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def format_duration(seconds: Optional[int]) -> str:
    """Format duration in seconds to human-readable format."""
    if seconds is None:
        return "N/A"
    
    minutes, secs = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def get_status_emoji(status: str) -> str:
    """Get emoji representation for pipeline status."""
    status_map = {
        "success": "✅",
        "failed": "❌",
        "running": "🔄",
        "pending": "⏳",
        "canceled": "🚫",
        "skipped": "⏭️",
        "manual": "🤚",
        "created": "🆕"
    }
    return status_map.get(status, "❓")


def get_verdict(status: str, failed_jobs: int = 0) -> str:
    """Generate a simple verdict based on pipeline status."""
    if status == "success":
        return "✅ PASS - All jobs completed successfully"
    elif status == "failed":
        return f"❌ FAIL - Pipeline failed ({failed_jobs} job(s) failed)"
    elif status == "running":
        return "🔄 IN PROGRESS - Pipeline is currently running"
    elif status == "pending":
        return "⏳ PENDING - Pipeline is waiting to start"
    elif status == "canceled":
        return "🚫 CANCELED - Pipeline was canceled"
    elif status == "skipped":
        return "⏭️ SKIPPED - Pipeline was skipped"
    else:
        return f"❓ UNKNOWN - Status: {status}"


def fetch_pipeline(gitlab_url: str, project_id: str, pipeline_id: Optional[str], token: Optional[str]) -> Dict[str, Any]:
    """Fetch pipeline data from GitLab API."""
    base_url = f"{gitlab_url}/api/v4"
    headers = {}
    
    if token:
        headers["PRIVATE-TOKEN"] = token
    
    # If no pipeline_id specified, get the latest pipeline
    if not pipeline_id:
        url = f"{base_url}/projects/{project_id}/pipelines?per_page=1"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        pipelines = response.json()
        
        if not pipelines:
            raise ValueError("No pipelines found for this project")
        
        pipeline_id = pipelines[0]["id"]
    
    # Fetch pipeline details
    url = f"{base_url}/projects/{project_id}/pipelines/{pipeline_id}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    pipeline = response.json()
    
    # Fetch pipeline jobs
    jobs_url = f"{base_url}/projects/{project_id}/pipelines/{pipeline_id}/jobs"
    jobs_response = requests.get(jobs_url, headers=headers)
    jobs_response.raise_for_status()
    jobs = jobs_response.json()
    
    return {"pipeline": pipeline, "jobs": jobs}


def summarize_pipeline(data: Dict[str, Any]) -> str:
    """Generate a summary of the pipeline status."""
    pipeline = data["pipeline"]
    jobs = data["jobs"]
    
    # Extract key info
    pipeline_id = pipeline["id"]
    status = pipeline["status"]
    ref = pipeline.get("ref", "N/A")
    created_at = pipeline.get("created_at", "N/A")
    duration = pipeline.get("duration")
    web_url = pipeline.get("web_url", "N/A")
    
    # Count job statuses
    job_statuses = {}
    failed_jobs = []
    
    for job in jobs:
        job_status = job["status"]
        job_statuses[job_status] = job_statuses.get(job_status, 0) + 1
        
        if job_status == "failed":
            failed_jobs.append({
                "name": job["name"],
                "stage": job["stage"]
            })
    
    # Build summary
    summary = []
    summary.append("=" * 60)
    summary.append("🔍 GITLAB PIPELINE STATUS SUMMARY")
    summary.append("=" * 60)
    summary.append("")
    summary.append(f"Pipeline ID:  {pipeline_id}")
    summary.append(f"Status:       {get_status_emoji(status)} {status.upper()}")
    summary.append(f"Branch/Tag:   {ref}")
    summary.append(f"Duration:     {format_duration(duration)}")
    summary.append(f"Created:      {created_at}")
    summary.append(f"URL:          {web_url}")
    summary.append("")
    
    # Job breakdown
    summary.append("📊 JOB BREAKDOWN:")
    summary.append("-" * 60)
    for job_status, count in sorted(job_statuses.items()):
        emoji = get_status_emoji(job_status)
        summary.append(f"  {emoji} {job_status.capitalize()}: {count} job(s)")
    summary.append("")
    
    # Failed jobs details
    if failed_jobs:
        summary.append("❌ FAILED JOBS:")
        summary.append("-" * 60)
        for job in failed_jobs:
            summary.append(f"  • {job['name']} (stage: {job['stage']})")
        summary.append("")
    
    # Verdict
    summary.append("🎯 VERDICT:")
    summary.append("-" * 60)
    summary.append(f"  {get_verdict(status, len(failed_jobs))}")
    summary.append("")
    summary.append("=" * 60)
    
    return "\n".join(summary)


def main():
    parser = argparse.ArgumentParser(
        description="Check GitLab pipeline status and generate summary",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check latest pipeline for a project on gitlab.com
  python check_pipeline.py --project 278964

  # Check specific pipeline
  python check_pipeline.py --project 278964 --pipeline 123456789

  # Use self-hosted GitLab instance with authentication
  python check_pipeline.py --url https://gitlab.example.com --project 42 --token YOUR_TOKEN
        """
    )
    
    parser.add_argument(
        "--url",
        default="https://gitlab.com",
        help="GitLab instance URL (default: https://gitlab.com)"
    )
    
    parser.add_argument(
        "--project",
        required=True,
        help="Project ID or path (e.g., '278964' or 'group/project')"
    )
    
    parser.add_argument(
        "--pipeline",
        help="Pipeline ID (if not specified, fetches the latest pipeline)"
    )
    
    parser.add_argument(
        "--token",
        help="GitLab API token (required for private projects)"
    )
    
    args = parser.parse_args()
    
    try:
        print(f"🔍 Fetching pipeline data from {args.url}...")
        print()
        
        data = fetch_pipeline(args.url, args.project, args.pipeline, args.token)
        summary = summarize_pipeline(data)
        print(summary)
        
        # Exit code based on status
        status = data["pipeline"]["status"]
        if status == "success":
            sys.exit(0)
        elif status in ["failed", "canceled"]:
            sys.exit(1)
        else:
            sys.exit(2)  # Running/pending/other
            
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}", file=sys.stderr)
        if e.response.status_code == 401:
            print("💡 Hint: You may need to provide a GitLab API token with --token", file=sys.stderr)
        elif e.response.status_code == 404:
            print("💡 Hint: Check that the project ID and pipeline ID are correct", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
