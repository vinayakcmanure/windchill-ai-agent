import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import argparse
from src.agents import windchill_qa_graph


def main():
    parser = argparse.ArgumentParser(description="Windchill AI Agent CLI")
    parser.add_argument("--task", required=True)

    args = parser.parse_args()

    state = {
        "requirement": args.task,
        "endpoint": "",
        "http_method": "",
        "current_payload": {},
        "execution_result": {},
        "error_logs": "",
        "retry_count": 0
    }

    print("\n🚀 Running task:", args.task)

    result = windchill_qa_graph.invoke(state)

    print("\n✅ FINAL RESULT:\n", result)


if __name__ == "__main__":
    main()