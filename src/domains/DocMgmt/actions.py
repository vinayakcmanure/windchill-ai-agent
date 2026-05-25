"""
DocMgmt Actions

Responsible for handling business logic for DocMgmt domain.
"""

from typing import Dict, Any
from src.domains.DocMgmt.builder import create_document


def handle_create(data: Dict[str, Any], client) -> Dict[str, Any]:
    """
    Handle document creation flow.

    Args:
        data: Parsed LLM output
        client: WindchillClient instance

    Returns:
        API request config or error
    """

    doc_name = data.get("document")
    container_name = data.get("container")

    if not doc_name or not container_name:
        return {"error": "Missing document or container"}

    # ✅ Resolve container ID
    container_oid = client.get_container_id(container_name)

    if not container_oid:
        return {"error": f"Container '{container_name}' not found"}

    # ✅ Build API request using builder
    return create_document(doc_name, container_oid)
