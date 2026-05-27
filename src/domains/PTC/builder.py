"""
PTC Common Builder

Builds endpoint + HTTP method + payload
"""

BASE = "/Windchill/servlet/odata/v1/PTC"


# =========================================================
# GET ALL STATES
# =========================================================
def get_all_states():
    return {
        "endpoint": f"{BASE}/GetAllStates()",
        "method": "GET"
    }


# =========================================================
# GET ENUM TYPE CONSTRAINT
# =========================================================
def get_enum_type_constraint(entity_name: str, property_name: str):
    return {
        "endpoint": f"{BASE}/GetEnumTypeConstraint(entityName='{entity_name}',propertyName='{property_name}')",
        "method": "GET"
    }


# =========================================================
# GET META INFO (ALL)
# =========================================================
def get_meta_info():
    return {
        "endpoint": f"{BASE}/GetWindchillMetaInfo()",
        "method": "GET"
    }


# =========================================================
# GET META INFO (BY ENTITY)
# =========================================================
def get_meta_info_by_entity(entity_name: str):
    return {
        "endpoint": f"{BASE}/GetWindchillMetaInfo(EntityName='{entity_name}')",
        "method": "GET"
    }


# =========================================================
# GET WINDCHILL VERSION
# =========================================================
def get_windchill_version():
    return {
        "endpoint": f"{BASE}/GetWindchillVersion()",
        "method": "GET"
    }


# =========================================================
# CHECK ASSEMBLY INSTALLED
# =========================================================
def is_assembly_installed(assembly_name: str):
    return {
        "endpoint": f"{BASE}/IsAssemblyInstalled(assemblyName='{assembly_name}')",
        "method": "GET"
    }