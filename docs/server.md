# AMO Server

AMO includes a local server for the web graph viewer.

Local only:

```bash
amo server --host 127.0.0.1 --port 8787
```

LAN access:

```bash
amo server --host 0.0.0.0 --port 8787 --token
```

Default mode should be read-only. Write operations require explicit auth.
