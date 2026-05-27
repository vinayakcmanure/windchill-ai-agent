"""
PTC Common Actions

Handles validation + calls builder
"""

from typing import Dict, Any
from src.domains.PTC import builder


# =========================================================
# GET ALL STATES
# =========================================================
def handle_get_all_states(data: Dict[str, Any], client):
    return builder.get_all_states()


# =========================================================
# GET ENUM CONSTRAINT
# =========================================================
def handle_get_enum_constraint(data: Dict[str, Any], client):
    entity = data.get("entity")
    prop = data.get("property")

    if not entity or not prop:
        return {"error": "Missing entity or property name"}

    return builder.get_enum_type_constraint(entity, prop)


# =========================================================
# GET META INFO (ALL)
# =========================================================
def handle_get_meta(data: Dict[str, Any], client):
    return builder.get_meta_info()


# =========================================================
# GET META INFO (ENTITY)
# =========================================================
def handle_get_meta_entity(data: Dict[str, Any], client):
    entity = data.get("entity")

    if not entity:
        return {"error": "Missing entity name"}

    return builder.get_meta_info_by_entity(entity)


# =========================================================
# GET VERSION
# =========================================================
def handle_get_version(data: Dict[str, Any], client):
    return builder.get_windchill_version()


# =========================================================
# CHECK ASSEMBLY
# =========================================================
def handle_check_assembly(data: Dict[str, Any], client):
    assembly = data.get("assembly")

    if not assembly:
        return {"error": "Missing assembly name"}

    return builder.is_assembly_installed(assembly)