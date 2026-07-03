# Comparison

AMO is not a replacement for AI coding tools. It is a shared repository memory layer that those tools can consume.

## Instruction files

Files such as `AGENTS.md` and tool-specific instruction docs are useful, but they can drift when maintained by hand.

AMO treats these files as generated adapters from canonical `.ai/` memory.

## Editor rules

Editor-specific rules are useful inside one editor, but they are not a portable memory model.

AMO keeps canonical memory portable and exports editor-specific views when needed.

## Memory banks

Memory-bank approaches are useful for long-running agent work.

AMO extends the pattern with validation, machine indexes, context packs, graph data, and multiple adapters.

## Human graph tools

Human graph tools are excellent for navigation.

AMO uses them as optional views, while `.ai/` remains the source of truth.

## Databases and embeddings

Search systems can help, but AMO does not require a database to start.

The alpha is file-based, portable, and Git-native.

## Summary

```txt
AI coding tool       = consumes context
AMO                  = prepares verified repository context
```
