ADAPTER_PROFILE = """## AMO Operating Contract

Authority order: source code > git history > `.ai/` canonical memory > `.ai/machine/` indexes > `.ai/packs/` > adapters > `.ai/runtime/` > chat.

- Preflight: `amo preflight --task "<task>"` before work.
- Expand only from pack pointers when evidence is missing; do not read the whole repository by default.
- Handoff: run `amo handoff --task "<task>" --summary "<state and next step>"` when context degrades.
- Degradation signals: repeated work, lost decisions or test plan, edits outside scope, or growing dependence on chat history.
- Postflight: run `amo postflight --task "<task>" --summary "<what changed>"` after project state changes.
- Validate with `ruff check .`, `pytest`, and `amo validate --strict` as applicable.
- `.ai/runtime/` is disposable and must remain gitignored; never promote runtime notes over repository truth.
"""
