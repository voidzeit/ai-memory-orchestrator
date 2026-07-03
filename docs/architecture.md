# Architecture

AMO is organized around one invariant:

```txt
repo = code truth
.ai/ = memory truth
.ai/machine/ = derived indexes
.ai/packs/ = compiled agent context
.ai/runtime/ = disposable session state
```

## Lifecycle

```txt
init -> scan -> context -> agent work -> postflight -> validate -> graph/server/sync
```

## Layers

1. Canonical memory
2. Machine indexes
3. Project graph
4. Context compiler
5. Validators
6. Web graph server
7. Adapters
