"""
DocMgmt Builder

Responsible for constructing API requests (endpoint + method + payload)
"""

from typing import Dict, Any


def create_document(name: str, container_oid: str) -> Dict[str, Any]:
    """
    Build payload for creating a document in Windchill.

    Args:
        name: Document name
        container_oid: Container ID

    Returns:
        Dict containing endpoint, method, and payload
    """

    return {
        "endpoint": "/Windchill/servlet/odata/v7/DocMgmt/Documents",
        "method": "POST",
        "payload": {
            "Name": name,
            "Title": name,
            "Description": name,
            "Context@odata.bind": f"Containers('{container_oid}')"
        }
    }