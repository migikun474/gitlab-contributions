"""Mirror GitLab contribution counts into this repo as empty, backdated commits.

Reads the public GitLab contribution calendar, compares it with the counts
already mirrored (synced.json), and makes one empty commit for every
contribution not yet mirrored, dated on the day it happened. GitHub then
counts those days on the contribution graph.
"""
import json, os, subprocess, sys, urllib.request

USER = os.environ.get("GITLAB_USER", "migikun474")
NAME = os.environ["AUTHOR_NAME"]
EMAIL = os.environ["AUTHOR_EMAIL"]
STATE = "synced.json"

if len(sys.argv) > 1:                      # local test: a saved calendar.json
    calendar = json.load(open(sys.argv[1]))
else:
    req = urllib.request.Request(f"https://gitlab.com/users/{USER}/calendar.json",
                                 headers={"User-Agent": "gitlab-contributions-sync"})
    calendar = json.load(urllib.request.urlopen(req, timeout=30))

synced = json.load(open(STATE)) if os.path.exists(STATE) else {}
env = {**os.environ, "GIT_AUTHOR_NAME": NAME, "GIT_AUTHOR_EMAIL": EMAIL,
       "GIT_COMMITTER_NAME": NAME, "GIT_COMMITTER_EMAIL": EMAIL}

todo = []
for day in sorted(calendar):
    missing = calendar[day] - synced.get(day, 0)
    todo += [(day, i) for i in range(max(missing, 0))]
    if missing > 0:
        synced[day] = calendar[day]

if todo:
    # The state file rides along in the first mirrored commit, so no extra
    # commit (and no extra contribution) is made for bookkeeping.
    json.dump(dict(sorted(synced.items())), open(STATE, "w"), indent=2)
    subprocess.run(["git", "add", STATE], check=True)
    for day, i in todo:
        stamp = f"{day}T12:{i % 60:02d}:00+05:30"
        e = {**env, "GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp}
        subprocess.run(["git", "commit", "--allow-empty", "-q", "-m",
                        f"GitLab contribution on {day}"], env=e, check=True)
print(f"mirrored {len(todo)} new GitLab contribution(s)")
