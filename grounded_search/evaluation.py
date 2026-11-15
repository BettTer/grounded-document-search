import json
from pathlib import Path
from statistics import mean, median
from time import perf_counter

from psycopg import Connection

from .search import search

CUTOFFS = (1, 3, 5)


def evaluate(connection: Connection, corpus_id: str, dataset: Path, match_mode: str) -> dict:
    cases = json.loads(dataset.read_text(encoding="utf-8"))
    indexed_ids = {
        evidence_id
        for (evidence_id,) in connection.execute(
            "SELECT evidence_id FROM evidence WHERE corpus_id = %s", (corpus_id,)
        )
    }
    if not indexed_ids:
        raise ValueError(f"No indexed evidence for {corpus_id}. Run index first.")

    reports = []
    for case in cases:
        expected = set(case["expected_evidence_ids"])
        unknown = sorted(expected - indexed_ids)
        if unknown:
            raise ValueError(f"{case['case_id']}: evidence not in the index: {', '.join(unknown)}")

        start = perf_counter()
        results = search(connection, corpus_id, case["question"]["en"], max(CUTOFFS), match_mode)
        latency_ms = (perf_counter() - start) * 1000
        returned = [hit["evidence_id"] for hit in results]
        metrics = {}
        if expected:
            for k in CUTOFFS:
                missing = expected - set(returned[:k])
                metrics[str(k)] = {
                    "recall": (len(expected) - len(missing)) / len(expected),
                    "all_evidence_found": not missing,
                    "missing_evidence_ids": sorted(missing),
                }

        reports.append({
            "case_id": case["case_id"],
            "tags": case["tags"],
            "expected_evidence_ids": case["expected_evidence_ids"],
            "retrieved_evidence_ids": returned,
            "metrics_at_k": metrics,
            "retrieval_ms": round(latency_ms, 3),
        })

    labeled = [report for report in reports if report["metrics_at_k"]]
    if not labeled:
        raise ValueError("Evaluation requires at least one case with expected evidence.")

    aggregate = {}
    for k in CUTOFFS:
        scores = [report["metrics_at_k"][str(k)] for report in labeled]
        aggregate[str(k)] = {
            "macro_recall": round(mean(score["recall"] for score in scores), 4),
            "all_evidence_found": sum(score["all_evidence_found"] for score in scores),
        }
    return {
        "corpus_id": corpus_id,
        "dataset": dataset.name,
        "postgres_version": connection.info.server_version,
        "match_mode": match_mode,
        "indexed_evidence_count": len(indexed_ids),
        "cases_with_expected_evidence": len(labeled),
        "cases_without_expected_evidence": len(reports) - len(labeled),
        "metrics_at_k": aggregate,
        "median_retrieval_ms": round(median(report["retrieval_ms"] for report in reports), 3),
        "cases": reports,
    }
