# DoVi fork changes

This log lists changes made to the OpenFang fork for DoVi. It covers repository code, not what is currently deployed. OpenFang's [CHANGELOG](../CHANGELOG.md) covers upstream releases. Agent behavior, skill definitions, and tool contracts remain authoritative in `dovi-agent-knowledge`; the files under `dovi/agents/` and `dovi/skills/` are deployment copies.

When adding a fork-specific change, record its purpose, implementation files, source contract, and whether it still needs to live in the runtime. Mark a change as retired if upstream or `dovi-mcp` replaces it.

## 2026-09-27 — Obi game-development agent

- Added `obi-director` and the Godot, Blender, and prototype-judge skills/templates as deployment copies in `dovi/obi/`. The director coordinates tasks with shared files and calls a narrowly scoped `obipc` MCP bridge on the Windows game-development PC. It does not use `dovi-mcp` as the task ledger.
- Added `dovi/obi/install_pi.py` to preserve existing task data, back up replaced manifests/configuration, install the agent workspace/skills, and register the `obipc` stdio adapter. `dovi/deploy.sh` invokes the installer before restarting OpenFang.
- Canonical prompts, skills, templates, bridge code, and generated bundle live in the DoVi Games repository at `infra/openfang/`; `infra/openfang/scripts/sync-to-fork.ps1` refreshes only the generated copies. Review and update this entry when those source files change.
- This agent setup is configuration and a PC bridge; it does not change the OpenFang Rust runtime. The native `agent_send` trace described below remains a separate DoVi runtime change.

## 2026-09-27 — Upstream v0.6.9 and coordination traces

- **Upstream baseline:** merged `RightNow-AI/openfang@acf2587` (v0.6.9) into the DoVi branch. This is an upstream update, not a DoVi-specific feature.
- **Native inter-agent trace:** `agent_send` and the WASM send path pass the actual caller ID to the kernel. The kernel publishes a request event before the existing send and a correlated reply after a successful send. It invokes the target once. Implemented in `crates/openfang-runtime/{tool_runner,kernel_handle,host_functions}.rs` and `crates/openfang-kernel/src/kernel.rs` ([commit](https://github.com/dinopollece/openfang/commit/26901c1)).
- **Communication API:** `CommsEvent` carries `exchange_id` and `reply`; `GET /api/comms/events?inter_agent_only=true` excludes user-directed audit entries; `GET /api/comms/events/{id}` returns full text while that event remains in the bus history. Implemented in `crates/openfang-types/src/comms.rs` and `crates/openfang-api/src/{routes,server}.rs` ([commit](https://github.com/dinopollece/openfang/commit/26901c1)).
- **CI compatibility:** made small Clippy 1.98 fixes in upstream memory, runtime, channel, API, and CLI code, and scoped an allowance to the existing DoVi task payload method's eight-argument signature. These do not change the DoVi API.
- **Boundary:** the visual graph belongs to `dovi-fe`, with its presentation contract in `dovi-agent-knowledge/docs/contracts/agent-coordination-view-v0.md`. Runtime instrumentation is needed to observe native `agent_send`; this event history is bounded and is not durable DoVi state. Full message content is available through the authenticated API during that window.

## 2026-05-11 — Feedback dashboard and Pi build

- Added `/api/feedbacks` and a feedback task page to OpenFang's bundled dashboard, plus an ARM64 Raspberry Pi build workflow ([commit](https://github.com/dinopollece/openfang/commit/ff8eb26)). The feedback page is an existing fork customization; new DoVi product UI should live in `dovi-fe`.

## 2026-05-10 — Feedback loop and deployment copies

- Added runtime-native `feedback_capture` and `feedback_complete` tools, task storage changes, and feedback event publication ([implementation](https://github.com/dinopollece/openfang/commit/635b125), [event API fix](https://github.com/dinopollece/openfang/commit/6e7a755)). The behavior decision is `dovi-agent-knowledge/docs/decisions/0008-use-native-feedback-capture-tool.md`.
- Added DoVi and feedback reviewer manifests, planning, task tracking, and feedback skills as runtime copies, with `dovi/deploy.sh` to propagate them ([commit](https://github.com/dinopollece/openfang/commit/dc40d03)). Their source of truth is `dovi-agent-knowledge`.
- Extended deployment to register the reviewer agent and its `feedback.captured` trigger; revised the manifests so the reviewer reacts to the event ([agent registration](https://github.com/dinopollece/openfang/commit/3ffd354), [reactive reviewer](https://github.com/dinopollece/openfang/commit/343dd66), [trigger registration](https://github.com/dinopollece/openfang/commit/26cb9de)). The workflow decision is `dovi-agent-knowledge/docs/decisions/0009-trigger-feedback-reviewer-via-feedback-event.md`.

## Revisit when changing runtime

| Customization | Possible extraction boundary |
| --- | --- |
| Native `agent_send` trace | Keep a narrow runtime event hook; move storage and visualization outside OpenFang. A DoVi MCP wrapper alone would miss native calls that bypass it. |
| Feedback tools and task storage | Reassess against `dovi-mcp` and the feedback decisions before migrating; preserve event semantics and existing data. |
| Bundled feedback dashboard | Move product-facing screens to `dovi-fe` when feature parity is available. |
| Agent and skill copies | Continue propagation from `dovi-agent-knowledge`; do not edit copies as the source. |
