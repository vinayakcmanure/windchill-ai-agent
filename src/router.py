"""
Central Router (DocMgmt + PTC Common + PTC ProdMgmt)

Responsibilities:
1. Determine domain + action
2. Enrich missing data (LLM fallback)
3. Dispatch to correct domain handler
"""

from typing import Dict, Any, Tuple

# ✅ DocMgmt handlers
from src.domains.DocMgmt.actions import (
    handle_create,
    handle_set_state,
    handle_checkout,
    handle_checkin,
    handle_delete,
    handle_update
)

# ✅ PTC handlers (metadata level)
from src.domains.PTC.actions import (
    handle_get_all_states,
    handle_get_enum_constraint,
    handle_get_meta,
    handle_get_meta_entity,
    handle_get_version,
    handle_check_assembly
)

# ✅ NEW: PTC ProdMgmt handlers (READ SAFE + core actions)
from src.domains.ProdMgmt.actions import (
    handle_list_parts,
    handle_get_part,
    handle_create_part,
    handle_update_part,
    handle_delete_part,

    handle_list_representations,
    handle_get_representation,
    handle_list_content,
    handle_get_content,

    handle_get_bom,
    handle_checkout_part,
    handle_checkin_part,
    handle_undo_checkout,

    handle_revise_part,
    handle_set_state_part,

    handle_get_references,
    handle_get_usedby,
    handle_get_uses,
    handle_get_describedby,

    handle_get_folder,
    handle_get_context,
    handle_get_organization,
    handle_get_creator,
    handle_get_modifier
)


# =========================================================
# 1. INTENT ROUTING
# =========================================================
def route_action(parsed: Dict[str, Any], requirement: str) -> Tuple[str, str]:
    text = requirement.lower()
    action = parsed.get("action", "create")

    # =====================================================
    # ✅ NEW: PTC PRODMGMT DOMAIN
    # =====================================================

    if "part" in text:

        if any(w in text for w in ["create", "new", "add"]):
            return "ProdMgmt", "create_part"

        if any(w in text for w in ["delete", "remove"]):
            return "ProdMgmt", "delete_part"

        if any(w in text for w in ["update", "modify"]):
            return "ProdMgmt", "update_part"

        if any(w in text for w in ["get", "details", "show"]):
            return "ProdMgmt", "get_part"

        return "ProdMgmt", "list_parts"

    if "representation" in text:
        if "id" in text:
            return "ProdMgmt", "get_representation"
        return "ProdMgmt", "list_representations"

    if "content" in text:
        if "id" in text:
            return "ProdMgmt", "get_content"
        return "ProdMgmt", "list_content"

    if any(w in text for w in ["bom", "structure"]):
        return "ProdMgmt", "get_bom"

    if "checkout" in text:
        return "ProdMgmt", "checkout_part"

    if "checkin" in text:
        return "ProdMgmt", "checkin_part"

    if "undo checkout" in text:
        return "ProdMgmt", "undo_checkout"

    if "revise" in text:
        return "ProdMgmt", "revise_part"

    if "state" in text and "part" in text:
        return "ProdMgmt", "set_state_part"

    if "reference" in text:
        return "ProdMgmt", "get_references"

    if "used by" in text:
        return "ProdMgmt", "get_usedby"

    if "uses" in text:
        return "ProdMgmt", "get_uses"

    if "described" in text:
        return "ProdMgmt", "get_describedby"

    if "folder" in text:
        return "ProdMgmt", "get_folder"

    if "context" in text:
        return "ProdMgmt", "get_context"

    if "organization" in text:
        return "ProdMgmt", "get_organization"

    if "creator" in text:
        return "ProdMgmt", "get_creator"

    if "modifier" in text:
        return "ProdMgmt", "get_modifier"


    # =====================================================
    # ✅ EXISTING PTC DOMAIN (METADATA APIs)
    # =====================================================

    if any(w in text for w in ["all states", "lifecycle states", "state list"]):
        return "ptc", "get_states"

    if any(w in text for w in ["meta", "metadata", "meta info"]):
        if "entity" in text:
            return "ptc", "get_meta_entity"
        return "ptc", "get_meta"

    if any(w in text for w in ["enum", "enumeration", "valid values"]):
        return "ptc", "get_enum"

    if "version" in text:
        return "ptc", "get_version"

    if any(w in text for w in ["assembly", "installed"]):
        return "ptc", "check_assembly"


    # =====================================================
    # ✅ DocMgmt DOMAIN (UNCHANGED)
    # =====================================================

    if any(w in text for w in ["state", "lifecycle", "release", "promote"]):
        return "DocMgmt", "set_state"

    if any(w in text for w in ["create", "new", "add"]):
        return "DocMgmt", "create"

    if any(w in text for w in ["delete", "remove"]):
        return "DocMgmt", "delete"

    if any(w in text for w in ["checkout", "check out"]):
        return "DocMgmt", "checkout"

    if any(w in text for w in ["checkin", "check in"]):
        return "DocMgmt", "checkin"

    if any(w in text for w in ["update", "modify"]):
        return "DocMgmt", "update"

    return "DocMgmt", action.lower()


