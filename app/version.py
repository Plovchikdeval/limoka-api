import os
import git


try:
    branch = git.Repo(
        path=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    ).active_branch.name
except Exception:
    branch = "main"


def get_info(branch):
    repo = git.Repo()
    build = repo.heads[0].commit.hexsha
    diff = repo.git.log([f"HEAD..origin/{branch}", "--oneline"])
    upd = "Update required" if diff else "Up-to-date"

    return {"build": build, "upd": upd, "branch": branch}
