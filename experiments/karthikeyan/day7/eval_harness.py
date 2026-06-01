from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any


DAY6_PATH = Path(__file__).resolve().parent.parent / "day6"
sys.path.insert(0, str(DAY6_PATH))

from extract_compliance import extract_compliance, configure_gemini  # type: ignore


RULE_ID_WEIGHT = 0.4
STATUS_WEIGHT = 0.3
EVIDENCE_WEIGHT = 0.2
CONFIDENCE_WEIGHT = 0.1


def load_golden_set(file_path: Path) -> list[dict[str, Any]]:
    entries = []

    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                entries.append(json.loads(line))

    return entries


def normalize_quotes(quotes: list[str]) -> set[str]:
    return {
        quote.strip().lower()
        for quote in quotes
        if quote.strip()
    }


def jaccard_similarity(
    expected_quotes: list[str],
    actual_quotes: list[str],
) -> float:
    expected = normalize_quotes(expected_quotes)
    actual = normalize_quotes(actual_quotes)

    if not expected and not actual:
        return 1.0

    union = expected | actual

    if not union:
        return 0.0

    intersection = expected & actual

    return len(intersection) / len(union)


def score_case(expected: dict[str, Any], actual: Any) -> dict[str, float]:
    rule_score = 1.0 if actual.rule_id == expected["rule_id"] else 0.0
    status_score = 1.0 if actual.status == expected["status"] else 0.0

    evidence_score = jaccard_similarity(
        expected["evidence_quotes"],
        actual.evidence_quotes,
    )

    confidence_score = (
        1.0
        if abs(actual.confidence - expected["confidence"]) <= 0.2
        else 0.0
    )

    total_score = (
        rule_score * RULE_ID_WEIGHT
        + status_score * STATUS_WEIGHT
        + evidence_score * EVIDENCE_WEIGHT
        + confidence_score * CONFIDENCE_WEIGHT
    )

    return {
        "rule_id_score": rule_score,
        "status_score": status_score,
        "evidence_score": round(evidence_score, 3),
        "confidence_score": confidence_score,
        "total_score": round(total_score, 3),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate ComplianceCheck extraction against golden_set.jsonl"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional number of cases to run. Use --limit 2 for smoke test.",
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=7.0,
        help="Delay in seconds between model calls to avoid rate limits.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    configure_gemini()

    golden_file = Path(__file__).resolve().parent / "golden_set.jsonl"
    dataset = load_golden_set(golden_file)

    if args.limit is not None:
        dataset = dataset[: args.limit]

    results = []

    print("\nEVALUATION RESULTS")
    print("=" * 70)
    print(
        f"{'#':<3}"
        f"{'rule_id':<10}"
        f"{'status':<10}"
        f"{'evidence':<10}"
        f"{'conf':<10}"
        f"{'total':<10}"
    )
    print("-" * 70)

    for index, item in enumerate(dataset, start=1):
        expected = item["expected"]

        try:
            actual = extract_compliance(item["input"])
            scores = score_case(expected, actual)

            print(
                f"{index:<3}"
                f"{scores['rule_id_score']:<10.2f}"
                f"{scores['status_score']:<10.2f}"
                f"{scores['evidence_score']:<10.2f}"
                f"{scores['confidence_score']:<10.2f}"
                f"{scores['total_score']:<10.3f}"
            )

            results.append(
                {
                    "case_number": index,
                    "input": item["input"],
                    "expected": expected,
                    "actual": actual.model_dump(),
                    **scores,
                    "error": "",
                }
            )

        except Exception as error:
            print(
                f"{index:<3}"
                f"{0.0:<10.2f}"
                f"{0.0:<10.2f}"
                f"{0.0:<10.2f}"
                f"{0.0:<10.2f}"
                f"{0.0:<10.3f}"
            )

            results.append(
                {
                    "case_number": index,
                    "input": item["input"],
                    "expected": expected,
                    "actual": None,
                    "rule_id_score": 0.0,
                    "status_score": 0.0,
                    "evidence_score": 0.0,
                    "confidence_score": 0.0,
                    "total_score": 0.0,
                    "error": str(error),
                }
            )

        if index < len(dataset):
            time.sleep(args.delay)

    overall_score = round(
        sum(result["total_score"] for result in results) / len(results),
        3,
    )

    passed_cases = sum(
        1 for result in results if result["total_score"] >= 0.8
    )

    print("\nOVERALL SCORE")
    print("=" * 70)
    print(f"Score: {overall_score}")
    print(f"Cases >= 0.8: {passed_cases}/{len(results)}")

    output_file = Path(__file__).resolve().parent / "eval_results.json"
    output_file.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\nSaved results to eval_results.json")


if __name__ == "__main__":
    main()