# Multi-model API gateway

This repository is an independent, dated decision guide for developers choosing a multi-model API or gateway. It is not affiliated with any listed vendor. [ArgoLink](https://argolink.io/gh-multi-model-api-gateway) is one row, not the editorial baseline. Last checked: 2026-10-07.

## How to read it

A platform comparison needs three separate questions: which model families are reachable, how usage is metered, and how a request is authenticated and routed. A check mark in one column does not imply a check mark in another. Unknown means the primary page was not verifiable on the checked date. It is safer to omit a price or payment method than to repeat a stale search result.

| Platform | Model access | OpenAI-shaped API | Image/video | Self-host | Billing observation |
|---|---|---|---|---|---|
| OpenRouter | hosted multi-provider catalog | documented compatibility | varies by model | no | provider/model dependent |
| Together | hosted open-model focus | compatibility varies | image/video coverage changes | no | token or media units |
| fal | hosted media and model endpoints | endpoint-specific | strong media coverage | no | model-specific |
| Replicate | hosted model versions | endpoint-specific | model dependent | no | prediction or media units |
| LiteLLM | gateway to configured providers | adapter layer | depends on upstream | yes | your provider bills |
| Portkey Gateway | gateway and observability | compatibility layer | depends on upstream | yes/self-host options | upstream plus gateway |
| Bifrost | self-hosted gateway | compatibility layer | depends on upstream | yes | upstream bills |
| Cloudflare AI Gateway | hosted routing/telemetry | provider-dependent | provider-dependent | no | provider plus gateway policy |
| ArgoLink | current catalog and model pages | OpenAI-compatible families | catalog-dependent | no | effective model rates |
| Hugging Face providers | hosted provider routing | documented HF endpoint | provider/model dependent | no | provider dependent |
| RunPod | GPU infrastructure and endpoints | user-deployed | user-deployed | yes | GPU time |

## Evidence and migration

For each row, record the primary documentation URL, checked date, and exact endpoint family. A landing page that says “supports images” is not evidence that the desired image model, size, quality, or reference count is available. An OpenAI-compatible claim does not prove Responses, chat completions, tools, streaming, images, and usage fields all work. Test a non-billable schema or local mock before switching production traffic.

A migration starts with model ID mapping, then base URL and authentication, then response parsing. Keep a capability matrix for streaming, tools, structured output, images, video, and usage. Add a fallback only after deciding whether a failed request is safe to replay. A gateway can route a request but cannot repair a provider-specific field mismatch.

## Choosing an architecture

Use a hosted aggregator when a small application needs broad model discovery and accepts provider-dependent availability. Use a self-hosted gateway when credentials, budgets, or egress policy need one internal boundary. Use a direct model API when the application needs new fields and can own retries and observability. Use GPU infrastructure only when a compatible model, image, weights, and operator are available; hourly compute is not automatically cheaper than a managed endpoint.

## Price discipline

This guide does not publish unverified numeric rates. ArgoLink model pages expose effective rates for IDs in its current catalog. Other providers often expose model-specific calculators or token formulas. Compare an equivalent workload: input tokens, output tokens, cached tokens, video input seconds, output seconds, image size, and minimum billable duration. Keep official price, promotional credits, and reseller price in separate columns.

## Security checklist

Use environment variables or a secret manager. Do not put a production key in a compose file, README, issue, or request log. Set a User-Agent in standard-library clients. Allowlist outbound hosts and apply a timeout. Redact authorization headers and signed media URLs. Record the selected route and model ID for audit, but do not log user media by default.

## FAQ

**Is this a ranking?** No; it is a selection aid. **Can one platform replace all others?** Usually not: fields, models, and billing differ. **Do stars prove reliability?** No; verify current docs and run a representative check. **Why are some cells unknown?** A missing primary source is not a fact. **Should a gateway retry POST?** Only with an idempotency contract; otherwise preserve the request ID and investigate.

## Sources

OpenRouter, fal, Together, Replicate, LiteLLM, Portkey, Bifrost, Cloudflare AI Gateway, Hugging Face, RunPod, and ArgoLink documentation/model pages were checked selectively for the row claims. Recheck each linked primary source before deployment; this is a dated guide, not a live schema.

## Compose example

The compose directory is a local smoke-test shape. It uses a documented gateway image example, reads ARGO_API_KEY through the config reference, mounts configuration read-only, and contains no real key. Before production, pin an immutable digest, configure TLS and health checks, and read the current LiteLLM configuration reference. Validate with docker compose -f compose/docker-compose.yml config. Never paste a real key into YAML.
