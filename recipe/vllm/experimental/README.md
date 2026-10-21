# DeepEP Legacy CUDA IPC Recipe

This variant keeps DeepEP's intra-node NVLink buffer on the legacy CUDA IPC path. Foundry translates sharing of VMM allocations through POSIX file descriptors and peer mappings.

Follow the base [vLLM recipe](../README.md) for installation and the two-pass SAVE workflow. This variant enables `FOUNDRY_DEEPEP_NVL_IPC=1` and uses the separate `foundry_archive_ipc` workspace.

## Run

Set the model and NVSHMEM paths in the script/TOML files. From one consistent workspace containing the Foundry and vLLM checkouts:

```bash
bash foundry/recipe/vllm/experimental/serve_qwen3-30ba3b_ipc_ep.sh 2 --save
bash foundry/recipe/vllm/experimental/serve_qwen3-30ba3b_ipc_ep.sh 2 --save
bash foundry/recipe/vllm/experimental/serve_qwen3-30ba3b_ipc_ep.sh 2 --load
```

Stop the server between modes. Keep the working directory, model, parallelism, and archive settings consistent across all runs.
