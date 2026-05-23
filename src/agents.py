import os
import re
from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END

# CORRECT IMPORTS (THIS FIXES YOUR ERROR)
from src.windchill_client import WindchillClient
from src.builders import create_document


# ---- FIX SSL ISSUE (Enterprise environments) ----
os.environ.pop("SSL_CERT_FILE", None)
os.environ.pop("SSL_CERT_DIR", None)

import truststore
truststore.inject_into_ssl()

client = WindchillClient()


# -------------------------
# STATE DEFINITION
# -------------------------
class AgentState(TypedDict):
    requirement: str
    endpoint: str
    http_method: str
    current_payload: Dict[str, Any]
    execution_result: Dict[str, Any]
    error_logs: str
    retry_count: int


# -------------------------
# AUTHOR NODE (Parser + Builder)
# -------------------------
def author_node(state: AgentState) -> AgentState:
    req = state["requirement"]

    # Extract document name
    name_match = re.search(r"create\s+([a-zA-Z0-9_\-]+)", req, re.IGNORECASE)

    # Extract full container (supports spaces)
    container_match = re.search(r"inside\s+(.+)", req, re.IGNORECASE)

    if not name_match:
        return {**state, "error_logs": "Document name not found"}

    doc_name = name_match.group(1)
    container_name = container_match.group(1).strip() if container_match else None

    print("Document:", doc_name)
    print("Container:", container_name)

    # Handle document creation
    if "doc" in req.lower() or "document" in req.lower():

        container_oid = client.get_container_id(container_name)

        if not container_oid:
            return {
                **state,
                "error_logs": f"Container '{container_name}' not found"
            }

        config = create_document(doc_name, container_oid)

        return {
            **state,
            "endpoint": config["endpoint"],
            "http_method": config["method"],
            "current_payload": config["payload"],
            "retry_count": 0,
            "execution_result": {},
            "error_logs": ""
        }

    return {**state, "error_logs": "Unsupported operation"}


# -------------------------
# EXECUTION NODE
# -------------------------
def execution_node(state: AgentState) -> AgentState:
    print(f"\n Executing: {state['http_method']} {state['endpoint']}")

    result = client.execute_request(
        state["http_method"],
        state["endpoint"],
        state["current_payload"]
    )

    print(" API RESULT:", result)

    return {
        **state,
        "execution_result": result
    }


# -------------------------
# SELF-HEALING NODE
# -------------------------
def healer_node(state: AgentState) -> AgentState:
    result = state["execution_result"]

    if result.get("status_code") in [200, 201, 202, 204]:
        print(" SUCCESS")
        return {**state, "error_logs": ""}

    print(f" FAILED: {result.get('status_code')}")

    return {
        **state,
        "retry_count": state.get("retry_count", 0) + 1,
        "error_logs": "Failed"
    }


# -------------------------
# ROUTING LOGIC
# -------------------------
def route(state: AgentState) -> str:
    if state["error_logs"] == "":
        return "done"

    if state["retry_count"] >= 2:
        print(" Max retries reached")
        return "fail"

    return "retry"


# -------------------------
# GRAPH DEFINITION
# -------------------------
workflow = StateGraph(AgentState)

workflow.add_node("Author", author_node)
workflow.add_node("Executor", execution_node)
workflow.add_node("Healer", healer_node)

workflow.set_entry_point("Author")

workflow.add_edge("Author", "Executor")
workflow.add_edge("Executor", "Healer")

workflow.add_conditional_edges(
    "Healer",
    route,
    {
        "retry": "Executor",
        "done": END,
        "fail": END
    }
)

#  USED BY CLI
windchill_qa_graph = workflow.compile()