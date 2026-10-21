# SGLang Integration

Foundry persists SGLang `CudaGraphRunner` graphs and restores them at startup. An engine-side shim activates `python/foundry/integration/sglang/`.

## Components

| Module | Responsibility |
|---|---|
| `config.py` | TOML configuration and hook/library paths |
| `runtime.py` | VMM region and allocation watermark |
| `graph_ops.py` | Graph archives and CUDA binaries |
| `hooks.py` | Engine and worker lifecycle integration |

## Memory contract

SGLang uses one SAVE pass. LOAD restores the saved graph set and deterministic memory layout. Set the current CUDA device before reserving the VMM region in each rank, and keep KV pools, scratch space, model settings, and graph sizes identical between modes.

Single-GPU, DP, symmetric-memory TP, and DeepEP EP configurations have corresponding recipes. Attention and communication setup is selected by each serve script.

## Usage

See the [SGLang recipes](../../recipe/sglang/README.md) for installation and commands, the [shared configuration reference](../../README.md#integration-configuration) for TOML fields, and [Hooks](hooks.md) for implementation entry points.
