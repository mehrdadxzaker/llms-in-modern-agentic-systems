# Personal-account transfer preparation

Staged destination: `mehrdadxzaker/llms-in-modern-agentic-systems`. Repository ID: `1348716372`.
Keep this draft unmerged until its separately approved cutover. This preparation
does not transfer anything or change live service settings, App ownership,
Apple identities, DNS, deployments, or billing.

## Prepared changes

The canonical/Open Graph URLs, GitHub metadata request, repository links,
current citation URL, LaTeX link macros, and literature/PDF-link generators
point to the personal account. Both editable website sources and their `docs/`
publication copies are updated. The paper text, external citations, published
PDF bytes, figures, and attribution are preserved.

## Later cutover

The future site is
`https://mehrdadxzaker.github.io/llms-in-modern-agentic-systems/`.
After the approved repository transfer, review/merge this branch and publish
with the existing main-only Pages workflow. Confirm the homepage, narrative,
paper download, metadata request, and citation links.

Old Pages addresses need separate hosting. The local handoff includes an
organization-root redirect bundle for both HTML pages and unchanged copies of
the published assets, including the PDF. This preserves old paper links without
rewriting the archived paper. Publish/review that bundle separately and verify
its PDF hash before cutover; do not recreate the old repository slug. Future
paper builds use the updated LaTeX/generator URLs. No paper is republished here.

## Validation

`python3 scripts/validate_site.py` verifies all four HTML source/publication
pages, anchors, and local assets. Check the canonical and metadata API owners
across the source copies, and compare the two published PDF hashes with main.
