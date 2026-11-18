#!/usr/bin/env python3
"""Aggregate actual historic GitHub lockfile replay, no false incident labels."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from analyze import wilson


def summarize(paths: list[Path]) -> dict:
    cells, sources, errors = [], [], []
    for p in paths:
        fp = p / "runs.json" if p.is_dir() else p
        if not fp.is_file():
            errors.append(f"Missing {fp}")
            continue
        data = json.loads(fp.read_text(encoding="utf-8"))
        os_name = data.get("host", {}).get("os", "unknown")
        sources.append({"file": str(fp), "runner_os": os_name,
                        "run": data.get("github_run_id"),
                        "replay_errors": data.get("errors", [])})
        for row in data.get("results", []):
            for family, obs in row.get("per_parent", {}).items():
                cells.append({"source": str(fp), "project": row["project"],
                              "git_sha": row["commit"], "os": os_name,
                              "family": family, "strategy": row["strategy"],
                              "ci_ok": row["npm_ci"]["returncode"] == 0,
                              "ci_peer_fallback": row.get("ci_peer_fallback", False),
                              "treatment_peer_fallback": row.get("treatment_peer_fallback", False),
                              "loader_ok": obs["native_execution_ok"],
                              "host_missing": obs["coverage"]["host_missing"] if obs.get("coverage") else None,
                              "version_churn": row["comparison"]["changed_non_target_versions"] if row.get("comparison") else None,
                              "treatment_seconds": row["treatment"]["seconds"]})
    groups = {}
    for x in cells:
        groups.setdefault(x["strategy"], []).append(x)
    summary = {}
    for strategy, rows in sorted(groups.items()):
        n = len(rows)
        good = sum(x["loader_ok"] for x in rows)
        summary[strategy] = {"n_package_host_cells": n,
                             "native_loader_success_n": good,
                             "native_loader_success_rate": round(good / n, 4) if n else None,
                             "wilson_95_ci": wilson(good, n),
                             "npm_ci_success_n": sum(x["ci_ok"] for x in rows),
                             "npm_ci_legacy_peer_fallback_n": sum(x["ci_peer_fallback"] for x in rows),
                             "treatment_legacy_peer_fallback_n": sum(x["treatment_peer_fallback"] for x in rows),
                             "non_target_version_churn_total": sum(x["version_churn"] or 0 for x in rows)}
    pair_index = {}
    for c in cells:
        pair_index.setdefault((c["source"], c["project"], c["family"], c["os"]), {})[c["strategy"]] = c
    pairs = []
    for key, variants in sorted(pair_index.items()):
        if "unmodified" not in variants:
            continue
        unmodified = variants["unmodified"]
        for method in ("npm11-in-place", "npm12-in-place", "strict-donor", "clean-regenerate"):
            if method not in variants:
                continue
            b = variants[method]
            pairs.append({"source": key[0], "project": key[1], "family": key[2], "host": key[3],
                          "strategy": method, "from_failed_to_working": not unmodified["loader_ok"] and b["loader_ok"],
                          "baseline_loader_ok": unmodified["loader_ok"],
                          "strategy_loader_ok": b["loader_ok"],
                          "non_target_version_churn": b["version_churn"]})
    return {"scope": "three public project locks pinned to immutable commits, replayed today; NOT natural CI failure logs",
            "n_files": len(sources), "n_project_host_parent_cells": len(pair_index),
            "sources": sources, "errors": errors, "strategy_summary": summary,
            "paired_comparisons": pairs, "all_cells": cells,
            "caveats": ["Project sampling was conditioned on finding a missing lock entry in the exploratory audit",
                        "Native dependency execution was tested; original project build/test and historical CI logs were not",
                        "Ignoring lifecycle scripts prevents unsafe arbitrary install-time execution but changes full-project behavior",
                        "Legacy-peer-deps retries are separately labeled and cannot be equated with default npm ci",
                        "Package families within a single project/host are correlated; descriptive rates are not ecosystem estimates"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+", type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    data = summarize(args.inputs)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"n_files": data["n_files"], "n_cells": data["n_project_host_parent_cells"],
                      "strategies": data["strategy_summary"], "errors": data["errors"]}, indent=2))


if __name__ == "__main__":
    main()
