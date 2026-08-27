# Contributing

Thank you for helping improve **LLMs in Modern Agentic Systems: A Systems Survey**. Contributions should make the research map more accurate, more complete, or easier to navigate.

## What to submit

### Literature suggestions

Please provide:

- the paper title and stable URL;
- authors, year, and venue or repository;
- the proposed taxonomy locus;
- one or two sentences explaining the paper’s primary contribution;
- whether it changes the survey’s comparison, evidence, or conclusion.

A paper may span several layers, but Figure 2 assigns each representative work to one **primary locus**. Explain why your proposed locus is the best first location.

### Corrections

For a correction, identify the exact paper section, figure, table, bibliography key, literature-index entry, or webpage element. Include the current text, the proposed correction, and a source when the correction concerns an external fact.

### Pull requests

Keep changes narrow and auditable. Do not combine unrelated manuscript, bibliography, and website changes in one pull request.

- Edit bibliography metadata in `refs.bib` or `expanded-refs.bib`.
- Edit the Figure 2 taxonomy in `1-intro.tex`.
- Regenerate `LITERATURE.md` with `python3 scripts/generate_literature.py` after changing a mapped work or its metadata.
- Edit the deployed project hub in `docs/`.
- Preserve the terminology and operational taxonomy used by the current manuscript.

## Inclusion principles

The survey favors work that contributes at least one of the following:

- a clear system mechanism, architecture, or control pattern;
- comparative or benchmark evidence relevant to agentic systems;
- deployment evidence, failure analysis, or incident evidence;
- a security, governance, or interoperability standard with direct system implications;
- a survey that materially shapes the scope or taxonomy.

Citation count or popularity alone is not an inclusion criterion. Repository-only projects should have enough technical or empirical detail to support a specific claim.

## Research cutoff

The current manuscript’s research cutoff is **July 2026**. Later work may be proposed for the public resource hub, but it should not be represented as part of the frozen manuscript unless the paper itself is updated.

## Anonymized manuscript

Do not add or infer author identities while the manuscript remains anonymized. Citation metadata will be updated when the public preprint is released.
