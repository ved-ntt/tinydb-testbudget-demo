"""Write the plan as a job summary (stdout) and post it as a GitHub check run."""

import json
import sys

from testbudget.github import checks

with open(sys.argv[1], encoding="utf-8") as handle:
    plan = json.load(handle)
repo = sys.argv[2]
selected, skipped = plan["selected"], plan["skipped"]
used = sum(t.get("duration_s", 0.0) for t in selected)
rate = plan["catch_rate_estimate"]
rate_text = "unknown" if rate is None else f"{rate:.0%}"

summary = "\n".join(
    [
        f"**Risk level:** {plan['risk_level']}",
        f"**Budget:** {plan['budget_s']:.3f}s (planned test time {used:.3f}s)",
        f"**Historical catch rate:** {rate_text}",
        f"**Tests run:** {len(selected)}",
        f"**Tests skipped:** {len(skipped)}",
    ]
)
lines = ["## TestBudget plan", "", summary, "", "### First tests in the plan", ""]
lines += [f"{i}. `{t['test_id']}`: {t['reason']}" for i, t in enumerate(selected[:20], 1)]
more = max(len(selected) - 20, 0)
lines += ["", f"...and {more} more selected, {len(skipped)} skipped."]
print("\n".join(lines))

try:
    token = checks.get_token()
    payloads = checks.build_payloads(plan)
    for payload in payloads:
        payload["output"]["summary"] = summary
    base = f"{checks.API}/repos/{repo}"
    run_id = checks._http("POST", f"{base}/check-runs", token, payloads[0])["id"]
    for extra in payloads[1:]:
        checks._http("PATCH", f"{base}/check-runs/{run_id}", token, extra)
except Exception as error:  # the tests still run if the check can't be posted
    print(f"::warning::Could not post the TestBudget check run: {error}", file=sys.stderr)
