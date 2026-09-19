SCHEMA = {
    "Element": {
        "R1ElementID": {"not_null": True, "unique": True},
        "R1Element": {"not_null": True, "unique": True},
    },
    "ElementInstances": {
        "R1InstanceID": {"not_null": True, "unique": True},
        "R1Instance": {"not_null": True, "unique": False},
        "R1InstanceDescription": {"not_null": False, "unique": False},
        "R1InstanceRichText": {"not_null": False, "unique": False},
    },
    "Properties": {
        "Property": {"not_null": True, "unique": True, "normalize": True},
    },
    "PropertyInstances": {
        "R1InstanceID": {"not_null": True, "unique": False},
        "Property": {"not_null": True, "unique": False, "normalize": True},
        "PropertyInstance": {"not_null": False, "unique": False},
    },
    "Relations": {
        "RelationID": {"not_null": True, "unique": False},
        "Relation": {"not_null": True, "unique": False, "normalize": True},
        "Cardinality": {"not_null": False, "unique": False},
        "R1Element": {"not_null": True, "unique": False, "normalize": True},
        "R2ElementID": {"not_null": True, "unique": False},
        "R2Element": {"not_null": True, "unique": False, "normalize": True},
        "ChildR2ElementID": {"not_null": False, "unique": False},
        "ChildR2Element": {"not_null": False, "unique": False, "normalize": True},
    },
    "RelationInstances": {
        "RelationID": {"not_null": True, "unique": False},
        "Relation": {"not_null": True, "unique": False, "normalize": True},
        "Cardinality": {"not_null": False, "unique": False},
        "R1InstanceID": {"not_null": True, "unique": False},
        "R2Element": {"not_null": True, "unique": False, "normalize": True},
        "R2InstanceID": {"not_null": True, "unique": False},
        "R2Instance": {"not_null": True, "unique": False},
    },
}
