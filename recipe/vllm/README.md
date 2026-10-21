# vLLM Recipes

Install the Foundry-adapted vLLM checkout before [building Foundry](../../README.md#installation), using the same Torch/CUDA environment. Set checkpoint paths in the chosen serve script.

Run commands from `foundry/recipe/vllm/`.

## Scripts

| Script | Configuration |
|---|---|
| `serve_qwen3-mini.sh` | Qwen3-1.7B, single GPU |
| `serve_qwen3-1.7b_tp.sh` | Qwen3-1.7B, TP |
| `serve_qwen3-14b_dp.sh` | Qwen3-14B, DP |
| `serve_qwen3-30ba3b_ep.sh` | Qwen3-30B-A3B, DeepEP |
| `serve_qwen3-30ba3bfp8_ep.sh` | FP8 MoE, DeepGEMM |

Parallel scripts take the group size as their first argument. All accept `--save` or `--load`.

## Save and load

Configure `foundry_save.toml` and `foundry_load.toml` with the same archive and memory settings. Use a separate archive for each model/topology. EP also needs the matching NVSHMEM host library.

Run SAVE twice, stopping the server after each startup, then run LOAD:

```bash
bash serve_qwen3-mini.sh --save
bash serve_qwen3-mini.sh --save
bash serve_qwen3-mini.sh --load
```

For example, `bash serve_qwen3-30ba3b_ep.sh 2 --save` selects EP=2. Query the model through the OpenAI-style endpoint and port configured by the serve script.

## Archive

`workspace_root` contains warmup state and one `rank_<N>/` directory per rank with graph binaries, a manifest, CUDA module images, and allocation metadata.

See the [integration design](../../docs/vllm/overview.md) or the [legacy IPC variant](experimental/README.md).
