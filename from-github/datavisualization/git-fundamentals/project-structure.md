# Project Structure & How to Use This Repo

This repo contains the files and exercises for the **Git & GitHub Basics** course.

## Repository layout

| File | Purpose |
|------|---------|
| `README.md` | Course overview, key GitHub terms, and resources |
| `my-learning.md` | Personal learning notes — what I understood, practised, and still need to explore |

## How the project is structured

This is a documentation-focused repository used for the Git & GitHub assignment at Howest. The structure is intentionally simple:

- **One repo** = one course
- **Two main files**: `README.md` (course material) + `my-learning.md` (personal notes)
- **Branches** are used to practice isolated development workflows

## Working with this project

### Creating a new branch

```bash
git checkout -b feature/#<issue-number>-<short-description>
# e.g. feature/#1-improve-documentation
```

### Committing changes

```bash
git add <file-or-files>
git commit -m "fix: <meaningful message describing your change>"
git push origin feature/<branch-name>
```

### Making a Pull Request

After pushing, GitHub shows a **Compare & Pull Request** button. Use it to:

1. Review changes between branches
2. Add reviewers (your instructor or classmates)
3. Merge into `main` once approved

### Switching back to main

```bash
git checkout main
git pull origin main  # sync with the latest remote state
```

## Naming conventions used in this repo

- **Branches**: `feature/#<issue-number>-<description>` — links issues and branches together
- **Commit messages**: Conventional Commits style (`feat:`, `fix:`, `chore:`) for clarity
- **Issues**: Track TODOs, bugs, and enhancements; reference in branch names
