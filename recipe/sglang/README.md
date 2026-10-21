# SGLang Recipes

Install the Foundry-adapted SGLang `foundry` branch, then [build Foundry](../../README.md#installation) in that environment. Use the engine's matching kernel and communication packages. Set checkpoint paths in the chosen serve script.

Run commands from `foundry/recipe/sglang/`.

## Scripts

| Script | Configuration |
|---|---|
| `serve_qwen3-mini.sh` | Qwen3-1.7B, single GPU |
| `serve_qwen3-1.7b_dp.sh` | Qwen3-1.7B, DP |
| `serve_qwen3-1.7b_tp.sh` | Qwen3-1.7B, symmetric-memory TP |
| `serve_qwen3-30ba3b_ep.sh` | Qwen3-30B-A3B, DeepEP |
| `serve_qwen3-30ba3b_ep_tpattn.sh` | MoE with TP attention |
| `serve_qwen3-30ba3bfp8_ep_v2.sh` | FP8 MoE, DeepEP v2 |

Parallel scripts take the group size as their first argument. All accept `--save` or `--load`.

## Save and load

Configure `foundry_save.toml` and `foundry_load.toml` with the same archive and memory settings. Use a separate archive for each model/topology. The integration detects installed hook and NVSHMEM libraries; TOML fields can override their paths.

Run SAVE once, stop the server after startup, then run LOAD:

```bash
bash serve_qwen3-mini.sh --save
bash serve_qwen3-mini.sh --load
```

For example, `bash serve_qwen3-30ba3b_ep.sh 2 --save` selects EP=2. Query the model through the OpenAI-style endpoint and port configured by the serve script.

## Archive

Each `rank_<N>/` directory contains graph binaries, a manifest, CUDA module images, and allocation metadata. SAVE and LOAD use the same graph sizes and pool configuration.

See the [integration design](../../docs/sglang/overview.md).
