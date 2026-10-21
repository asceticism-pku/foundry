# SGLang Hooks

`install_hooks()` connects Foundry to the engine lifecycle. Implementations are in `python/foundry/integration/sglang/hooks.py`.

| Hook | Responsibility |
|---|---|
| Distributed initialization | Bind the rank's device and reserve its VMM region |
| Memory-pool initialization | Preserve deterministic KV and pool sizing |
| `load_model` | Restore CUDA modules and memory allocation state |
| `kernel_warmup` | Use the archive-controlled warmup path |
| `CudaGraphRunner` | Prepare metadata and capture/restore the graph set |
| Worker spawn sites | Install hooks and preload libraries in child processes |
| DeepEP setup | Bootstrap communication and restore its kernel modules |

SAVE and LOAD keep the same pool configuration and per-batch metadata layout. See the [integration overview](overview.md) for the memory contract and [recipes](../../recipe/sglang/README.md) for runtime commands.
