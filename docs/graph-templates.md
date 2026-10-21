# Graph Templates

Graphs with the same kernel and dependency topology can share a construction template while retaining their own parameters and executors.

## Restoration

1. SAVE groups graphs by topology and writes a manifest.
2. LOAD parses graph binaries and builds one graph structure per template.
3. Each member applies its parameters to the builder and receives a dedicated `CUgraphExec`.
4. Replay launches that member's executor directly.

The shared graph is a builder; execution instances remain independent. Parameter switching stays outside the replay path.

## Options

| Option | Scope | Effect |
|---|---|---|
| `graph_templates` | SGLang SAVE TOML | Enable topology grouping |
| `FOUNDRY_LAZY_GRAPH_EXEC=1` | LOAD environment | Instantiate member executors on first replay |
| `FOUNDRY_DEBUG` | Build flag | Enable graph and hook diagnostics |

Eager instantiation is the default. Lazy instantiation reduces startup work by deferring it to the first use of each member.
