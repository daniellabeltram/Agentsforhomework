# PRH M&A Expert Agents

Fifteen specialist agents that act as a virtual deal team for Penguin Random House (PRH) executives evaluating acquisitions. Background: [`docs/penguin-random-house-research.md`](../docs/penguin-random-house-research.md) and [`docs/ma-expert-roles.md`](../docs/ma-expert-roles.md).

Each agent is generated in two formats from one source, [`build_agents.py`](./build_agents.py):

| Format | Location | Use it for |
|---|---|---|
| **Claude Code subagents** ([docs](https://code.claude.com/docs/en/sub-agents)) | [`.claude/agents/`](../.claude/agents/) | Working with the team interactively in Claude Code while you build the app |
| **Claude Managed Agents** ([docs](https://platform.claude.com/docs/en/managed-agents/overview)) | [`agents/managed/`](./managed/) | Calling the team from the M&A application itself through the Claude API |

## The 15 agents

| # | Agent | Role | Runs code |
|---|---|---|---|
| 1 | `corp-dev-lead` | Corporate development / M&A lead: deal thesis, go/no-go, IC memo, synthesis | |
| 2 | `investment-banker` | Sourcing, process strategy, bid tactics, LOI economics, comps | |
| 3 | `valuation-modeler` | DCF, comps, synergies, IRR, walk-away price | ✓ |
| 4 | `trade-publishing-exec` | Imprint P&L, list quality, fit inside a PRH division | |
| 5 | `backlist-catalog-analyst` | Title-level catalog valuation, decay curves | ✓ |
| 6 | `rights-licensing-expert` | Audio, translation, film/TV, IP and franchise value | |
| 7 | `royalties-contracts-specialist` | Advances, royalty liabilities, change-of-control and reversion clauses | ✓ |
| 8 | `distribution-supply-chain-expert` | Distribution, channel mix, supply-chain synergies | ✓ |
| 9 | `antitrust-counsel` | Competition-law risk, S&S precedent, merger filings | |
| 10 | `ma-transaction-attorney` | Structure, purchase agreement terms, legal diligence | |
| 11 | `ip-copyright-attorney` | Chain of title, copyright termination, AI rights, data privacy | |
| 12 | `financial-due-diligence` | Quality of earnings, working capital, debt-like items | ✓ |
| 13 | `tax-accounting-specialist` | Tax structure, IFRS 3 purchase price allocation, FX | ✓ |
| 14 | `integration-lead` | Day-1 / 100-day plans, synergy tracking, retention | |
| 15 | `market-intel-analyst` | Market sizing, target screening, competitor deals | ✓ |

Every agent shares the same PRH context (financials, leadership, deal history, playbook) and the same operating rules: separate facts from estimates, cite sources, keep deal information confidential, defer to licensed counsel, and answer in a fixed format (bottom line, key findings, risks, open questions, confidence).

## Run limits (guardrails against runaway agents)

Every agent belongs to a tier, with a few per-role overrides. The limits are set in `TIERS` in `build_agents.py`:

| Tier | Agents | Turn cap | Effort | Web searches | Page fetches | Session cap |
|---|---|---|---|---|---|---|
| Advisor | investment-banker, trade-publishing-exec, rights-licensing-expert, antitrust-counsel (8 searches / 5 fetches), ma-transaction-attorney, ip-copyright-attorney, integration-lead | 15 | medium | 6 | 4 | $3 |
| Modeler | valuation-modeler, backlist-catalog-analyst, royalties-contracts-specialist, distribution-supply-chain-expert, financial-due-diligence, tax-accounting-specialist | 25 | high | 8 | 6 | $6 |
| Researcher | market-intel-analyst; corp-dev-lead (20 turns, 10 searches, 6 fetches) | 30 | high | 15 | 10 | $8 |
| Coordinator | deal-team-lead: at most 5 specialists at once, 2 rounds each, 3 own searches | – | high | – | – | $30 shared |

How each limit is enforced:

- **Turn cap**: `maxTurns` in each Claude Code subagent. Claude Code stops the agent when it is reached.
- **Effort**: `effort` in Claude Code and on the Managed Agents model. Advisors run at `medium` to stay quick.
- **Search and fetch caps**: written into each agent's prompt as a "Work budget". When the agent hits a limit it must stop and return what it has, marked **PARTIAL**, with a list of gaps, instead of continuing to search.
- **Session cap (Managed Agents)**: a hard spend ceiling enforced by the platform. The app passes it as the session `budget` when it creates the session, using the amounts in `agents/managed/budgets.json`. At the cap the session pauses with `stop_reason: budget_reached`. It keeps its history and resumes if the cap is raised.
- **Coordinator limits**: written into `deal-team-lead`'s prompt. Dynamic workflows run only when the user explicitly asks for confirmatory diligence or a screen of more than five targets.
- **Output length**: about 1,200 words for specialists and 1,500 for the coordinator.

The search and fetch caps are prompt instructions: agents follow them reliably, but the platform doesn't enforce them. The turn caps (Claude Code) and the session spend caps (Managed Agents) are the hard backstops.

## Editing the agents

Edit `ROLES`, `PRH_CONTEXT` or `OPERATING_RULES` in `build_agents.py`, then regenerate both formats:

```bash
python3 agents/build_agents.py
```

Don't hand-edit the generated files; the next build overwrites them.

---

## Option A: Claude Code subagents

The files in `.claude/agents/` load automatically when you open this repository in Claude Code. Claude delegates to them based on each description, or you can ask for one by name:

```text
Use the antitrust-counsel agent to screen a potential acquisition of a mid-sized US romance publisher.
```

```text
Have the corp-dev-lead, valuation-modeler and integration-lead agents each assess Cherry Lake as if we were buying it today, then combine their views.
```

Run `/agents` in Claude Code to list, view or edit them. Research agents get read and web tools; agents marked "Runs code" also get `Bash`, `Write` and `Edit` so they can build models in Python.

## Option B: Claude Managed Agents (for the application)

Anthropic hosts the agent loop and a sandbox for each session. Managed Agents is in beta, bills session runtime on top of tokens, and keeps session history until you delete it.

```text
agents/managed/
├── agents/
│   ├── deal-team-lead.md          # coordinator; rosters the 15 specialists
│   └── <15 specialist files>.md   # frontmatter = agent config, body = system prompt
└── environments/
    └── prh-ma-research.yaml       # cloud sandbox, limited network allowlist
```

- **Model:** `claude-opus-5-5` at `high` effort.
- **Tools:** the built-in agent toolset with web search and web fetch on and an `auto` permission policy. Bash is off for agents that don't run code.
- **Coordinator:** `deal-team-lead` delegates to the 15 specialists and returns one investment-committee style recommendation. Dynamic workflows are **on**: for full diligence or screening many targets, it can run the specialists in parallel phases. That uses more tokens. To turn it off, set `workflows: {type: disabled}` in `build_agents.py` and rebuild.
- **Network:** the environment uses `limited` networking. The web tools reach only the publishing, regulator and reference sites listed in `ALLOWED_HOSTS`. Add hosts there when the team needs another source.

### Deploy

You need the [`ant` CLI](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/quickstart) 1.40.0 or later and a Claude API key (`ant auth login`). Run from `agents/managed/` so `claude-lock.json` lives there:

```bash
cd agents/managed
```

```bash
ant apply --dry-run -v agents environments
```

```bash
ant apply agents environments
```

`ant apply` creates the 16 agents and the environment and writes their IDs to `claude-lock.json`. Commit that file so later runs update the same agents instead of creating duplicates.

### Run a session from the app (Python)

```python
import json
import anthropic

lock = json.load(open("agents/managed/claude-lock.json"))["resources"]
agent_id = lock["./agents/deal-team-lead.md"]["id"]
env_id = lock["./environments/prh-ma-research.yaml"]["id"]

budgets = json.load(open("agents/managed/budgets.json"))
cap_cents = str(budgets["deal-team-lead"]["budget_usd"] * 100)  # "3000" = $30.00

client = anthropic.Anthropic()
session = client.beta.sessions.create(
    agent=agent_id,
    environment_id=env_id,
    title="First look: example target",
    # Hard spend cap: the session pauses with stop_reason "budget_reached" at the cap.
    budget={"type": "limit", "max_list_cost": {"amount": cap_cents, "currency": "USD"}},
)
client.beta.sessions.events.send(
    session_id=session.id,
    events=[{
        "type": "user.message",
        "content": [{"type": "text", "text": "Give me a first look at acquiring <target>. Here is what we know: ..."}],
    }],
)
```

To query one specialist directly, use that specialist's ID from `claude-lock.json` instead of the coordinator's. See the [Managed Agents docs](https://platform.claude.com/docs/en/managed-agents/overview) for streaming events and session budgets. Set a session budget whenever the coordinator runs workflows.

> These agents are decision-support tools. Legal, tax, accounting and antitrust output should be confirmed by PRH's counsel and advisors.
