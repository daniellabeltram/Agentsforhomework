# Expert Roles for a Penguin Random House M&A Application

> Companion to [penguin-random-house-research.md](./penguin-random-house-research.md).
> Lists the expertise needed to build an M&A decision-support application for Penguin Random House (PRH) executives. Most roles are part-time advisors or existing PRH staff, not full-time hires.
>
> The 15 most important roles are implemented as AI agents. See [`../agents/README.md`](../agents/README.md).

---

## 1. M&A and deal expertise (the core subject matter)

| Role | What they bring to the app |
|---|---|
| **Corporate development / M&A lead** (ideally a former corp-dev executive) | Defines the deal stages from sourcing to close, what executives need at each decision point, and what a good deal memo looks like. The most important advisor. |
| **Investment banker / M&A advisor** (ideally with publishing deals) | How targets are found and priced; how auctions and letters of intent work. Firms such as Oaklins DeSilva+Phillips and The Fisher Company advised sellers on recent PRH deals. |
| **Valuation / financial modeling expert** | Discounted cash flow, comparable deals, multiples, standalone value vs. value with synergies. Shapes the modeling engine. |
| **Deal strategy consultant** | Strategic fit: which categories and regions PRH should buy into, and how to score targets against that. |

## 2. Publishing industry expertise (what makes this PRH-specific)

| Role | Why PRH needs it |
|---|---|
| **Trade publishing executive** (has run an imprint P&L) | How a publisher really makes money: advances, returns, backlist vs. frontlist, bestseller dependence. |
| **Backlist / catalog valuation specialist** | PRH buys deep catalogs (Cherry Lake ~6,000 titles, Hay House ~1,500). Valuing evergreen titles is a specialty. |
| **Rights and licensing expert** | Audio, translation, film/TV and merchandise rights; critical for IP deals like BOOM! Studios. |
| **Royalties and author contracts specialist** | Royalty obligations, unearned advances and option clauses are hidden liabilities in every target. |
| **Distribution and supply chain expert** | Most synergies come from moving a target onto PRH distribution; distribution clients are also a pipeline of future targets. |
| **Sales channel expert** | Retail and Amazon, libraries and schools, direct-to-consumer: different value and risk. |
| **Audio publishing expert** | Audio is PRH's most consistent growth segment. |
| **International publishing advisors** | PRH buys in Spain/Latin America, Germany, the UK and Australia. |
| **Direct-to-consumer and community expert** | Values audience businesses like Wonderbly and She Reads Truth: subscribers, lifetime value, engagement. |

## 3. Legal and regulatory

| Role | Why |
|---|---|
| **Antitrust / competition counsel** | Critical for PRH: the DOJ blocked the Simon & Schuster deal over harm to author pay. The app should flag antitrust risk per target (US DOJ/FTC, EU, UK CMA). |
| **M&A transactional attorney** | Deal structures, LOIs, purchase agreements, diligence checklists. |
| **IP / copyright attorney** | Catalog ownership, chain of title, copyright terms, reversion clauses. |
| **Data privacy counsel** | DTC targets bring customer data under GDPR and US state privacy laws. |
| **Employment counsel** | Retaining key editors and founders; employee transfers, especially abroad. |
| **International / cross-border counsel** | Local rules and approvals in each country. |
| **Securities / confidentiality compliance** | Deal information is highly confidential and Bertelsmann issues public bonds; shapes access control in the app. |

## 4. Finance, accounting and tax

| Role | Why |
|---|---|
| **Financial due diligence / quality of earnings** | Separates real earnings from accounting adjustments. |
| **Acquisition accountant (IFRS 3 / purchase price allocation)** | Bertelsmann reports under IFRS; deal accounting affects reported profit. |
| **Tax structuring specialist** | Cross-border structure has a big effect on value. |
| **Treasury / FX specialist** | Exchange rates hurt PRH's 2026 results; many targets are outside the US. |
| **R&W insurance broker** (optional) | Common in mid-market deals; affects risk and pricing. |