# =========================================================
# 2. DATA ENRICHMENT
# =========================================================
def enrich_data(data: Dict[str, Any], requirement: str) -> Dict[str, Any]:
    text = requirement.lower()

    if not data.get("state"):
        if "released" in text:
            data["state"] = "Released"
        elif "inwork" in text:
            data["state"] = "INWORK"
        elif "approved" in text:
            data["state"] = "APPROVED"

    return data


# =========================================================
# 3. DISPATCH
# =========================================================
def dispatch(domain: str, action: str, data: Dict[str, Any], client):

    requirement = data.get("requirement", "")
    data = enrich_data(data, requirement)

    if domain == "DocMgmt":
        return _dispatch_DocMgmt(action, data, client)

    elif domain == "ptc":
        return _dispatch_ptc(action, data, client)

    elif domain == "ProdMgmt":
        return _dispatch_ProdMgmt(action, data, client)

    return {"error": f"Unsupported domain: {domain}"}


# =========================================================
# 4. DocMgmt
# =========================================================
def _dispatch_DocMgmt(action: str, data: Dict[str, Any], client):

    if action == "create":
        return handle_create(data, client)
    elif action == "set_state":
        return handle_set_state(data, client)
    elif action == "checkout":
        return handle_checkout(data, client)
    elif action == "checkin":
        return handle_checkin(data, client)
    elif action == "delete":
        return handle_delete(data, client)
    elif action == "update":
        return handle_update(data, client)

    return {"error": f"Unsupported DocMgmt action: {action}"}


# =========================================================
# 5. PTC (metadata)
# =========================================================
def _dispatch_ptc(action: str, data: Dict[str, Any], client):

    if action == "get_states":
        return handle_get_all_states(data, client)
    elif action == "get_enum":
        return handle_get_enum_constraint(data, client)
    elif action == "get_meta":
        return handle_get_meta(data, client)
    elif action == "get_meta_entity":
        return handle_get_meta_entity(data, client)
    elif action == "get_version":
        return handle_get_version(data, client)
    elif action == "check_assembly":
        return handle_check_assembly(data, client)

    return {"error": f"Unsupported PTC action: {action}"}


# =========================================================
# 6. ✅ NEW: PTC PRODMGMT
# =========================================================
def _dispatch_ProdMgmt(action: str, data: Dict[str, Any], client):

    if action == "list_parts":
        return handle_list_parts(data, client)
    elif action == "get_part":
        return handle_get_part(data, client)
    elif action == "create_part":
        return handle_create_part(data, client)
    elif action == "update_part":
        return handle_update_part(data, client)
    elif action == "delete_part":
        return handle_delete_part(data, client)

    elif action == "list_representations":
        return handle_list_representations(data, client)
    elif action == "get_representation":
        return handle_get_representation(data, client)

    elif action == "list_content":
        return handle_list_content(data, client)
    elif action == "get_content":
        return handle_get_content(data, client)

    elif action == "get_bom":
        return handle_get_bom(data, client)

    elif action == "checkout_part":
        return handle_checkout_part(data, client)
    elif action == "checkin_part":
        return handle_checkin_part(data, client)
    elif action == "undo_checkout":
        return handle_undo_checkout(data, client)

    elif action == "revise_part":
        return handle_revise_part(data, client)
    elif action == "set_state_part":
        return handle_set_state_part(data, client)

    elif action == "get_references":
        return handle_get_references(data, client)
    elif action == "get_usedby":
        return handle_get_usedby(data, client)
    elif action == "get_uses":
        return handle_get_uses(data, client)
    elif action == "get_describedby":
        return handle_get_describedby(data, client)

    elif action == "get_folder":
        return handle_get_folder(data, client)
    elif action == "get_context":
        return handle_get_context(data, client)
    elif action == "get_organization":
        return handle_get_organization(data, client)
    elif action == "get_creator":
        return handle_get_creator(data, client)
    elif action == "get_modifier":
        return handle_get_modifier(data, client)

    return {"error": f"Unsupported PTC ProdMgmt action: {action}"}
