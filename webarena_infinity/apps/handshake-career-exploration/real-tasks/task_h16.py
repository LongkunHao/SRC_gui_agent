import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    career = state.get("currentUser", {}).get("careerInterests", {})
    errors = []

    # Check 1: careerCommunity == 'Technology'
    community = career.get("careerCommunity", "")
    if community != "Technology":
        errors.append(f"careerCommunity is '{community}', expected 'Technology'.")

    # Check 2: roles contains exactly the 4 AI/ML-focused roles (any order)
    roles = career.get("roles", [])
    expected_roles = {"Software Engineer", "Machine Learning Engineer", "Data Scientist", "Research Scientist"}
    removed_roles = {"Product Manager", "UX Designer"}

    current_roles_set = set(roles)
    missing_roles = expected_roles - current_roles_set
    unwanted_roles = removed_roles & current_roles_set
    extra_roles = current_roles_set - expected_roles

    if missing_roles:
        errors.append(f"Missing required roles: {missing_roles}. Current roles: {roles}")
    if unwanted_roles:
        errors.append(f"Roles that should have been removed are still present: {unwanted_roles}. Current roles: {roles}")
    if extra_roles:
        errors.append(f"Unexpected extra roles found: {extra_roles}. Current roles: {roles}")

    # Check 3: industries contains exactly ['Technology', 'Artificial Intelligence'] (any order)
    industries = career.get("industries", [])
    expected_industries = {"Technology", "Artificial Intelligence"}
    removed_industries = {"Finance", "Healthcare Technology"}

    current_industries_set = set(industries)
    missing_industries = expected_industries - current_industries_set
    unwanted_industries = removed_industries & current_industries_set
    extra_industries = current_industries_set - expected_industries

    if missing_industries:
        errors.append(f"Missing required industries: {missing_industries}. Current industries: {industries}")
    if unwanted_industries:
        errors.append(f"Industries that should have been removed are still present: {unwanted_industries}. Current industries: {industries}")
    if extra_industries:
        errors.append(f"Unexpected extra industries found: {extra_industries}. Current industries: {industries}")

    if errors:
        return False, " | ".join(errors)

    return True, (
        f"Career interests updated to AI/ML focus: "
        f"careerCommunity='Technology', roles={roles}, industries={industries}."
    )
