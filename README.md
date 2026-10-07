# Multi-model API gateway

This repository is a self-hosted-versus-hosted decision guide with a runnable local LiteLLM example. It is not a gateway product and is not affiliated with any listed vendor. [ArgoLink](https://argolink.io/gh-multi-model-api-gateway) is shown as one upstream provider. Checked 2026-10-07.

## Decision guide

| Question | Self-hosted LiteLLM/Bifrost | Hosted gateway/aggregator |
| --- | --- | --- |
| Where do credentials live? | Your secret store and process environment | Hosted account or virtual-key policy |
| Who controls egress? | Your network and allowlist | Vendor edge and provider policy |
| Routing and fallback | Your model groups, health policy, and retry budget | Vendor's documented provider policy |
| Cache | Your chosen backend and retention policy | Vendor plan/configuration; verify media behavior |
| Budget | Your proxy counters plus upstream bills | Account credits, limits, and upstream usage |
| Operations | You own TLS, upgrades, logs, and rollback | Vendor owns gateway availability; you still own client behavior |
| Best fit | Compliance, internal policy, predictable egress | Fast setup and hosted observability |

A gateway can standardize an interface, but it cannot erase provider differences. Model IDs, tools, streaming, image reference limits, video job states, and usage fields must be mapped and tested per upstream.

## Runnable local example

The `compose/` directory starts LiteLLM v1.104.0 on `127.0.0.1:4000`. The configuration has two explicit model aliases: `argolink-gpt-6-sol` points at ArgoLink's current `/v1/responses` model family, while `openai-gpt-4-1-mini` is a separate provider example. The first alias has a documented fallback target; retry count is set to zero so an ambiguous POST is not silently duplicated. Adjust that policy only after deciding which requests are idempotent.

1. Export credentials in your shell or an ignored `.env` file:

   ```bash
   export ARGO_API_KEY='replace-with-a-development-key'
   export OPENAI_API_KEY='replace-with-a-development-key'
   ```

2. Validate the rendered configuration without starting a container:

   ```bash
   docker compose -f compose/docker-compose.yml config
   ```

3. Start the local gateway after reviewing the rendered config:

   ```bash
   docker compose -f compose/docker-compose.yml up
   ```

4. Send a text request to the local OpenAI-shaped boundary only after checking the selected model and budget. Do not paste keys into this repository or its issue tracker.

The image uses a version tag for a reproducible example; production should pin the image digest after your image-scanning process approves it. Bind to loopback in development, put TLS/authentication in front of a shared deployment, and retain a rollback path for image/config changes.

## ArgoLink model contract

Use `https://argolink.io/v1` as the API base. The current catalog lists `gpt-6-sol` on `POST /v1/responses`; model ID, context, reasoning controls, and pricing come from the live model list and should be refreshed before deployment. Image routes use `/v1/images/generations` or `/v1/images/edits`; video routes use `/v1/videos/generations`, then status/content endpoints with model-specific limits. This repository does not assume that a text alias can accept image or video fields.

Every client request should set a descriptive `User-Agent`, a connect/read timeout, and a request identifier. Never log `Authorization`, signed media URLs, or full prompts containing secrets. Record upstream request IDs and selected aliases for audit.

## Routing and fallback safety

Classify failures before acting: validation 4xx errors should not retry; 429 responses should honor `Retry-After`; connection failures before a request is written may be retried within a bound; a timeout after a POST may have created a billable job and requires request-ID reconciliation. For images and videos, preserve the asynchronous job ID and query its status before selecting a fallback. A fallback should be explicit in the manifest, with estimated cost and the reason for switching.

## Hosted alternatives

Use a hosted aggregator when broad model discovery and low operational overhead matter. Use a managed gateway when hosted observability and policy controls matter. Use a self-hosted gateway when secrets, budgets, audit logs, and egress must remain inside your boundary. Use a direct provider API when provider-specific fields matter more than one abstraction.

## Sources

See [`sources.md`](sources.md) for the LiteLLM configuration references, ArgoLink model source, and hosted/self-hosted comparison sources. They were checked on 2026-10-07; re-check current schemas, image digests, model IDs, and pricing before production.