## 5. Post-merger integration

| Role | Why |
|---|---|
| **Integration lead** | PRH's Acquisition Optimization and Integration team (Rachel Goldstein) does this; a design partner and primary user. |
| **Synergy tracking / finance analyst** | Promised vs. achieved synergies. |
| **HR / change management** | Retaining talent and preserving editorial independence, part of PRH's promise to sellers. |
| **IT / systems integration** | ERP, title management, ONIX metadata feeds, royalty systems. |

## 6. Analysts and data

| Role | Why |
|---|---|
| **Publishing market / industry analyst** | Category sizes and trends using data such as Circana BookScan. |
| **Data analyst / data scientist** | Target-scoring model; benchmarks targets against PRH titles. |
| **Competitive intelligence analyst** | Tracks deals by HarperCollins, Hachette, Simon & Schuster (KKR), Macmillan and private equity, plus independents that might sell. |
| **Data sourcing specialist** | PitchBook, Capital IQ, Tracxn, BookScan, Edelweiss, filings. |

## 7. Team that builds the app

| Role | Why |
|---|---|
| **Product manager** (finance/M&A exposure) | Turns expert knowledge into features and priorities. |
| **UX designer for executive dashboards** | One-page deal view, target comparison, invest-or-pass screens. |
| **Full-stack engineers** | Build the app. |
| **Data engineer** | Pipelines for market, sales and deal data. |
| **AI/ML engineer** | Document and contract analysis, scoring models. |
| **Security engineer** | Deal-room-grade security: per-deal access, audit logs, encryption. |
| **QA / testing** | Errors in financial models destroy executive trust. |

## 8. Stakeholders on PRH's side (users and approvers)

- **Executive sponsor:** CFO Manuel Sansigre or COO Jeff Abraham.
- **Division presidents and publishers:** originate most deals (e.g., Random House Children's Books with Cherry Lake).
- **Bertelsmann corporate M&A and finance:** approves large deals and the capital behind them.
- **Acquisition Optimization and Integration team:** power users.

---

## Minimum starting team

1. Product owner, with a part-time **corp-dev / M&A advisor**
2. **Publishing finance expert** (catalog value, royalties, imprint P&L)
3. **Data analyst** (scoring model, data sources)
4. **Antitrust and M&A counsel** on review
5. **UX designer** for executive dashboards
6. A **PRH design partner**, ideally from the integration team

---

## The 15 roles implemented as agents

| # | Agent | Covers |
|---|---|---|
| 1 | `corp-dev-lead` | Corporate development / M&A lead, deal strategy |
| 2 | `investment-banker` | Sourcing, process, pricing and negotiation |
| 3 | `valuation-modeler` | DCF, comps, synergy and returns modeling |
| 4 | `trade-publishing-exec` | Imprint P&L and publishing-program fit |
| 5 | `backlist-catalog-analyst` | Catalog and backlist valuation |
| 6 | `rights-licensing-expert` | Subsidiary rights, audio, translation, film/TV/IP |
| 7 | `royalties-contracts-specialist` | Author contracts, advances, royalty liabilities |
| 8 | `distribution-supply-chain-expert` | Distribution, channels, supply-chain synergies |
| 9 | `antitrust-counsel` | Competition law and regulatory risk |
| 10 | `ma-transaction-attorney` | Deal structure, LOI/SPA terms, legal diligence |
| 11 | `ip-copyright-attorney` | Chain of title, copyright, reversions, data privacy |
| 12 | `financial-due-diligence` | Quality of earnings, working capital, red flags |
| 13 | `tax-accounting-specialist` | Tax structuring, IFRS 3 purchase accounting, FX |
| 14 | `integration-lead` | Post-merger integration and synergy tracking |
| 15 | `market-intel-analyst` | Market sizing, competitive intelligence, target sourcing |

Roles left out of the agent set are either covered inside these 15 (deal strategy, channels, audio, international, data privacy, treasury) or are app-building roles (product, UX, engineering, security) rather than deal-decision roles.
