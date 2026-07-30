# Second Assignment — Merge Conflicts & Git LFS

## Goal of This Assignment

The goal of this assignment is to deepen the understanding of collaborative workflows in Git, specifically around:

1. **Merge conflicts** — what causes them and how to resolve them correctly.
2. **Advanced merge conflicts** — resolving conflicts where both branches need to be combined (not just picking one side).
3. **Git LFS** — tracking large binary files so they don't bloat Git history.

This builds on the basics covered in the first assignment and prepares you for real-world team workflows where multiple developers work on shared code simultaneously.

---

## What Was Done So Far

### Merge Conflicts (Basic HTML/CSS Example)

Walked through a complete merge conflict scenario:

1. Created `index.html` + `style.css` with initial content
2. Committed to main: `"Initial commit"`
3. Created branch `feature-branch`, changed h1 color from blue → red, committed
4. Switched back to main, changed same file — blue → green, committed
5. Attempted `git merge feature-branch` → conflict detected
6. Resolved by choosing a version and removing markers (`<<<<<<< HEAD`, `=======`, `>>>>>>>`)

**How we demonstrated it:** Through the terminal as a live demo (not committed to repo). This is how you'd show this during a presentation or sketch session — the instructor watches you create branches, make conflicting changes, merge, resolve, then commit.

### Advanced Merge Conflict Challenge: E-Commerce Feature Integration

Explored a more realistic scenario where two teams work on parallel features that touch overlapping code:

1. **Branch A (Feature-Discount):** Adds discount logic to `Product.js` and `pricing.js`
2. **Branch B (Feature-Tax):** Adds tax calculations to the same files
3. **Merge conflict:** Both branches modified `calculatePrice()` in `Product.js` and `calculateTotal()` in `pricing.js`
4. **Resolution strategy:** Combined both — discount applied before tax calculation (`priceWithDiscount = base - discount`, then `tax(priceWithDiscount)`)

**How we demonstrated it:** Through the terminal (not committed to repo). You'd run through this live during your sketch/presentation to show you understand business logic considerations when resolving conflicts.

### Git LFS for PDFs and Large Assets

Configured Git Large File Storage to track binary files:
- `git lfs track "*.pdf"` creates/updates `.gitattributes` with `*.pdf filter=lfs diff=lfs merge=lfs -text`
- The `.gitattributes` file itself should be committed so all collaborators get the LFS rules

---

## What Changed Since Last Session

| Change | Details |
|--------|---------|
| New file: `second-assignment.md` | This document — what we did, why, and how to present it |
| Repo stays on main branch | Clean working tree with no uncommitted changes |
| Feature branch cleaned up | `feature/#1-improve-documentation` was merged via PR #2 and deleted |

---

## What Still Needs Doing (Optional)

- **Git LFS:** Run `git lfs track "*.pdf"` in the repo root, commit `.gitattributes`. Our repo has PDFs already (`PedLabel_UX_Brief_FINAL.pdf`, etc.).
- **Profile README:** Create a `pascal-maker/pascal-maker` repository with a README that appears on your GitHub profile.

---

## How to Present This During Your Sketch Session

When you do the live demo/sketch, focus on these points:

1. **Explain what a merge conflict is** before running any commands — it's when Git can't automatically decide which change wins because both branches touched the same line differently.
2. **Walk through the basic example step by step** — create files, commit, branch, modify different lines (or same line in our case).
3. **Show the conflict markers clearly** — `<<<<<<< HEAD`, `=======`, `>>>>>>>` are Git's way of saying "I can't decide."
4. **For the advanced challenge, explain WHY we combine both branches** instead of just picking one — this shows you understand that business logic (apply discount before tax) matters in real projects.
5. **Mention best practices** at the end: pull frequently, small focused commits, clear communication between team members.
