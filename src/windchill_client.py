import os
import requests
from dotenv import load_dotenv

load_dotenv()


class WindchillClient:
    def __init__(self):
        self.host = os.getenv("WINDCHILL_HOST", "").rstrip('/')
        self.username = os.getenv("WINDCHILL_USERNAME")
        self.password = os.getenv("WINDCHILL_PASSWORD")

        self.session = requests.Session()
        self.container_cache = {}

        print("Host:", self.host)
        print("Username:", self.username)

    # =========================================================
    # CSRF TOKEN
    # =========================================================
    def get_csrf_token(self):
        url = f"{self.host}/Windchill/servlet/odata/v5/PTC/GetCSRFToken()"
        try:
            response = self.session.get(
                url,
                auth=(self.username, self.password),
                timeout=10
            )
            if response.status_code == 200:
                return response.json().get("NonceValue")
            return None
        except Exception:
            return None

    # =========================================================
    # CONTAINER RESOLUTION
    # =========================================================
    def get_container_id(self, container_name: str):
        if container_name.lower() in self.container_cache:
            return self.container_cache[container_name.lower()]

        url = f"{self.host}/Windchill/servlet/odata/v7/DataAdmin/Containers"

        try:
            response = self.session.get(
                url,
                auth=(self.username, self.password),
                headers={"Accept": "application/json"},
                timeout=15
            )

            if response.status_code != 200:
                return None

            data = response.json()

            for c in data.get("value", []):
                name = c.get("Name", "").lower()
                if container_name.lower() in name:
                    oid = c.get("ID")
                    self.container_cache[container_name.lower()] = oid
                    return oid

            return None

        except Exception:
            return None

    # =========================================================
    # ✅ DOCUMENT RESOLUTION (NEW FIX)
    # =========================================================
    def get_document_id(self, document_name: str):
        """
        Resolve document name → Windchill document ID (OID)
        """

        endpoint = f"/Windchill/servlet/odata/v1/DocMgmt/Documents?$filter=Name eq '{document_name}'"

        response = self.execute_request("GET", endpoint)

        if not response or response.get("status_code") != 200:
            print(f"❌ Failed to fetch document: {document_name}")
            return None

        data = response.get("body", {})

        docs = data.get("value", [])

        if not docs:
            print(f"❌ Document '{document_name}' not found")
            return None

        doc_id = docs[0].get("ID")

        print(f"✅ Resolved document ID: {doc_id}")

        return doc_id

    # =========================================================
    # EXECUTION ENGINE
    # =========================================================
    def execute_request(self, method, endpoint, payload=None):
        url = f"{self.host}{endpoint}"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            # ✅ CSRF for write operations
            if method.upper() in ["POST", "PUT", "PATCH"]:
                token = self.get_csrf_token()
                if not token:
                    return {"status_code": 401, "error": "CSRF failed"}
                headers["CSRF_NONCE"] = token

            response = getattr(self.session, method.lower())(
                url,
                auth=(self.username, self.password),
                headers=headers,
                json=payload,
                timeout=15
            )

            try:
                body = response.json()
            except Exception:
                body = {"raw": response.text[:300]}

            return {
                "status_code": response.status_code,
                "body": body,
                "error": None if response.ok else body
            }

        except Exception as e:
            return {"status_code": 500, "error": str(e)}