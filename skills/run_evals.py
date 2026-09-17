#!/usr/bin/env python3
"""
Eval runner for PAIOS skills — the regression net.

Each skill may ship evals/evals.json: a list of scenarios
  {"name": ..., "cmd": [...], "expect_exit": 0, "expect_substr": "...",
   "reject_substr": "...", "stdin": "..."}

Deterministic, side-effect-free scenarios only (the CLIs are read-only unless
told otherwise, and these never tell them otherwise). Run before trusting any
skill edit:

    python3 skills/run_evals.py            # all skills
    python3 skills/run_evals.py paios-today
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def run_skill(skill):
    path = os.path.join(HERE, skill, "evals", "evals.json")
    if not os.path.isfile(path):
        return None
    cases = json.load(open(path))
    passed = 0
    for c in cases:
        r = subprocess.run(c["cmd"], capture_output=True, text=True,
                           input=c.get("stdin"), timeout=120, cwd=HERE)
        out = r.stdout + r.stderr
        ok = True
        if "expect_exit" in c and r.returncode != c["expect_exit"]:
            ok = False; why = "exit %d != %d" % (r.returncode, c["expect_exit"])
        elif c.get("expect_substr") and c["expect_substr"] not in out:
            ok = False; why = "missing %r" % c["expect_substr"]
        elif c.get("reject_substr") and c["reject_substr"] in out:
            ok = False; why = "forbidden %r present" % c["reject_substr"]
        print("  %s %s%s" % ("PASS" if ok else "FAIL", c["name"],
                             "" if ok else "  (%s)" % why))
        passed += ok
    print("%s: %d/%d" % (skill, passed, len(cases)))
    return passed == len(cases)

def main():
    targets = sys.argv[1:] or sorted(
        d for d in os.listdir(HERE)
        if os.path.isfile(os.path.join(HERE, d, "evals", "evals.json")))
    results = [run_skill(t) for t in targets]
    sys.exit(0 if all(r is not False for r in results) else 1)

if __name__ == "__main__":
    main()
