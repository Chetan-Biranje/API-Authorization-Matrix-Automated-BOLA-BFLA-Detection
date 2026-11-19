# Research results

Run on 2026-11-20, scanner at this commit, local API on 127.0.0.1:8000.
3 roles x 3 endpoints, 10 generated cases.

| Mode | Cases | Findings | Time |
|---|---|---|---|
| Secure | 10 | 0 | ~0.26 s |
| `LAB_VULNERABLE=1` | 10 | 3 (1 BOLA, 2 BFLA) | ~0.26 s |

Seeded flaws: BOLA on `GET /users/{id}` for `user`; BFLA on `GET /admin/users` for
`user` and `manager`. All three were found and nothing else was flagged, so on this
sample there were no false positives and no false negatives.

## What this does and does not show

It shows that case generation, execution and classification work end to end. It does not
show detection accuracy: the sample is tiny, the flaws are the obvious kind, and the
author wrote both the app and the scanner. The next step is more endpoints, write
methods, and flaws that are less direct (for example a check that only covers one HTTP
method).

## Bug found while writing this

The first run labelled the BOLA case as `BFLA`, because every `DENY` that was allowed
was classified as function-level. Fixed in `scanner/analyzer.py` and covered by
`tests/scanner/test_analyzer.py`.
