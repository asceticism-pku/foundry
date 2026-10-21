# vLLM Integration

Foundry persists vLLM Decode graphs and restores them at startup. An engine-side shim activates the integration; runtime behavior lives in `python/foundry/integration/vllm/`.

## Components

| Module | Responsibility |
|---|---|
| `config.py` | TOML configuration and rank workspaces |
| `runtime.py` | VMM region, warmup state, and allocation watermark |
| `graph_ops.py` | Graph archives, CUDA binaries, and manifests |
| `hooks.py` | Engine lifecycle integration |

## Memory contract

SAVE and LOAD use the same model, KV layout, virtual addresses, and capture configuration. vLLM uses two SAVE passes: the first records memory sizing, and the second captures with that sizing fixed. LOAD restores the resulting workspace.

Graph-owned allocations remain in the deterministic region through capture; subsequent runtime allocations use the normal CUDA allocator. Capture warmup is disabled while Foundry controls the graph lifecycle.

For MoE, load weights and initialize communication buffers before restoring communication kernels. See [MoE and DeepEP](moe-and-deepep.md).

## Usage

See the [vLLM recipes](../../recipe/vllm/README.md) for installation and commands, the [shared configuration reference](../../README.md#integration-configuration) for TOML fields, and [Hooks](hooks.md) for implementation entry points.
