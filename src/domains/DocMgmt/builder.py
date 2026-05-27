"""
DocMgmt Builder

Builds endpoint + HTTP method + payload
"""

BASE = "/Windchill/servlet/odata/v1/DocMgmt"


# -------------------------------
# CREATE
# -------------------------------
def create_document(name: str, container_oid: str):
    return {
        "endpoint": f"{BASE}/Documents",
        "method": "POST",
        "payload": {
            "Name": name,
            "Title": name,
            "Description": name,
            "Context@odata.bind": f"Containers('{container_oid}')"
        }
    }


# -------------------------------
# READ
# -------------------------------
def get_documents():
    return {
        "endpoint": f"{BASE}/Documents",
        "method": "GET"
    }


def get_document(doc_id: str):
    return {
        "endpoint": f"{BASE}/Documents('{doc_id}')",
        "method": "GET"
    }


# -------------------------------
# UPDATE
# -------------------------------
def update_document(doc_id: str, updates: dict):
    return {
        "endpoint": f"{BASE}/Documents('{doc_id}')",
        "method": "PATCH",
        "payload": updates
    }


# -------------------------------
# DELETE
# -------------------------------
def delete_document(doc_id: str):
    return {
        "endpoint": f"{BASE}/Documents('{doc_id}')",
        "method": "DELETE"
    }


# -------------------------------
# CHECKOUT
# -------------------------------
def checkout_document(doc_id: str, note: str):
    return {
        "endpoint": f"{BASE}/Documents('{doc_id}')/PTC.DocMgmt.CheckOut",
        "method": "POST",
        "payload": {
            "CheckOutNote": note
        }
    }


# -------------------------------
# CHECKIN
# -------------------------------
def checkin_document(doc_id: str, note: str, keep_checked_out: bool):
    return {
        "endpoint": f"{BASE}/Documents('{doc_id}')/PTC.DocMgmt.CheckIn",
        "method": "POST",
        "payload": {
            "CheckInNote": note,
            "KeepCheckedOut": keep_checked_out
        }
    }


# -------------------------------
# UNDO CHECKOUT
# -------------------------------
def undo_checkout(doc_id: str):
    return {
        "endpoint": f"{BASE}/Documents('{doc_id}')/PTC.DocMgmt.UndoCheckOut",
        "method": "POST"
    }


# -------------------------------
# REVISE
# -------------------------------
def revise_document(doc_id: str):
    return {
        "endpoint": f"{BASE}/Documents('{doc_id}')/PTC.DocMgmt.Revise",
        "method": "POST",
        "payload": {}
    }


# -------------------------------
# SET STATE
# -------------------------------
def set_state(doc_id: str, state: str):
    return {
        "endpoint": f"{BASE}/Documents('{doc_id}')/PTC.DocMgmt.SetState",
        "method": "POST",
        "payload": {
            "State": {
                "Value": state
            }
        }
    }


# -------------------------------
# ATTACHMENTS
# -------------------------------
def get_attachments(doc_id: str):
    return {
        "endpoint": f"{BASE}/Documents('{doc_id}')/Attachments",
        "method": "GET"
    }


def add_attachment(doc_id: str):
    return {
        "endpoint": f"{BASE}/Documents('{doc_id}')/Attachments",
        "method": "POST",
        "payload": {
            "@odata.type": "#PTC.ContentItem"
        }
    }


# -------------------------------
# UPLOAD (Stage 1)
# -------------------------------
def upload_stage1(doc_id: str, num_files: int):
    return {
        "endpoint": f"{BASE}/Documents('{doc_id}')/PTC.DocMgmt.uploadStage1Action",
        "method": "POST",
        "payload": {
            "noOfFiles": num_files
        }
    }


# -------------------------------
# UPLOAD (Stage 3)
# -------------------------------
def upload_stage3(doc_id: str, content_info: list):
    return {
        "endpoint": f"{BASE}/Documents('{doc_id}')/PTC.DocMgmt.uploadStage3Action",
        "method": "POST",
        "payload": {
            "contentInfo": content_info
        }
    }
