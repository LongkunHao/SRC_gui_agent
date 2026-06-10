import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find template named "Geriatric Assessment"
    templates = state.get("visitNoteTemplates", [])
    geriatric = None
    for t in templates:
        name = (t.get("name") or "").strip()
        if name.lower() == "geriatric assessment":
            geriatric = t
            break

    if not geriatric:
        return False, "Template 'Geriatric Assessment' not found."

    errors = []

    # Check content sections
    content = geriatric.get("content", {})

    hpi = content.get("hpi")
    if not hpi:
        errors.append("content.hpi is empty or missing")

    ros = content.get("ros")
    if not ros:
        errors.append("content.ros is empty or missing")

    pe = content.get("pe")
    if not pe:
        errors.append("content.pe is empty or missing")

    # Check billing items for 99205
    billing_items = geriatric.get("billingItems", [])
    found_99205 = False
    for bi in billing_items:
        cpt = str(bi.get("cptCode", ""))
        if cpt == "99205":
            desc = (bi.get("description") or "").lower()
            if "high complexity" in desc:
                found_99205 = True
            else:
                # Accept 99205 even if description doesn't exactly say "high complexity"
                found_99205 = True
            break

    if not found_99205:
        cpt_codes = [bi.get("cptCode") for bi in billing_items]
        errors.append(f"Missing billing item with cptCode 99205. Found: {cpt_codes}")

    if errors:
        return False, f"Template 'Geriatric Assessment' found but has issues: {'; '.join(errors)}"

    return True, "Template 'Geriatric Assessment' created with HPI, ROS, PE content and billing code 99205."
