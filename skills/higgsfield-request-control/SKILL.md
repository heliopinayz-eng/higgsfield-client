---
name: higgsfield-request-control
description: Poll status, fetch result, or cancel an existing Higgsfield API request by request_id via the Python SDK's explicit control functions (not subscribe). Use when a worker already holds a request_id and needs status/result/cancel control instead of automatic polling — e.g. 'check status of this request_id', 'cancel this higgsfield job', 'get result for request_id'.
license: MIT
compatibility: Requires python3.
---

# Higgsfield Request Control

## Purpose

Check status, fetch result, or cancel a Higgsfield API request by
`request_id`, using the Python SDK's explicit control functions
(`status`/`result`/`cancel`) instead of `subscribe`'s automatic polling.
For when a worker already holds a `request_id` from an earlier `submit`
call and needs one-shot control over it.

Model-agnostic: `request_id` alone identifies the request server-side —
no model/endpoint argument needed here. Works the same for any Higgsfield
model (e.g. `bytedance/seedance-2.5/text-to-video`, `minimax/h3/reference-to-video`,
or any future one) as long as it was created via `submit`.

## Commands

```bash
python3 higgsfield_request_control.py status <request_id>
python3 higgsfield_request_control.py result <request_id>
python3 higgsfield_request_control.py cancel <request_id>
```

Requires `HF_KEY` (or `HF_API_KEY` + `HF_API_SECRET`) in the environment
and `higgsfield-client` installed (`pip install higgsfield-client`).

## Rules

- Never poll in a loop here — that is what `subscribe` is for. This skill
  makes exactly one API call per invocation.
- Never invent a `request_id` — it only exists after an earlier `submit`
  call; ask the caller for it rather than guessing.

## Related Notes

- status-result-cancel.md (repo docs/notes/) — original doc excerpt this skill was built from.
