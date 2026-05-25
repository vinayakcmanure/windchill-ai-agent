<div align="center">

# 🤖 Windchill AI Agent

### *Your PLM system, now speaks plain English.*

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestrated-FF6B35?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![PTC Windchill](https://img.shields.io/badge/PTC_Windchill-13.x-0066CC?style=for-the-badge)](https://www.ptc.com/en/products/windchill)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

<br/>

> A **tool-calling AI agent** that understands PLM intent and autonomously executes  
> PTC Windchill operations via WRS REST API — **no manual OID lookups. No repetitive navigation. Just intent → action.**

<br/>

```
"Create Design_Spec_Rev_A in the Released_Products container"
                          ↓
              ✅ Done. Zero clicks. Zero copy-paste.
```

</div>

---

## 📖 Table of Contents

- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [How It Works](#-how-it-works)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage Examples](#-usage-examples)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Author](#-author)

---

## 🧩 The Problem

Engineers working with PTC Windchill spend hours every week on tasks that add **zero engineering value**:

| Pain Point | What Engineers Do Today |
|---|---|
| Container resolution | Manually look up OIDs in the UI before every API call |
| Document creation | Navigate 4–5 menu levels for a routine operation |
| Repetitive workflows | Copy-paste identifiers between sessions and tools |
| API integration work | Write brittle scripts that break on schema changes |

This is not an edge case. It is the **daily reality** for PLM engineers across every major manufacturing enterprise running Windchill.

---

## 💡 The Solution

The **Windchill AI Agent** takes a single natural language instruction and executes the full Windchill operation autonomously — resolving dependencies, chaining API calls, and confirming success. No human intervention required.

```bash
python cli.py --task "Create Design_Spec_Rev_A in the Released_Products container"
```

```
🚀 Windchill AI Agent initializing...
🔍 Resolving container: Released_Products
   └─ OID: OR:wt.inf.container.WTProduct:887766 ✓
📄 Creating document: Design_Spec_Rev_A
   └─ POST /DocMgmt/Documents
✅ Success — Status: 200 Created
```

---

## ⚙️ How It Works

The agent follows a **multi-step tool-calling loop** — each step resolves exactly what the next step needs:

```
Step 1 — Parse Intent
┌──────────────────────────────────────────────────────────┐
│  "Create Design_Spec_Rev_A in Released_Products"         │
│                         ↓                               │
│   LLM identifies: doc_name + container_name             │
│   LLM selects:    Tool 1 → get_container_oid()          │
└──────────────────────────────────────────────────────────┘

Step 2 — Resolve Container OID
┌──────────────────────────────────────────────────────────┐
│  HTTP GET /ContainerMgmt/Containers?name=Released_Products│
│                         ↓                               │
│  Returns: "OR:wt.inf.container.WTProduct:887766"        │
│  LLM stores OID in state → selects Tool 2               │
└──────────────────────────────────────────────────────────┘

Step 3 — Execute the Operation
┌──────────────────────────────────────────────────────────┐
│  HTTP POST /DocMgmt/Documents                           │
│  { name: "Design_Spec_Rev_A",                           │
│    containerRef: "OR:wt.inf.container...887766" }       │
│                         ↓                               │
│  201 Created ✅                                          │
└──────────────────────────────────────────────────────────┘
```

> If any step fails, the **self-healing loop** activates — the agent reads the error response, corrects the payload, and retries automatically.

---

## 🧠 Architecture

```
 ┌────────────────────────────────────────────────────────────┐
 │                     USER INSTRUCTION                       │
 │       "Create Design_Spec_Rev_A in Released_Products"      │
 └──────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
 ┌────────────────────────────────────────────────────────────┐
 │                  LLM / NLP ENGINE                          │
 │        Intent Recognition · Tool Selection · State         │
 └────────────────────┬───────────────────────────────────────┘
                      │
         ┌────────────▼────────────┐
         │         TOOL 1          │
         │   get_container_oid()   │
         │                         │
         │  GET /ContainerMgmt/    │
         │       Containers        │
         └────────────┬────────────┘
                      │  OID resolved & stored in state
         ┌────────────▼────────────┐
         │         TOOL 2          │
         │    create_document()    │
         │                         │
         │  POST /DocMgmt/         │
         │       Documents         │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │    WINDCHILL WRS        │
         │    REST API Layer       │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │   ✅ OPERATION COMPLETE  │
         │   Document Created      │
         └─────────────────────────┘

         ⚠️ On failure at any step:
         └──► SELF-HEALING LOOP ACTIVATES
              Error analysed → Payload corrected → Retry
```

**Agent Components:**

| Component | Role |
|---|---|
| **LLM Engine** | Recognises PLM intent, selects tools, manages state |
| **Tool Layer** | Thin Python wrappers over Windchill WRS REST endpoints |
| **State Graph** | LangGraph passes resolved values (OIDs, handles) between tool calls |
| **Self-Healing Loop** | Reads API error responses and retries with corrected payloads |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Access to a PTC Windchill 13.x instance (non-production recommended for first run)
- OpenAI API key

### 1. Clone

```bash
git clone https://github.com/vinayakcmanure/windchill-agentic-qa.git
cd windchill-agentic-qa
```

### 2. Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔐 Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Fill in your values:

```env
# Windchill Server
WINDCHILL_HOST=https://your-windchill-server.company.com
WINDCHILL_USERNAME=your_username
WINDCHILL_PASSWORD=your_password

# LLM API DETAILS
LLM_API_KEY="abcdefgh1234"
LLM_BASE_URL=https://openai.generative.engine.yourcompany.com/v1
LLM_MODEL=openai.gpt-5.2
```

---

## ▶️ Usage Examples

**Create a document in a named container:**
```bash
python cli.py --task "Create Design_Spec_Rev_A in the Released_Products container"
```

**Create in a specific vault:**
```bash
python cli.py --task "Create Thermal_Analysis_Report inside Engineering_Vault"
```

---

## 📂 Project Structure

```
windchill-ai-agent/
│
├── cli.py                    # ✅ CLI entry point (runs the agent)
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore
├── .env.example
│
└── src/
    ├── __init__.py           # ✅ Makes src a Python package
    │
    ├── agents.py             # ✅ LangGraph workflow (Author → Executor → Healer)
    │
    ├── windchill_client.py  # ✅ Handles:
    │                         #   - CSRF token
    │                         #   - API calls
    │                         #   - container lookup
    │
    └── builders.py           # ✅ Builds payloads (create document etc.)
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| AI Orchestration | LangGraph | State-machine agent loop & tool chaining |
| LLM + Tool Calling | LangChain + OpenAI | Intent recognition & tool invocation |
| PLM Integration | PTC Windchill WRS | REST API target (GET, POST) |
| API Client | Python Requests | HTTP execution layer |
| Validation | Pydantic + JSON Schema | Payload construction & validation |
| Runtime | Python 3.10+ | Core language |

---

## ✅ Key Capabilities

| Capability | Detail |
|---|---|
| 🗣️ Natural Language Input | Plain English → Windchill operations, no syntax to learn |
| 🔗 Multi-step Tool Chaining | OID resolution feeds directly into document creation |
| 🔁 Self-Healing Loop | Reads API errors, corrects payloads, retries automatically |
| 🏗️ Extensible Tool Library | Add new WRS operations by registering new tools |
| 🏭 Enterprise Validated | Tested on a live Windchill 13.x enterprise environment |
| 🔒 Secure by Default | Credentials in `.env`, never hardcoded |

---

## 🗺️ Roadmap

| Status | Feature |
|---|---|
| ✅ Done | Document creation via natural language |
| ✅ Done | Container OID resolution — automatic |
| ✅ Done | Self-healing execution loop |
| 🔄 In Progress | Part creation and BOM operations |
| 📋 Planned | Workflow trigger via natural language |
| 📋 Planned | ECR / ECN creation and routing |
| 📋 Planned | Multi-step chains ("Create part → attach doc → submit for review") |
| 📋 Planned | Windchill+ / SaaS OData API support |
| 💡 Exploring | Voice input interface |

---

## 🤝 Contributing

Contributions are welcome — especially from the PLM and AI/LangChain communities.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add: your feature description"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

For major changes, please open an issue first to discuss scope and approach.

---

## 👤 Author

<div align="center">

**Vinayak Manure**

*Principal Solution Architect — PLM & AI*
*18+ years of PTC Windchill delivery across global manufacturing enterprises*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vinayak-manure-71961615/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/vinayakcmanure)

*Built from 18 years of Windchill pain — and a belief that engineers deserve better tools.*

</div>

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.
See [LICENSE](LICENSE) for full details.

---

<div align="center">

*If this project saves you time, consider giving it a ⭐ — it helps others in the PLM community discover it.*

</div>
