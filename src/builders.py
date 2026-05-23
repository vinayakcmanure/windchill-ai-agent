def create_document(name: str, container_oid: str):
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
