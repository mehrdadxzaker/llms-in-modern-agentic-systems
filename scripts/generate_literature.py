#!/usr/bin/env python3
"""Generate the public Figure 2 literature index from the paper bibliography."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CATEGORIES = [
    (
        "Foundations and scope",
        [
            (
                "Cross-cutting surveys",
                "Broad surveys that establish the scope of agents, RAG, memory, tool learning, evaluation, and self-improvement.",
                "wang2024autonomousagentssurvey xi2025agentsurvey plaat2025agenticllms ren2026selfimprovingagents gao2023ragsurvey singh2025agenticragsurvey zhang2025memorysurvey shi2025toollearning yehudai2026agentsurveyeval".split(),
            ),
            (
                "Classical and language-model foundations",
                "Classical agency, planning, hierarchical control, multi-agent systems, cognitive analogies, transformers, and few-shot language models.",
                "russell2021aima rao1995bdi wooldridge2009multiagent kaelbling1998pomdp sutton1999options fikes1971strips erol1994htn mcdermott1998pddl hawkins2021thousandbrains vaswani2017attention brown2020language".split(),
            ),
        ],
    ),
    (
        "Grounding and action",
        [
            (
                "Retrieval and grounding",
                "Canonical, adaptive, corrective, and self-reflective retrieval; query rewriting, pseudo-documents, reranking, context structure, and RAG evaluation.",
                "lewis2020rag ghodratnama2024adapting ma2023queryrewriting wang2023query2doc shi2023replug jiang2023flare asai2024selfrag sarthi2024raptor yan2024crag es2024ragas liu2024lostinthemiddle".split(),
            ),
            (
                "Reasoning and planning",
                "ReAct, branching search, least-to-most decomposition, plan-and-solve, program-of-thought, self-refinement, tool routing, and plan-and-act control.",
                "yao2023react yao2023treeofthoughts zhou2023leasttomost wang2023planandsolve chen2023pot madaan2023selfrefine karpas2022mrkl erdogan2025planandact".split(),
            ),
            (
                "Tools and action runtime",
                "Web interaction, learned tool use, tool-use datasets, function-calling evaluation, and production agent runtimes.",
                "nakano2021webgpt schick2023toolformer qin2024toolllm openai2025agentssdk patil2025bfcl".split(),
            ),
        ],
    ),
    (
        "State, adaptation, and coordination",
        [
            (
                "Memory and persistent state",
                "Generative, hierarchical, conversational, experiential, structured, and learned memory policies, together with memory benchmarks.",
                "park2023generativeagents packer2024memgpt zhong2024memorybank zhao2024expel xu2025amem chhikara2025mem0 yu2026agemem ghodratnama2023personalized ghodratnama2024sumrecom tan2025membench shen2026mem2actbench".split(),
            ),
            (
                "Self-improvement and long horizons",
                "Verbal reflection, program or library growth, embodied exploration, weak-to-strong feedback, and agentic reinforcement learning.",
                "shinn2023reflexion gao2023pal wang2023voyager li2026soar lu2026supo zakershahrak2024explanation".split(),
            ),
            (
                "Coordination and protocols",
                "Role-play, conversational coordination, software-development teams, multi-agent debate, benchmarked coordination, MCP, and A2A.",
                "li2023camel wu2023autogen hong2024metagpt du2024multiagentdebate zhu2025multiagentbench mcp2025spec a2a2026spec".split(),
            ),
        ],
    ),
    (
        "Evaluation and evidence",
        [
            (
                "Benchmark frameworks",
                "Breadth-oriented agent environments, progress-sensitive boards, and multimodal general-assistant evaluation.",
                "liu2024agentbench hsieh2024agentboard mialon2024gaia".split(),
            ),
            (
                "Interactive environments",
                "Web, desktop, human-executed computer use, long-horizon operating-system tasks, enterprise work, and controllable app worlds.",
                "zhou2024webarena xie2024osworld abhyankar2025osworldhuman yuan2026osworld2 drouin2024workarena trivedi2024appworld".split(),
            ),
            (
                "Code, tool, science, and long-horizon tests",
                "Repository repair, software agents, tool-agent-user interaction, scientific discovery, data-driven science, full-agency episodes, and benchmark auditing.",
                "jimenez2024swebench yang2024sweagent yao2024taubench jansen2024discoveryworld chen2025scienceagentbench li2026agencybench openai2026swebenchaudit".split(),
            ),
        ],
    ),
    (
        "Assurance and deployment",
        [
            (
                "Security and governance",
                "Prompt injection, controlled attack benchmarks, agent-security evaluation, trustworthy web interaction, NIST guidance, OWASP, and MITRE ATLAS.",
                "greshake2023promptinjection zhan2024injecagent zhang2024agentsecuritybench levy2026stwebagentbench nist2023airmf nist2024genaiprofile owasp2025llmtop10 mitre2026atlas".split(),
            ),
            (
                "Application evidence",
                "Verified mathematical search, autonomous materials synthesis, chemistry tooling, automated research, multi-agent scientific work, and consequential office workflows.",
                "romeraparedes2024funsearch szymanski2023alab bran2024chemcrow lu2024aiscientist ghafarollahi2024sciagents xu2025agentcompany".split(),
            ),
        ],
    ),
]


def read_balanced(text: str, start: int, opener: str, closer: str) -> tuple[str, int]:
    depth = 0
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == opener:
            depth += 1
        elif char == closer:
            depth -= 1
            if depth == 0:
                return text[start + 1 : index], index + 1
    raise ValueError("Unbalanced BibTeX value")


def parse_fields(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    position = 0
    while position < len(body):
        match = re.search(r"([A-Za-z][A-Za-z0-9_-]*)\s*=\s*", body[position:])
        if not match:
            break
        name = match.group(1).lower()
        value_start = position + match.end()
        if body[value_start] == "{":
            value, position = read_balanced(body, value_start, "{", "}")
        elif body[value_start] == '"':
            value, position = read_balanced(body, value_start, '"', '"')
        else:
            end = body.find(",", value_start)
            if end == -1:
                end = len(body)
            value, position = body[value_start:end].strip(), end
        fields[name] = value.strip()
    return fields


def parse_bibliography(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    entries: dict[str, dict[str, str]] = {}
    position = 0
    pattern = re.compile(r"@([A-Za-z]+)\s*\{\s*([^,\s]+)\s*,")
    while match := pattern.search(text, position):
        body, position = read_balanced(text, text.find("{", match.start()), "{", "}")
        key, _, fields_body = body.partition(",")
        entries[key.strip()] = {"type": match.group(1).lower(), **parse_fields(fields_body)}
    return entries


def clean_tex(value: str) -> str:
    replacements = {
        r"\&": "&",
        r"\%": "%",
        r"\_": "_",
        "--": "–",
        r"\textendash": "–",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    value = re.sub(r"\\(?:textit|textbf|emph|mathrm|operatorname)\s*\{([^{}]*)\}", r"\1", value)
    value = value.replace("{", "").replace("}", "")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def entry_url(entry: dict[str, str]) -> str | None:
    if entry.get("url"):
        return clean_tex(entry["url"])
    if entry.get("doi"):
        return f"https://doi.org/{clean_tex(entry['doi'])}"
    eprint = entry.get("eprint")
    if eprint:
        return f"https://arxiv.org/abs/{clean_tex(eprint)}"
    arxiv = re.search(r"arXiv(?::| preprint arXiv:)(\d{4}\.\d{4,5})", entry.get("journal", ""), re.I)
    return f"https://arxiv.org/abs/{arxiv.group(1)}" if arxiv else None


def markdown_entry(key: str, entry: dict[str, str]) -> str:
    title = clean_tex(entry.get("title", key)).replace("|", r"\|")
    url = entry_url(entry)
    title_cell = f"[{title}]({url})" if url else title
    year = clean_tex(entry.get("year", "—"))
    venue = clean_tex(entry.get("booktitle") or entry.get("journal") or entry.get("howpublished") or "—")
    venue = venue.replace("|", r"\|")
    return f"| {year} | {title_cell} | {venue} | `{key}` |"


def main() -> None:
    entries: dict[str, dict[str, str]] = {}
    for bib_path in (ROOT / "refs.bib", ROOT / "expanded-refs.bib"):
        entries.update(parse_bibliography(bib_path))

    mapped_keys = [key for _, loci in CATEGORIES for _, _, keys in loci for key in keys]
    if len(mapped_keys) != 98 or len(set(mapped_keys)) != 98:
        raise SystemExit(f"Expected 98 unique atlas keys, found {len(mapped_keys)} entries and {len(set(mapped_keys))} unique keys")
    missing = [key for key in mapped_keys if key not in entries]
    if missing:
        raise SystemExit(f"Missing bibliography entries: {', '.join(missing)}")

    lines = [
        "<!-- Generated by scripts/generate_literature.py; edit the source taxonomy or bibliography instead. -->",
        "# Literature index",
        "",
        "This index accompanies **LLMs in Modern Agentic Systems: A Systems Survey**. It follows Figure 2 and assigns **98 representative works** to one primary locus. The full survey cites **222 sources**; placement here identifies a work’s principal contribution, not an exclusive category.",
        "",
        "[Project page](https://xpounder-com.github.io/llms-in-modern-agentic-systems/) · [Paper PDF](https://xpounder-com.github.io/llms-in-modern-agentic-systems/llms-in-modern-agentic-systems.pdf) · [Complete bibliography](refs.bib) · [Additional bibliography](expanded-refs.bib)",
        "",
        "## Contents",
        "",
    ]
    for branch, _ in CATEGORIES:
        anchor = branch.lower().replace(",", "").replace(" ", "-")
        lines.append(f"- [{branch}](#{anchor})")

    for branch, loci in CATEGORIES:
        lines.extend(["", f"## {branch}", ""])
        for locus, description, keys in loci:
            lines.extend(
                [
                    f"### {locus}",
                    "",
                    description,
                    "",
                    "| Year | Work | Venue or source | BibTeX key |",
                    "| --- | --- | --- | --- |",
                ]
            )
            lines.extend(markdown_entry(key, entries[key]) for key in keys)
            lines.append("")

    lines.extend(
        [
            "## Corrections and additions",
            "",
            "Use the repository issue templates to suggest a missing work, report metadata, or challenge a taxonomy placement. See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.",
            "",
        ]
    )
    (ROOT / "LITERATURE.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
