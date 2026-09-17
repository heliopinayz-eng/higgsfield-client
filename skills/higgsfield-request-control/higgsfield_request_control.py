#!/usr/bin/env python3
"""Check status, fetch result, or cancel an existing Higgsfield API request.

Wraps higgsfield_client's explicit control functions (status/result/cancel)
for a request_id a caller already holds — no polling loop, one call in, one
answer out. Requires HF_KEY (or HF_API_KEY + HF_API_SECRET) in the
environment.
"""
import argparse
import json
import sys


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("action", choices=["status", "result", "cancel"])
    ap.add_argument("request_id")
    args = ap.parse_args(argv)

    try:
        import higgsfield_client
    except ImportError:
        print(
            "higgsfield_client not installed. "
            "pip install higgsfield-client",
            file=sys.stderr,
        )
        return 1

    try:
        if args.action == "status":
            result = higgsfield_client.status(request_id=args.request_id)
            print(result.__class__.__name__)
        elif args.action == "result":
            result = higgsfield_client.result(request_id=args.request_id)
            print(json.dumps(result))
        else:
            higgsfield_client.cancel(request_id=args.request_id)
            print("cancelled")
    except higgsfield_client.CredentialsMissedError as exc:
        print(f"credentials error: {exc}", file=sys.stderr)
        return 1
    except higgsfield_client.HiggsfieldClientError as exc:
        print(f"request failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
