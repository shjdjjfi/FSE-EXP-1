# N22: additional independent Django + OpenCode evidence (2026-11-18)

This addendum extends, and does not rewrite, the original N22 Open WebUI,
Drizzle, and Django 5.1.8 experiment files in this branch.

| Separate research suite | Independent upstream issue/project mechanisms | Primary distinct positive cases/conditions | Primary negative cases/conditions | Conclusion |
|---|---:|---:|---:|---|
| Original N22 [report](EXPERIMENT_REPORT.md) | Open WebUI, Drizzle ORM: 2 | 6 issue-derived conditions across 2 mechanisms | 6 | Contract detects 6/6; structural baselines 0/6; no demonstrated advantage over a fully asserted baseline |
| New [Django/OpenCode addendum](addenda/20261118_django_opencode/README.md) | Django, OpenCode: 2 | 2 historical failure inputs across 2 mechanisms | 13, plus 30 correlated legal data edits | Contract detects 2/2; 0/13 alarms; **full assertion baseline also detects 2/2** |

Across the two separate suites we now have real migration phenomena grounded
in public issue evidence from **four independent upstream projects**:
[Open WebUI](https://github.com/open-webui/open-webui/discussions/26635),
[Drizzle](https://github.com/drizzle-team/drizzle-orm/issues/5782),
[Django](https://code.djangoproject.com/ticket/36843), and
[OpenCode](https://github.com/anomalyco/opencode/issues/52226).

The suites use different case-selection rules, alternative-path semantics,
and comparison designs. **Do not combine the 6+2 positive conditions into an
eight-incident industrial recall estimate, or the 6+13+30 negatives into a
population false-positive rate.** Variants share mechanisms and scenarios
were selected retrospectively. In particular, no evidence supports a 5%
population false-positive guarantee.

The new dataset has 46 unique inputs, 138 observations, 123 verified
on-disk SQLite databases, 15 in-memory OpenCode observations, and 9 additional
baseline executions. Sources, hashes, raw-case summary, SQL evidence, and
an analysis unit test suite are in
[`addenda/20261118_django_opencode/`](addenda/20261118_django_opencode/README.md).
The versioned `observations.jsonl.gz` file carries compact original SQL/API
outputs; the complete ZIP with all raw SQLite files and log files was also
saved as a separate durable task artifact.

**Original stopping rule still fails.** Two or more distinct real defects are
now amply illustrated, but the additional suite establishes **0 percentage
points** of recall gain over a full baseline given the same data contracts.
There is still no blind industrial holdout, industrial ROI, or sufficiently
precise project-level false-positive estimate. See the follow-up
[study protocol](addenda/20261118_django_opencode/paper/NEXT_STUDY_PROTOCOL.md)
before proposing a method-efficacy submission.
