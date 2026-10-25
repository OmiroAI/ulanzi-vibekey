# Kodi development

Kodi uses an isolated canonical clone, a sandboxed coding worker, offline QA on
an independent host, different-model review, GitHub `kodi-tests`, and human PR
approval. Credentials, production services, device access and deployment authority
are not provided to workers. Repository tasks can be filed as GitHub issues with
the `kodi:ready` label after this onboarding PR and the coordinator update merge.

Run `python .kodi/qa.py` for the baseline gate. Install pytest and PyYAML first;
the Astro profile also needs `npm ci` with Node 24. Hardware profiles validate
Python syntax plus a `tests/` suite when present; they do not prove USB, Bluetooth,
Wi-Fi or firmware behavior. Add deterministic unit tests for behavior changes and
include manual bench instructions in the PR. Kodi does not flash devices or deploy.

Automatic merging remains disabled for newly onboarded repositories. Website
main branches already deploy through their existing workflows: human approval
and the existing release process remain required.
