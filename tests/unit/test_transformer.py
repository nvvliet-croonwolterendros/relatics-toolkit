import pandas as pd
import pytest

from relatics_toolkit.processing.transformer import _prepare_relation_targets


def test_prepare_relation_targets_disambiguates_self_ref():
    """Prefixes self-referencing target elements with the relation name."""
    relations_df = pd.DataFrame(
        {
            "RelationID": [1, 2],
            "Relation": ["manages", "reports_to"],
            "R1Element": ["person", "person"],
            "R2Element": ["person", "person"],
            "R2ElementID": [1, 1],
            "ChildR2Element": [None, None],
            "ChildR2ElementID": [None, None],
        }
    )

    relation_instances_df = pd.DataFrame(
        {
            "RelationID": [1, 2],
            "Relation": ["manages", "reports_to"],
            "R2Element": ["person", "person"],
        }
    )

    relations_df, relation_instances_df = _prepare_relation_targets(
        relations_df,
        relation_instances_df,
    )

    assert relations_df["R2Element"].tolist() == [
        "manages_person",
        "reports_to_person",
    ]

    assert relation_instances_df["R2Element"].tolist() == [
        "manages_person",
        "reports_to_person",
    ]


def test_prepare_relation_targets_disambiguates_duplicate_targets():
    """Prefixes duplicate target elements with the relation name."""
    relations_df = pd.DataFrame(
        {
            "RelationID": [1, 2],
            "Relation": ["borrows", "owns"],
            "R1Element": ["person", "person"],
            "R2Element": ["device", "device"],
            "R2ElementID": [1, 1],
            "ChildR2Element": [None, None],
            "ChildR2ElementID": [None, None],
        }
    )

    relation_instances_df = pd.DataFrame(
        {
            "RelationID": [1, 2],
            "Relation": ["borrows", "owns"],
            "R2Element": ["device", "device"],
        }
    )

    relations_df, relation_instances_df = _prepare_relation_targets(
        relations_df,
        relation_instances_df,
    )

    assert relations_df["R2Element"].tolist() == [
        "borrows_device",
        "owns_device",
    ]

    assert relation_instances_df["R2Element"].tolist() == [
        "borrows_device",
        "owns_device",
    ]


def test_prepare_relation_targets_coalesces_child_elements():
    """Replaces target elements and IDs with child element values when present."""
    relations_df = pd.DataFrame(
        {
            "RelationID": [1, 2],
            "Relation": ["borrows", "owns"],
            "R1Element": ["person", "person"],
            "R2Element": ["device", "component"],
            "R2ElementID": [1, 2],
            "ChildR2Element": [None, "hardware"],
            "ChildR2ElementID": [None, 3],
        }
    )

    relation_instances_df = pd.DataFrame(
        {
            "RelationID": [1, 2],
            "Relation": ["borrows", "owns"],
            "R2Element": ["device", "hardware"],
        }
    )

    relations_df, relation_instances_df = _prepare_relation_targets(
        relations_df,
        relation_instances_df,
    )

    assert relations_df["R2Element"].tolist() == [
        "device",
        "hardware",
    ]

    assert relations_df["R2ElementID"].tolist() == [
        1,
        3,
    ]

    assert relation_instances_df["R2Element"].tolist() == [
        "device",
        "hardware",
    ]


def test_prepare_relation_targets_disambiguates_child_elements():
    """
    Prefixes coalesced child elements with the relation name
    when duplicates exist.
    """
    relations_df = pd.DataFrame(
        {
            "RelationID": [1, 2, 2],
            "Relation": ["borrows", "owns", "owns"],
            "R1Element": ["person", "person", "person"],
            "R2Element": ["hardware", "component", "component"],
            "R2ElementID": [1, 2, 2],
            "ChildR2Element": [None, "hardware", "software"],
            "ChildR2ElementID": [None, 3, 4],
        }
    )

    relation_instances_df = pd.DataFrame(
        {
            "RelationID": [1, 2, 2],
            "Relation": ["borrows", "owns", "owns"],
            "R2Element": ["hardware", "hardware", "software"],
        }
    )

    relations_df, relation_instances_df = _prepare_relation_targets(
        relations_df,
        relation_instances_df,
    )

    assert relations_df["R2Element"].tolist() == [
        "borrows_hardware",
        "owns_hardware",
        "owns_software",
    ]

    assert relations_df["R2ElementID"].tolist() == [1, 3, 4]

    assert relation_instances_df["R2Element"].tolist() == [
        "borrows_hardware",
        "owns_hardware",
        "owns_software",
    ]


def test_prepare_relation_targets_raises_on_duplicates():
    """Raises when disambiguation still produces duplicate target element names."""
    relations_df = pd.DataFrame(
        {
            "RelationID": [1, 2],
            "Relation": ["manages", "manages"],
            "R1Element": ["person", "person"],
            "R2Element": ["person", "person"],
            "R2ElementID": [1, 1],
            "ChildR2Element": [None, None],
            "ChildR2ElementID": [None, None],
        }
    )

    relation_instances_df = pd.DataFrame(
        {
            "RelationID": [1, 2],
            "Relation": ["manages", "manages"],
            "R2Element": ["person", "person"],
        }
    )

    with pytest.raises(RuntimeError):
        _prepare_relation_targets(relations_df, relation_instances_df)


def test_prepare_relation_targets_raises_on_duplicate_children():
    """Raises when duplicate child targets cannot be uniquely disambiguated."""
    relations_df = pd.DataFrame(
        {
            "RelationID": [1, 2, 2],
            "Relation": ["borrows", "borrows", "borrows"],
            "R1Element": ["person", "person", "person"],
            "R2Element": ["hardware", "component", "component"],
            "R2ElementID": [1, 2, 2],
            "ChildR2Element": [None, "hardware", "software"],
            "ChildR2ElementID": [None, 3, 4],
        }
    )

    relation_instances_df = pd.DataFrame(
        {
            "RelationID": [1, 2, 2],
            "Relation": ["borrows", "borrows", "borrows"],
            "R2Element": ["hardware", "hardware", "software"],
        }
    )

    with pytest.raises(RuntimeError):
        _prepare_relation_targets(relations_df, relation_instances_df)