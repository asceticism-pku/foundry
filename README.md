# Foundry

Foundry captures CUDA graphs and restores them across process restarts. It persists graph structure, kernel binaries, and deterministic device-memory layouts to reduce inference-engine startup work.

## Installation

Use Linux, standard CPython 3.10 (>=3.10,<3.11) with the GIL enabled, a CUDA-enabled PyTorch environment, CMake 4+, and Boost 1.83+. Install the inference engine before building Foundry in the same environment.

From the Foundry directory:

```bash
conda install -c conda-forge 'boost-cpp>=1.83' 'boost>=1.83' 'cmake>=4.0' ninja
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
python -m pip install -e . --no-build-isolation
```

`libcuda_hook.so` intercepts CUDA driver calls through `LD_PRELOAD`. Engine integrations configure worker preloading; direct library callers preload it before starting a CUDA process.

## Engine integrations

| Engine | Design | Usage |
|---|---|---|
| vLLM | [Integration](docs/vllm/overview.md) | [Recipes](recipe/vllm/README.md) |
| SGLang | [Integration](docs/sglang/overview.md) | [Recipes](recipe/sglang/README.md) |

Aegaeon's integration is configured separately through its `server.cuda_graph` settings.

## Library API

| Entry point | Purpose |
|---|---|
| `CUDAGraph` / `graph()` | Capture and replay a graph |
| `CUDAGraph.save(path, output_tensors=...)` | Save graph and output metadata |
| `CUDAGraph.load(path)` | Restore a graph and its outputs |
| `load_cuda_modules_and_libraries()` | Restore archived CUDA modules |
| `set_allocation_region()` / `allocation_region()` | Use a deterministic VMM address range |
| `preallocate_region()` | Reserve physical memory for fast allocation |
| `save_graph_manifest()` | Group graphs by topology |
| `CUDAGraph.start_graph_builds()` / `CUDAGraph.finish_graph_loads()` | Build and restore graph sets asynchronously |

SAVE and LOAD use matching allocations, graph shapes, and runtime dependencies. See [Graph Templates](docs/graph-templates.md) for grouped graph restoration.

## Integration configuration

Both engine integrations read a TOML file:

| Field | Purpose |
|---|---|
| `mode` | `none`, `save`, or `load` |
| `workspace_root` | Archive directory |
| `base_addr` | Base virtual address shared by SAVE and LOAD |
| `region_size` | Reserved virtual-address range |
| `scratch_space_size` | Space for initialization scratch allocations |
| `hook_library_path` | Optional explicit hook path |
| `nvshmem_host_path` | Optional NVSHMEM host-library path |

Each rank stores its graph and kernel artifacts separately. Use a separate archive directory for each model and topology.

See [Contributing](CONTRIBUTING.md), [Release Notes](RELEASE.md), and the [Roadmap](ROADMAP.md).
