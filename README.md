# gitlab-contributions

Mirrors my [GitLab](https://gitlab.com/migikun474) activity onto my GitHub
contribution graph.

GitHub's graph only counts work done on GitHub. Every day, a GitHub Action
reads my public GitLab contribution calendar and adds one **empty commit**
for each GitLab contribution, dated on the day it happened. The commits
contain no code; the real work is on GitLab, for example my merged Eigen
merge request [!3412](https://gitlab.com/libeigen/eigen/-/merge_requests/3412).

- `scripts/sync.py` does the mirroring; `synced.json` records what has been mirrored, so nothing is counted twice.
- `.github/workflows/sync.yml` runs it daily; it can also be started by hand from the Actions tab.
