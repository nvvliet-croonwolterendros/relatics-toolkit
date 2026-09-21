SCHEMA = {
    "Element": {
        "columns": {
            "R1ElementID": {"not_null": True},
            "R1Element": {"not_null": True, "normalize": True},
        },
        "unique": [
            ["R1ElementID"],
            ["R1Element"],
        ],
    },
    "ElementInstances": {
        "columns": {
            "R1InstanceID": {"not_null": True},
            "R1Instance": {"not_null": True},
            "R1InstanceDescription": {"not_null": False},
            "R1InstanceRichText": {"not_null": False},
        },
        "unique": [
            ["R1InstanceID"],
        ],
    },
    "Properties": {
        "columns": {
            "Property": {"not_null": True, "normalize": True},
        },
        "unique": [
            ["Property"],
        ],
    },
    "PropertyInstances": {
        "columns": {
            "R1InstanceID": {"not_null": True},
            "Property": {"not_null": True, "normalize": True},
            "PropertyInstance": {"not_null": False},
        },
        "unique": [
            ["R1InstanceID", "Property"],
        ],
    },
    "Relations": {
        "columns": {
            "RelationID": {"not_null": True},
            "Relation": {"not_null": True, "normalize": True},
            "Cardinality": {"not_null": False},
            "R1Element": {"not_null": True, "normalize": True},
            "R2ElementID": {"not_null": True},
            "R2Element": {"not_null": True, "normalize": True},
            "ChildR2ElementID": {"not_null": False},
            "ChildR2Element": {"not_null": False, "normalize": True},
        },
    },
    "RelationInstances": {
        "columns": {
            "RelationID": {"not_null": True},
            "Relation": {"not_null": True, "normalize": True},
            "Cardinality": {"not_null": False},
            "R1InstanceID": {"not_null": True},
            "R2Element": {"not_null": True, "normalize": True},
            "R2InstanceID": {"not_null": True},
            "R2Instance": {"not_null": True},
        },
    },
}
