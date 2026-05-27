# src/domains/ProdMgmt/actions.py

"""
ProdMgmt Actions Layer
Maps router intent → actual API calls
"""

from src.windchill_client import WindchillClient
from .builder import (
    build_create_part_payload,
    build_update_part_payload,
    build_checkout_payload,
    build_checkin_payload,
    build_bom_payload,
    build_revise_payload,
    build_setstate_payload
)


# =========================================================
# ✅ PARTS (CRUD)
# =========================================================

def handle_list_parts(data, client):
    return client.get("/Parts")


def handle_get_part(data, client):
    part_id = data["part_id"]
    return client.get(f"/Parts('{part_id}')")


def handle_create_part(data, client: WindchillClient):
    payload = build_create_part_payload(data)
    csrf = client.get_csrf_token()

    return client.post(
        "/Parts",
        json=payload,
        headers={"CSRF_NONCE": csrf}
    )


def handle_update_part(data, client):
    part_id = data["part_id"]
    payload = build_update_part_payload(data)
    csrf = client.get_csrf()

    return client.patch(
        f"/Parts('{part_id}')",
        json=payload,
        headers={"CSRF_NONCE": csrf}
    )


def handle_delete_part(data, client):
    part_id = data["part_id"]
    csrf = client.get_csrf()

    return client.delete(
        f"/Parts('{part_id}')",
        headers={"CSRF_NONCE": csrf}
    )


# =========================================================
# ✅ CHECKOUT / CHECKIN (BOUND ACTIONS)
# =========================================================

def handle_checkout_part(data, client):
    part_id = data["part_id"]
    payload = build_checkout_payload(data)
    csrf = client.get_csrf()

    return client.post(
        f"/Parts('{part_id}')/PTC.ProdMgmt.CheckOut",
        json=payload,
        headers={"CSRF_NONCE": csrf}
    )


def handle_checkin_part(data, client):
    part_id = data["part_id"]
    payload = build_checkin_payload(data)
    csrf = client.get_csrf()

    return client.post(
        f"/Parts('{part_id}')/PTC.ProdMgmt.CheckIn",
        json=payload,
        headers={"CSRF_NONCE": csrf}
    )


def handle_undo_checkout(data, client):
    part_id = data["part_id"]
    csrf = client.get_csrf()

    return client.post(
        f"/Parts('{part_id}')/PTC.ProdMgmt.UndoCheckOut",
        headers={"CSRF_NONCE": csrf}
    )


# =========================================================
# ✅ BOM
# =========================================================

def handle_get_bom(data, client):
    part_id = data["part_id"]
    payload = build_bom_payload(data)
    csrf = client.get_csrf()

    return client.post(
        f"/Parts('{part_id}')/PTC.ProdMgmt.GetBOM",
        json=payload,
        headers={"CSRF_NONCE": csrf}
    )


# =========================================================
# ✅ REVISE / STATE
# =========================================================

def handle_revise_part(data, client):
    part_id = data["part_id"]
    payload = build_revise_payload(data)
    csrf = client.get_csrf()

    return client.post(
        f"/Parts('{part_id}')/PTC.ProdMgmt.Revise",
        json=payload,
        headers={"CSRF_NONCE": csrf}
    )


def handle_set_state_part(data, client):
    part_id = data["part_id"]
    payload = build_setstate_payload(data)
    csrf = client.get_csrf()

    return client.post(
        f"/Parts('{part_id}')/PTC.ProdMgmt.SetState",
        json=payload,
        headers={"CSRF_NONCE": csrf}
    )


# =========================================================
# ✅ RELATIONSHIPS (GET ONLY)
# =========================================================

def handle_get_references(data, client):
    return client.get(f"/Parts('{data['part_id']}')/References")


def handle_get_describedby(data, client):
    return client.get(f"/Parts('{data['part_id']}')/DescribedBy")


def handle_get_usedby(data, client):
    return client.get(f"/Parts('{data['part_id']}')/UsedBy")


def handle_get_uses(data, client):
    return client.get(f"/Parts('{data['part_id']}')/Uses")


# =========================================================
# ✅ REPRESENTATIONS / CONTENT
# =========================================================

def handle_list_representations(data, client):
    return client.get(f"/Parts('{data['part_id']}')/Representations")


def handle_get_representation(data, client):
    return client.get(
        f"/Parts('{data['part_id']}')/Representations('{data['representation_id']}')"
    )


def handle_list_content(data, client):
    return client.get(
        f"/Parts('{data['part_id']}')/Representations('{data['representation_id']}')/Content"
    )


def handle_get_content(data, client):
    return client.get(
        f"/Parts('{data['part_id']}')/Representations('{data['representation_id']}')/Content('{data['content_id']}')"
    )


# =========================================================
# ✅ CONTEXT / META
# =========================================================

def handle_get_folder(data, client):
    return client.get(f"/Parts('{data['part_id']}')/Folder")


def handle_get_context(data, client):
    return client.get(f"/Parts('{data['part_id']}')/Context")


def handle_get_creator(data, client):
    return client.get(f"/Parts('{data['part_id']}')/Creator")


def handle_get_modifier(data, client):
    return client.get(f"/Parts('{data['part_id']}')/Modifier")


def handle_get_organization(data, client):
    return client.get(f"/Parts('{data['part_id']}')/Organization")
