# Embeddings Strategy

AMO supports embeddings as an optional intelligence layer.

The core product remains file-based and Git-native. A repository should be useful with AMO even without a vector database or external model.

## Why optional?

Embeddings introduce operational decisions:

- model provider
- vector dimensions
- refresh policy
- storage format
- privacy boundaries
- reproducibility

AMO should work before embeddings are added.

## Where embeddings help

Embeddings can improve:

- semantic memory search
- task-to-context ranking
- duplicate memory detection
- related decision discovery
- cross-repository retrieval

## Storage model

```txt
.ai/machine/embeddings.jsonl
.ai/machine/embedding_index.json
.ai/runtime/embedding_cache/
```

Version stable metadata. Ignore runtime caches.

## Alpha implementation

The alpha uses a deterministic local vectorizer so the feature works without APIs.

Future versions can add provider adapters for local models, OpenAI-compatible APIs, or vector databases.

## Source of truth

Embeddings are derived artifacts. They never replace `.ai/` memory.
