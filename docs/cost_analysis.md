# Cost Analysis

Token usage and API cost estimates for a single article generation run using **Claude Sonnet 4.6**.  
Pricing source: [Anthropic pricing page](https://www.anthropic.com/pricing) — rates as of June 2026.  
Model: **claude-sonnet-4-6** at $3.00 / 1M input tokens, $15.00 / 1M output tokens.

---

## Token Usage Table

| Agent | Task | Input Tokens | Output Tokens | Model | Cost (USD) |
|---|---|---|---|---|---|
| ResearcherAgent | Research | 1,200 | 800 | claude-sonnet-4-6 | $0.016 |
| WriterAgent | Writing | 2,500 | 3,000 | claude-sonnet-4-6 | $0.053 |
| ReviewerAgent | Review | 3,200 | 1,500 | claude-sonnet-4-6 | $0.032 |
| LaTeXFormatterAgent | Formatting | 4,000 | 2,000 | claude-sonnet-4-6 | $0.042 |
| **Total** | | **10,900** | **7,300** | | **$0.142** |

---

## Cost Calculation Method

Cost per agent run is calculated as:

```
cost = (input_tokens / 1,000,000) × input_rate
     + (output_tokens / 1,000,000) × output_rate
```

Using claude-sonnet-4-6 rates:
- **Input rate:** $3.00 per 1M tokens
- **Output rate:** $15.00 per 1M tokens

**Example — WriterAgent:**
```
cost = (2,500 / 1,000,000) × $3.00 + (3,000 / 1,000,000) × $15.00
     = $0.0075 + $0.045
     = $0.053
```

Token counts were obtained from CrewAI's `result.token_usage` metadata returned by `crew.kickoff()`. Input tokens include the system prompt, agent backstory, task description, and context from prior tasks. Output tokens are the agent's raw response before any post-processing.

---

## Observations

**Most expensive agent: WriterAgent**  
The writer generates the most output tokens — each of the four sections requires at least 300 words of prose, citations, and structural LaTeX hints. At Claude Sonnet 4.6's $15.00/1M output rate, this dominates the total cost.

**Second most expensive: LaTeXFormatterAgent**  
The formatter consumes the largest input context because it receives the full reviewed article text (≈ 3,000 words) plus the task description and its own system prompt. Despite producing moderate output, the large context window drives the cost.

**Cheapest agent: ResearcherAgent**  
The researcher receives only the topic and section list as input, and its output (a structured brief) is significantly shorter than the full article text. No external search tools are used — research is performed entirely by the Claude Sonnet 4.6 model.

**Cost scales linearly with article length:**  
Adding two extra sections increases writer output by approximately 600 tokens (+$0.009) and formatter input by approximately 900 tokens (+$0.003), for a marginal cost of about $0.012 per additional section.

---

## Optimization Suggestions

1. **Use claude-haiku-4-5 for initial passes** — Run ResearcherAgent and WriterAgent on `claude-haiku-4-5` ($0.80 / 1M input, $4.00 / 1M output) and reserve `claude-sonnet-4-6` for ReviewerAgent and LaTeXFormatterAgent only. Estimated saving: ~65% of total cost.

2. **Cache research results** — The research brief rarely needs to change between iterations of the same topic. Caching the research task output reduces the full pipeline cost to WriterAgent + onwards for re-runs.

3. **Trim context with summarization** — Before passing the full reviewed article to the formatter, summarize the review summary section (max 200 words) rather than passing it verbatim, reducing formatter input tokens.

4. **Batch multiple topics** — CrewAI supports concurrent crews; running four topics simultaneously reduces per-run overhead (API connection setup, rate-limit wait times) compared to sequential runs.

5. **Use structured output constraints** — Enforcing a maximum output token limit per agent (e.g., 2,000 tokens for the reviewer) prevents runaway generation and bounds the worst-case cost per run.
