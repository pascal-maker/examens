# What I Learned — The Basics of GitHub

## What I understand now

### Git & Version Control
- Git is a **distributed VCS** — every developer has a full copy of the history locally, not just the latest version.
- Commits are like checkpoints. Good commit messages (e.g. `feat:`, `fix:`, `chore:`) make it easy to understand what changed and why.
- Pushing sends your local commits to the remote so teammates can see your work.

### Branches
- Branches let you work on a feature or fix without touching `main` until it's ready.
- The typical flow: `git checkout -b feature/my-feature` → commit changes → push → open a PR → merge.
- I practised this in the merge-demo and chess projects by using dedicated branches (`feature/chess-pieces`, `feature/board-setup`, `feature/decorators-and-state`).

### Merge Conflicts
- Conflicts happen when two branches change the **same line** differently.
- Git marks them with `<<<<<<<`, `=======`, `>>>>>>>` — you manually pick which version to keep (or combine both).
- In a larger project (e-commerce example) conflicts can span multiple files and require understanding the business logic to resolve correctly.

### Pull Requests
- A PR is how you propose merging a branch into `main`.
- It gives teammates a chance to review, comment, and request changes before anything is merged.
- Linking issues to PRs auto-closes them on merge.

### Other GitHub features I learned about
- **Forks** — copy someone else's repo to contribute without touching the original.
- **Issues** — track bugs, tasks, and enhancements.
- **Stars** — bookmark interesting repos.
- **Profile README** — a special `username/username` repo whose README appears on your GitHub profile.

---

## What I practised in this course

| Project | Concepts used |
|---------|--------------|
| `merge-demo` | Branching, conflicts, resolution, commits |
| `merge-demo-project` | Multi-file conflicts, business logic resolution |
| `chess` | Feature branches, decorators, OOP, generators |

---

## What I am still exploring

- `git rebase` vs `git merge` — when to use each
- Protected branches and required reviews in team settings
- GitHub Actions for automated testing on every push
- Writing better PR descriptions so reviewers have full context
