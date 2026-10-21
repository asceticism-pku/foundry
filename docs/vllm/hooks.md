# vLLM Hooks

`install_hooks()` connects Foundry to the engine lifecycle. Implementations are in `python/foundry/integration/vllm/hooks.py`.

| Hook | Responsibility |
|---|---|
| Device capability query | Keep the parent process fork-safe |
| Distributed initialization | Reserve the VMM region and scratch boundary |
| `kernel_warmup` | Use the archive-controlled warmup path |
| `_dummy_run` | Skip sampler-only warmup while preserving profile and collective forwards |
| `load_model` | Preallocate, load weights, then start graph builds |
| Communication buffer setup | Initialize archived NVSHMEM modules after communication bootstrap |
| `capture_model` | Save/restore graphs and finish the allocation region |
| `CUDAGraphWrapper.__call__` | Capture or restore the matching graph |
| KV cache initialization | Save or restore memory sizing |
| Worker spawn sites | Set hook preloading before process startup |
| DeepEP buffer setup | Select the Foundry-compatible communication path |

Preserve the allocation order and the real forwards needed by distributed collectives. The [integration overview](overview.md) describes the memory contract; [recipes](../../recipe/vllm/README.md) contain runtime commands.
