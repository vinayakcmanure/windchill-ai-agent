import os
from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END

from src.windchill_client import WindchillClient
from src.llm import parse_requirement

# ✅ Router imports
from src.router import route_action, dispatch, enrich_data

# ---- FIX SSL ISSUE ----
os.environ.pop("SSL_CERT_FILE", None)
os.environ.pop("SSL_CERT_DIR", None)

import truststore
truststore.inject_into_ssl()

client = WindchillClient()


# =========================
# STATE DEFINITION
# =========================
class AgentState(TypedDict):
    requirement: str
    endpoint: str
    http_method: str
    current_payload: Dict[str, Any]
    execution_result: Dict[str, Any]
    error_logs: str
    retry_count: int


# =========================
# AUTHOR NODE (FINAL ✅)
# =========================
def author_node(state: AgentState) -> AgentState:
    req = state["requirement"]

    # ✅ Step 1: LLM parsing
    parsed = parse_requirement(req)

    print("\n🤖 LLM RAW OUTPUT:\n", parsed)

    # ✅ Attach requirement (IMPORTANT)
    parsed["requirement"] = req

    # ✅ Step 2: Route
    domain, action = route_action(parsed, req)

    print("\n🔍 Routed Values:")
    print("Domain:", domain)
    print("Action:", action)

    # ✅ ✅ CRITICAL FIX (THIS WAS MISSING)
    parsed = enrich_data(parsed, req)

    # ✅ Step 3: Dispatch
    result = dispatch(domain, action, parsed, client)

    # ✅ Handle errors
    if "error" in result:
        print("⛔ Author failed:", result["error"])
        return {
            **state,
            "error_logs": result["error"]
        }

    # ✅ Success
    return {
        **state,
        "endpoint": result["endpoint"],
        "http_method": result["method"],
        "current_payload": result.get("payload", {}),
        "execution_result": {},
        "error_logs": "",
        "retry_count": 0
    }


# =========================
# EXECUTION NODE
# =========================
def execution_node(state: AgentState) -> AgentState:
    print(f"\n🚀 Executing: {state['http_method']} {state['endpoint']}")

    result = client.execute_request(
        state["http_method"],
        state["endpoint"],
        state["current_payload"]
    )

    print("📦 API RESULT:", result)

    return {
        **state,
        "execution_result": result
    }


# =========================
# HEALER NODE
# =========================
def healer_node(state: AgentState) -> AgentState:
    result = state["execution_result"]

    if result.get("status_code") in [200, 201, 202, 204]:
        print("✅ SUCCESS")
        return {**state, "error_logs": ""}

    print(f"❌ FAILED: {result.get('status_code')}")

    return {
        **state,
        "retry_count": state.get("retry_count", 0) + 1,
        "error_logs": "Failed"
    }


# =========================
# AUTHOR ROUTING
# =========================
def author_route(state: AgentState) -> str:
    if state.get("error_logs"):
        print("⛔ Author failed:", state["error_logs"])
        return "fail"
    return "ok"


# =========================
# HEALER ROUTING
# =========================
def route(state: AgentState) -> str:
    if state["error_logs"] == "":
        return "done"

    if state["retry_count"] >= 2:
        print("⛔ Max retries reached")
        return "fail"

    return "retry"


# =========================
# GRAPH DEFINITION
# =========================
workflow = StateGraph(AgentState)

workflow.add_node("Author", author_node)
workflow.add_node("Executor", execution_node)
workflow.add_node("Healer", healer_node)

workflow.set_entry_point("Author")

workflow.add_conditional_edges(
    "Author",
    author_route,
    {
        "ok": "Executor",
        "fail": END
    }
)

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

# ✅ Used by CLI
windchill_qa_graph = workflow.compile()