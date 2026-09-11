# Third-Party Licenses & Transparency Notice

> **Project:** `ellmos-ai/compare-race`  
> **Audited:** 2026-09-11  
> **Repository License:** [MIT License](LICENSE)  
> **Architecture & Privacy:** 100% Local-First, Zero-Egress, Unprivileged User-Mode (`RunAsInvoker`)

---

## Executive Summary & Compliance Assurance

`compare-race` is engineered under strict architectural and governance invariants: **100% Local-First, Zero-Egress by default, and unprivileged user-mode execution (`RunAsInvoker`)**. All benchmarking, lane dispatching, stopwatch timing, artefact recording, and starter-judge evaluations execute entirely within local process boundaries.

All direct, optional, and development dependencies utilized across `compare-race` are distributed under strictly **permissive open-source licenses** (MIT, Apache-2.0, PSFL). There are **zero copyleft, GPL, or AGPL dependencies**, ensuring maximum portability for local development, academic research, and automated CI/CD pipelines. The evidence-aware judge was independently implemented from concepts observed in SentinelFleet; no AGPL source was copied (see [`docs/SENTINELFLEET-CONCEPT-TRANSFER.md`](docs/SENTINELFLEET-CONCEPT-TRANSFER.md)).

Furthermore, `compare-race` guarantees:
1. **100% Local-First & Zero Egress (INV-LOCAL-01):** Model benchmarking, artefact persistence, and judging occur entirely locally. Zero telemetry, zero external tracking, and zero remote data transmission.
2. **Unprivileged User-Mode (`RunAsInvoker` / INV-SEC-02):** Executes safely in standard user space without requiring root or administrator elevation.
3. **Six-Axis Identity Discipline (INV-AXIS-03):** Every run carries `time · prompt · system · model · run · variant`. Attributions are only permitted when exactly one axis varies.
4. **Evidence-Aware Fail-Closed Judge (INV-JUDGE-04):** Only real live-executed or model-manually recorded evidence is admitted. Simulated, blocked, or unknown provenance lanes are recorded as refusals, never scored.
5. **Safe Process Scoping & Working Directory Isolation (INV-ISOL-05):** `lane_workdir` safely isolates child execution directories and restores `cwd` on exceptions; process logs are isolated under `_lane-logs`.
6. **Transparent Lane Accounting (INV-FAIL-06):** Failed lanes are explicitly recorded (`ok: false`) with error details, never silently dropped or filtered out.
7. **Descriptive Olympiad Separation (INV-BUNDLE-07):** Across bundled disciplines, medal tables count results without drawing causal conclusions across multi-variable changes.

---

## Runtime Dependency Matrix

| Package | Role / Functional Scope | License | Project Repository / Upstream |
|:---|:---|:---|:---|
| **Python Standard Library** | Core CLI runner, process timing, token hashing, JSON configuration parsing, filesystem manipulation | [PSFL-2.0](https://docs.python.org/3/license.html) | [python/cpython](https://github.com/python/cpython) |
| **system-auditor** | Front-matter parser contract and canonical execution identity discipline | [MIT](https://github.com/ellmos-ai/system-auditor/blob/main/LICENSE) | [ellmos-ai/system-auditor](https://github.com/ellmos-ai/system-auditor) |

---

## Optional Execution Adapter Dependencies

| Package | Role / Functional Scope | License | Project Repository / Upstream |
|:---|:---|:---|:---|
| **coma** (optional) | Multi-provider LLM CLI orchestrator & adapter framework (Claude, Codex, Agy, Kimi) | [MIT](https://github.com/dev-bricks/coma/blob/main/LICENSE) | [dev-bricks/coma](https://github.com/dev-bricks/coma) |

---

## Development & Quality Assurance Tooling

| Package | Usage & Purpose | License | Source / Upstream |
|:---|:---|:---|:---|
| **pytest** | Automated test runner, contract verification suites, mock fixtures | [MIT](https://github.com/pytest-dev/pytest/blob/main/LICENSE) | [pytest-dev/pytest](https://github.com/pytest-dev/pytest) |
| **ruff** | High-performance Python linter and code formatting enforcement | [MIT / Apache-2.0](https://github.com/astral-sh/ruff/blob/main/LICENSE-MIT) | [astral-sh/ruff](https://github.com/astral-sh/ruff) |
| **setuptools** | Standard package build backend (PEP 517 / PEP 621 compliant) | [MIT](https://github.com/pypa/setuptools/blob/main/LICENSE) | [pypa/setuptools](https://github.com/pypa/setuptools) |

---

## Full License Texts (Excerpts & Notices)

### 1. Python Software Foundation License Version 2 (PSFL-2.0)
Python standard library modules are used under the PSF License Agreement.  
Copyright (c) 2001-2026 Python Software Foundation. All rights reserved.

### 2. MIT License (MIT)
Used by `system-auditor`, `coma`, `pytest`, and `setuptools`.

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:  
>  
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.  
>  
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### 3. Apache License Version 2.0 (Apache-2.0)
Co-licensed by `ruff`.

> Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at:  
> http://www.apache.org/licenses/LICENSE-2.0  
> Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
