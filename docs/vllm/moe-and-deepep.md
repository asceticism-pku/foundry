# MoE and DeepEP

The vLLM integration keeps MoE weight packing and communication setup consistent across SAVE and LOAD.

## Communication setup

The default DeepEP path uses fabric/NVSHMEM buffers. Provide a compatible NVSHMEM host library through `nvshmem_host_path` when it is not supplied by the installed environment.

Initialization order is:

1. Load model weights and prepare communication buffers.
2. Initialize archived NVSHMEM modules with `init_nvshmem_for_loaded_modules()`.
3. Finish graph restoration and launch graphs.

Each rank uses its own archive artifacts. Keep model, parallelism, KV sizing, and communication configuration consistent across modes.

For hosts using legacy CUDA IPC buffers, see the [IPC recipe](../../recipe/vllm/experimental/README.md). Other commands are in the [vLLM recipes](../../recipe/vllm/README.md).
