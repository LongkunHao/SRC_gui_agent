"""
Task: Remove non-CA locations, add San Jose CA and LA CA, save. Then save all active
CA internships.

Discovery: Current locations: SF, NY, Seattle, Austin, Remote. Keep SF, add San Jose CA,
LA CA. CA internships (active): job_01 (Mountain View), job_02 (SF), job_06 (Cupertino),
job_07 (Menlo Park, already saved), job_09 (SF), job_12 (SF, already saved),
job_22 (SF), job_25 (Cupertino), job_26 (Menlo Park), job_29 (SF), job_30 (SF).

Verify:
(1) careerInterests.locations contains only CA cities (San Francisco CA, San Jose CA,
    Los Angeles CA at minimum; no NY, Seattle, Austin, Remote)
(2) All of job_01, job_02, job_06, job_07, job_09, job_12, job_22, job_25, job_26,
    job_29, job_30 in savedJobIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    current_user = state.get("currentUser", {})
    career = current_user.get("careerInterests", {})

    # Check 1: Locations contain only CA cities; no non-CA locations remain
    locations = career.get("locations", [])

    # These non-CA locations must be removed
    non_ca_locations = ["New York, NY", "Seattle, WA", "Austin, TX", "Remote"]
    remaining_non_ca = [loc for loc in locations if loc in non_ca_locations]
    if remaining_non_ca:
        errors.append(
            f"Non-CA locations still present: {remaining_non_ca}. "
            f"Current locations: {locations}"
        )

    # Must have San Francisco CA (kept), San Jose CA (added), Los Angeles CA (added)
    # Check case-insensitively with flexible matching for format variations
    locations_lower = [loc.lower() for loc in locations]

    required_cities = {
        "San Francisco": False,
        "San Jose": False,
        "Los Angeles": False,
    }
    for city_name in required_cities:
        for loc in locations_lower:
            if city_name.lower() in loc and "ca" in loc:
                required_cities[city_name] = True
                break

    missing_cities = [city for city, found in required_cities.items() if not found]
    if missing_cities:
        errors.append(
            f"Required CA cities not found in locations: {missing_cities}. "
            f"Current locations: {locations}"
        )

    # Check 2: All active CA internships in savedJobIds
    saved_job_ids = current_user.get("savedJobIds", [])
    required_jobs = {
        "job_01": "Google SWE Intern (Mountain View)",
        "job_02": "Google APM Intern (SF)",
        "job_06": "Apple SWE Intern (Cupertino)",
        "job_07": "Meta SWE Intern (Menlo Park)",
        "job_09": "Stripe SWE Intern (SF)",
        "job_12": "Airbnb SWE Intern (SF)",
        "job_22": "Google UX Design Intern (SF)",
        "job_25": "Apple ML Intern (Cupertino)",
        "job_26": "Meta RPM Intern (Menlo Park)",
        "job_29": "Databricks DE Intern (SF)",
        "job_30": "Salesforce Marketing Analyst Intern (SF)",
    }

    missing_jobs = []
    for job_id, job_desc in required_jobs.items():
        if job_id not in saved_job_ids:
            missing_jobs.append(f"{job_desc} ({job_id})")

    if missing_jobs:
        errors.append(
            f"Active CA internships not saved: {', '.join(missing_jobs)}. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Locations updated to CA-only cities (San Francisco, San Jose, Los Angeles). "
        "All active CA internships saved: job_01, job_02, job_06, job_07, job_09, "
        "job_12, job_22, job_25, job_26, job_29, job_30."
    )
