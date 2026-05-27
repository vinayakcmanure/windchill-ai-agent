"""
DocMgmt Actions

Handles business logic + validation before calling builders
"""

from typing import Dict, Any
from src.domains.DocMgmt import builder


# =========================================================
# 🔧 HELPER: Resolve Document ID
# =========================================================
def resolve_document_id(data: Dict[str, Any], client):
    """
    Resolve document name to document ID if possible
    """
    doc_id = data.get("document_id")

    if doc_id:
        return doc_id

    doc_name = data.get("document")
    if not doc_name:
        return None

    return client.get_document_id(doc_name)


# =========================================================
# CREATE
# =========================================================
def handle_create(data: Dict[str, Any], client):
    doc_name = data.get("document")
    container_name = data.get("container")

    if not doc_name or not container_name:
        return {"error": "Missing document or container"}

    container_oid = client.get_container_id(container_name)
    if not container_oid:
        return {"error": f"Container '{container_name}' not found"}

    return builder.create_document(doc_name, container_oid)


# =========================================================
# READ
# =========================================================
def handle_get(data: Dict[str, Any], client):
    doc_id = resolve_document_id(data, client)

    # ✅ fallback
    if not doc_id:
        doc_id = data.get("document")

    if doc_id:
        return builder.get_document(doc_id)

    return builder.get_documents()


# =========================================================
# UPDATE
# =========================================================
def handle_update(data: Dict[str, Any], client):
    doc_id = resolve_document_id(data, client)

    # ✅ fallback
    if not doc_id:
        doc_id = data.get("document")

    updates = data.get("updates")

    if not doc_id or not updates:
        return {"error": "Missing document or updates"}

    return builder.update_document(doc_id, updates)


# =========================================================
# DELETE
# =========================================================
def handle_delete(data: Dict[str, Any], client):
    doc_id = resolve_document_id(data, client)

    # ✅ fallback
    if not doc_id:
        doc_id = data.get("document")

    if not doc_id:
        return {"error": "Missing document"}

    return builder.delete_document(doc_id)


# =========================================================
# CHECKOUT
# =========================================================
def handle_checkout(data: Dict[str, Any], client):
    doc_id = resolve_document_id(data, client)

    # ✅ fallback
    if not doc_id:
        doc_id = data.get("document")

    note = data.get("note", "")

    if not doc_id:
        return {"error": "Missing document"}

    return builder.checkout_document(doc_id, note)


# =========================================================
# CHECKIN
# =========================================================
def handle_checkin(data: Dict[str, Any], client):
    doc_id = resolve_document_id(data, client)

    # ✅ fallback
    if not doc_id:
        doc_id = data.get("document")

    note = data.get("note", "")
    keep_checked_out = data.get("keep_checked_out", False)

    if not doc_id:
        return {"error": "Missing document"}

    return builder.checkin_document(doc_id, note, keep_checked_out)


# =========================================================
# UNDO CHECKOUT
# =========================================================
def handle_undo_checkout(data: Dict[str, Any], client):
    doc_id = resolve_document_id(data, client)

    # ✅ fallback
    if not doc_id:
        doc_id = data.get("document")

    if not doc_id:
        return {"error": "Missing document"}

    return builder.undo_checkout(doc_id)


# =========================================================
# REVISE
# =========================================================
def handle_revise(data: Dict[str, Any], client):
    doc_id = resolve_document_id(data, client)

    # ✅ fallback
    if not doc_id:
        doc_id = data.get("document")

    if not doc_id:
        return {"error": "Missing document"}

    return builder.revise_document(doc_id)


# =========================================================
# SET STATE ✅ (THIS IS YOUR CASE)
# =========================================================
def handle_set_state(data: Dict[str, Any], client):
    doc_id = resolve_document_id(data, client)

    # ✅ ✅ CRITICAL FIX (fallback)
    if not doc_id:
        doc_id = data.get("document")

    state = data.get("state")

    if not doc_id or not state:
        return {"error": "Missing document_id or state"}

    return builder.set_state(doc_id, state)


# =========================================================
# ATTACHMENTS
# =========================================================
def handle_add_attachment(data: Dict[str, Any], client):
    doc_id = resolve_document_id(data, client)

    # ✅ fallback
    if not doc_id:
        doc_id = data.get("document")

    if not doc_id:
        return {"error": "Missing document"}

    return builder.add_attachment(doc_id)


def handle_get_attachments(data: Dict[str, Any], client):
    doc_id = resolve_document_id(data, client)

    # ✅ fallback
    if not doc_id:
        doc_id = data.get("document")

    if not doc_id:
        return {"error": "Missing document"}

    return builder.get_attachments(doc_id)
