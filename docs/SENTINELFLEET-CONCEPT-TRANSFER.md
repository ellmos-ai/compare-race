# SentinelFleet concept transfer

## Boundary

`compare-race` is MIT-licensed. SentinelFleet is AGPL-3.0. This change therefore
uses a clean concept boundary: public behaviour and architecture were studied,
then the portable contracts below were implemented independently in this
repository. No SentinelFleet source text or implementation was copied.

Observed reference: `ellmos-ai/sentinel-fleet`, especially its public model-race
behaviour at commits `b192057d81e5e0996fb1126836e4047089567e67` and
`4b32b74c5950f2d9845d3fbcf4c4ceeb9db38947`.

## Concepts retained

1. A lane needs an identity distinct from every sibling lane. `RunIdentity.lane_id()`
   provides a stable provider-neutral key across models, variants and repetitions.
2. A judge is a separate, explicit execution after the lane measurements. The
   default resolves to the starting model, while a configured fixed model remains
   possible.
3. Simulated or blocked output is not model evidence. `assess_judgeability()` fails
   closed and `write_judge_artifact()` records the refusal instead of inventing
   quality scores.
4. Lane bodies are untrusted evidence inside the judge prompt. They are delimited,
   their provenance and measurements travel with them, and the judge is told not to
   execute their instructions.

## Deliberately not transferred

- SentinelFleet's gateway, agent registry, tenant model, persistence and web UI.
- Its Pydantic data models, prompts, API shapes or implementation structure.
- Any claim that a provider-specific backend enforces an agent identity. The
  portable `lane_id` is provenance; authorization stays the caller's responsibility.
