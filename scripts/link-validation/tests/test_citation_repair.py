"""Regression tests for citation-repair.py confidence gating."""

from conftest import load_script

cr = load_script("citation-repair.py")


def test_wayback_of_original_keeps_high_confidence():
    repair = cr.CitationRepair()

    confidence = repair._cap_confidence(
        95,
        "https://example.com/dead/path",
        "https://web.archive.org/web/20250101000000/https://example.com/dead/path",
        "wayback",
        {},
        is_archived=True,
    )

    assert confidence == 95


def test_same_doi_resolution_keeps_high_confidence():
    repair = cr.CitationRepair()

    confidence = repair._cap_confidence(
        95,
        "https://publisher.example/article/10.1234/example.doi",
        "https://doi.org/10.1234/example.doi",
        "doi_resolution",
        {},
    )

    assert confidence == 95


def test_different_live_url_caps_high_confidence_with_empty_relevance():
    repair = cr.CitationRepair()

    confidence = repair._cap_confidence(
        95,
        "https://old.example/articles/dead",
        "https://new.example/articles/replacement",
        "alternative",
        {},
    )

    assert confidence == 90
