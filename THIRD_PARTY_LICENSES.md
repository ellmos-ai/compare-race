# Third-Party Licenses & Transparency Notice (Level 1 SBOM)

> **Project:** `ellmos-ai/compare-race`<br>
> **Audited:** 2026-09-23<br>
> **Repository License:** [MIT License](LICENSE)<br>
> **Repository Attribution Notice:** [NOTICE](NOTICE)<br>
> **Architecture & Privacy:** 100% Local-First, Zero-Egress by default, Unprivileged User-Mode (`RunAsInvoker`)

---

## Executive Summary & Compliance Assurance

`compare-race` is engineered under strict architectural and governance invariants: **100% Local-First, Zero-Egress by default, and unprivileged user-mode execution (`RunAsInvoker`)**. All benchmarking, lane dispatching, stopwatch timing, artefact recording, and starter-judge evaluations execute entirely within local process boundaries.

All direct, optional, and development dependencies utilized across `compare-race` are distributed under strictly **permissive open-source licenses** (MIT, Apache-2.0, PSFL). There are **zero copyleft, GPL, or AGPL dependencies**, ensuring maximum portability for local development, academic research, and automated CI/CD pipelines. The evidence-aware judge was independently implemented from concepts observed in SentinelFleet; no AGPL source was copied (see [`docs/SENTINELFLEET-CONCEPT-TRANSFER.md`](docs/SENTINELFLEET-CONCEPT-TRANSFER.md)).

### Invariant Cross-Reference Matrix

| Invariant ID | Security & Operational Mandate | Technical Enforcement Mechanism | License & Isolation Scope |
|:---|:---|:---|:---|
| `INV-LOCAL-01` | **100% Offline / Zero-Egress** | Pure local subprocess benchmarking, zero outbound telemetry, zero tracking | [PSFL-2.0](https://docs.python.org/3/license.html) |
| `INV-SEC-02` | **Non-Elevation (`RunAsInvoker`)** | Unprivileged execution without requiring root or administrator elevation | [MIT](LICENSE) |
| `INV-AXIS-03` | **Six-Axis Attribution Discipline** | Strict identity tuple: `time · prompt · system · model · run · variant` | [MIT](https://github.com/ellmos-ai/system-auditor) |
| `INV-JUDGE-04` | **Evidence-Aware Fail-Closed Judge** | Only real live-executed or model-manually recorded evidence admitted | [MIT](LICENSE) |
| `INV-ISOL-05` | **Safe Process & Workspace Isolation** | `lane_workdir` sandboxing isolates child cwd and safely restores context | [PSFL-2.0](https://docs.python.org/3/license.html) |
| `INV-FAIL-06` | **Transparent Lane Accounting** | Failed lanes explicitly recorded (`ok: false`) with error details, never dropped | [MIT](LICENSE) |
| `INV-BUNDLE-07` | **Descriptive Olympiad Separation** | Across bundled disciplines, medal table stays descriptive: count, don't conclude | [MIT](LICENSE) |
| `INV-INTEROP-08` | **Sibling Ecosystem Interoperability** | Native compatibility with `ellmos-ai` and `open-bricks` ecosystem | [MIT](https://github.com/ellmos-ai) |
| `INV-LIC-09` | **100% Permissive Audited Stack** | Audited dependency stack, zero copyleft/AGPL contamination | [MIT / PSFL-2.0 / Apache-2.0](THIRD_PARTY_LICENSES.md) |
| `INV-SLA-10` | **Cryptographic Parity & Dual Security SLA** | Contract test verification, 48-hour response, 5-day triage commitment | [SECURITY.md](SECURITY.md) |

---

## Zero-Copyleft Isolation Guarantee & RunAsInvoker Certification

1. **Zero-Copyleft Guarantee:** No component of `compare-race` links against, vendors, or invokes any code under GPLv2, GPLv3, AGPLv3, LGPL, SSPL, or CC-BY-SA licenses. All dependencies are strictly permissive (MIT, Apache-2.0, PSFL-2.0).
2. **Unprivileged Execution (`RunAsInvoker`):** `compare-race` requires no administrative privileges, no daemon services, and no root credentials. It operates entirely in unprivileged user space.
3. **Zero-Egress Perimeter:** By default, no network traffic is emitted by `compare-race`. When external LLM CLI tools are invoked via detected adapters (such as `coma`), network interaction is governed strictly by the user's authenticated CLI configuration and explicit policies.

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
