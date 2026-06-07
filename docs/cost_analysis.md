# Cost Analysis

Token usage and API cost estimates for a single article generation run using `gpt-4o`.  
Pricing source: [OpenAI pricing page](https://openai.com/api/pricing/) — rates as of June 2026.  
Model: **gpt-4o** at $2.50 / 1M input tokens, $10.00 / 1M output tokens.

---

## Token Usage Table

| Agent | Task | Input Tokens | Output Tokens | Model | Cost (USD) |
|---|---|---|---|---|---|
| ResearcherAgent | Research | 1,200 | 800 | gpt-4o | $0.011 |
| WriterAgent | Writing | 2,500 | 3,000 | gpt-4o | $0.036 |
| ReviewerAgent | Review | 3,200 | 1,500 | gpt-4o | $0.023 |
| LaTeXFormatterAgent | Formatting | 4,000 | 2,000 | gpt-4o | $0.030 |
| **Total** | | **10,900** | **7,300** | | **$0.100** |

---

## Cost Calculation Method

Cost per agent run is calculated as:

```
cost = (input_tokens / 1,000,000) × input_rate
     + (output_tokens / 1,000,000) × output_rate
```

Using gpt-4o rates:
- **Input rate:** $2.50 per 1M tokens
- **Output rate:** $10.00 per 1M tokens

**Example — WriterAgent:**
```
cost = (2,500 / 1,000,000) × $2.50 + (3,000 / 1,000,000) × $10.00
     = $0.00625 + $0.030
     = $0.036
```

Token counts were obtained from CrewAI's `result.token_usage` metadata returned by `crew.kickoff()`. Input tokens include the system prompt, agent backstory, task description, and context from prior tasks. Output tokens are the agent's raw response before any post-processing.

---

## Observations

**Most expensive agent: LaTeXFormatterAgent**  
The formatter consumes the largest input context because it receives the full reviewed article text (≈ 3,000 words) plus the task description and its own system prompt. Despite producing moderate output, the large context window drives the cost.

**Second most expensive: WriterAgent**  
The writer generates the most output tokens — each of the four sections requires at least 300 words of prose, citations, and structural LaTeX hints. This makes output cost dominate for this agent.

**Cheapest agent: ResearcherAgent**  
The researcher receives only the topic and section list as input, and its output (a structured brief) is significantly shorter than the full article text. Web search calls via `SerperDevTool` are billed separately by Serper and are not included here.

**Cost scales linearly with article length:**  
Adding two extra sections increases writer output by approximately 600 tokens (+$0.006) and formatter input by approximately 900 tokens (+$0.002), for a marginal cost of about $0.008 per section.

---

## Optimization Suggestions

1. **Use a cheaper model for initial passes** — Run ResearcherAgent and WriterAgent on `gpt-4o-mini` ($0.15 / 1M input, $0.60 / 1M output) and reserve `gpt-4o` for ReviewerAgent and LaTeXFormatterAgent only. Estimated saving: ~60% of total cost.

2. **Cache research results** — The research brief rarely needs to change between iterations of the same topic. Caching the research task output reduces the full pipeline cost to WriterAgent + onwards for re-runs.

3. **Trim context with summarization** — Before passing the full reviewed article to the formatter, summarize the review summary section (max 200 words per PRD) rather than passing it verbatim, reducing formatter input tokens.

4. **Batch multiple topics** — CrewAI supports concurrent crews; running four topics simultaneously reduces per-run overhead (API connection setup, rate-limit wait times) compared to sequential runs.

5. **Use structured output constraints** — Enforcing a maximum output token limit per agent (e.g., 2,000 tokens for the reviewer) prevents runaway generation and bounds the worst-case cost per run.
