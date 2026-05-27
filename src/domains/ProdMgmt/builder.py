# src/domains/ProdMgmt/builder.py

"""
Payload Builder Layer
Builds request bodies for API calls
"""


# =========================================================
# ✅ PART CREATION
# =========================================================

def build_create_part_payload(data):
    return {
        "Name": data.get("name"),
        "Number": data.get("number"),
        "Type": data.get("type", "wt.part.WTPart"),
        "Context": data.get("context", "Default"),
    }


def build_update_part_payload(data):
    return {
        "Name": data.get("name"),
        "Description": data.get("description"),
    }


# =========================================================
# ✅ CHECKOUT / CHECKIN
# =========================================================

def build_checkout_payload(data):
    return {
        "Comments": data.get("comment", "Checkout via API")
    }


def build_checkin_payload(data):
    return {
        "Comments": data.get("comment", "Checkin via API"),
        "KeepCheckedOut": data.get("keep_checked_out", False)
    }


# =========================================================
# ✅ BOM
# =========================================================

def build_bom_payload(data):
    return {
        "NavigationCriteriaId": data.get("nav_criteria_id"),
        "Depth": data.get("depth", 1)
    }


# =========================================================
# ✅ REVISE
# =========================================================

def build_revise_payload(data):
    return {
        "Comments": data.get("comment", "Revision created"),
    }


# =========================================================
# ✅ SET STATE
# =========================================================

def build_setstate_payload(data):
    return {
        "State": data.get("state", "INWORK"),
        "Comments": data.get("comment", "")
    }