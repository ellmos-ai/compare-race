# compare-race

> Same prompt, several models — stopwatch or true race. The **starting model judges**;
> time is only one dimension of the verdict.

[Deutsche Fassung](README_de.md)

## What it does

`compare-race` fans one prompt out to several LLMs — **sequentially** (the stopwatch:
one lane at a time, clean per-lane timing) or **in parallel** (the true race) — with
optional repetitions per model, and collects every answer as an artefact. The verdict
is **model-manual**: the starting model reads the lanes and fills a multi-dimensional
rubric (quality, correctness, completeness, instruction fidelity, latency, cost).
The stopwatch is only a picture.

## Identity — five axes, reused from system-auditor

Every run carries `time · prompt · system · model · run`. A difference may only be
*attributed* when exactly one axis varies: models vary → the race; runs vary →
variance of one model; time varies → drift across versions. The artefact headers speak
the [`system-auditor`](https://github.com/ellmos-ai/system-auditor) front-matter parser
— that library is the one hard dependency.

## Install and use

```bash
pip install -e .           # pulls system-auditor from GitHub
# execution layer (detected, not assumed):
git clone https://github.com/ellmos-ai/coma && pip install -e coma

cp config/compare-race.config.example.json compare-race.config.json
compare-race config
compare-race run --prompt-file question.md --mode sequential --repeats 2
# without COMA: run lanes yourself, then
compare-race record --model codex --output-file out.md --race-id <id>
```

Role prompt for agents: [`prompts/RACE-STARTER.en.md`](prompts/RACE-STARTER.en.md)
(German: [`RACE-STARTER.de.md`](prompts/RACE-STARTER.de.md)).

## Neighbours (detected, never assumed)

[coma](https://github.com/ellmos-ai/coma) spawn/polling/file protocol ·
clutch model catalogue · swarm-ai N-repeat consensus (mechanical) ·
MarbleRun sequential chains. compare-race adds what none of them have: the
**qualitative judge over sibling outputs** and the repetition×model cross product.

## License

MIT.
