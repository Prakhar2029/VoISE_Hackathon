# Git Branch Management Guide 🌿

A comprehensive guide to creating, managing, and merging branches in Git with real-world examples.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Creating Branches](#creating-branches)
3. [Switching Branches](#switching-branches)
4. [Listing Branches](#listing-branches)
5. [Merging Branches](#merging-branches)
6. [Rebasing Branches](#rebasing-branches)
7. [Deleting Branches](#deleting-branches)
8. [Advanced Branch Management](#advanced-branch-management)
9. [Best Practices](#best-practices)

---

## Introduction

Branches are fundamental to Git workflows. They allow you to work on features independently without affecting the main codebase. This guide covers essential branch operations with practical examples.

---

## Creating Branches

### 1. Create a New Branch

**Command:**
```bash
git branch <branch-name>
```

**Example:**
```bash
git branch feature/user-authentication
```

Creates a new branch called `feature/user-authentication` pointing to the current commit.

### 2. Create a Branch from a Specific Commit

**Command:**
```bash
git branch <branch-name> <commit-sha>
```

**Example:**
```bash
git branch hotfix/security-patch abc1234
```

Creates a branch starting from commit `abc1234`.

### 3. Create and Switch to a New Branch (One Step)

**Command:**
```bash
git checkout -b <branch-name>
```

**Example:**
```bash
git checkout -b feature/payment-integration
```

This combines creating and switching to the new branch.

**Modern Alternative (Git 2.23+):**
```bash
git switch -c <branch-name>
```

**Example:**
```bash
git switch -c feature/payment-integration
```

### 4. Create a Branch from a Remote Branch

**Command:**
```bash
git checkout -b <branch-name> origin/<remote-branch>
```

**Example:**
```bash
git checkout -b develop origin/develop
```

Tracks and creates a local branch from a remote branch.

---

## Switching Branches

### 1. Switch to an Existing Branch

**Command:**
```bash
git checkout <branch-name>
```

**Example:**
```bash
git checkout main
```

Switches to the `main` branch.

**Modern Alternative:**
```bash
git switch <branch-name>
```

**Example:**
```bash
git switch develop
```

### 2. Switch to Previous Branch

**Command:**
```bash
git checkout -
```

Switches to the branch you were previously on. Useful for toggling between two branches.

---

## Listing Branches

### 1. List Local Branches

**Command:**
```bash
git branch
```

**Output Example:**
```
  develop
* main
  feature/api
  feature/ui
```

The `*` indicates the currently active branch.

### 2. List All Branches (Local + Remote)

**Command:**
```bash
git branch -a
```

**Output Example:**
```
  develop
* main
  feature/api
  remotes/origin/main
  remotes/origin/develop
  remotes/origin/feature/deployment
```

### 3. List Branches with Last Commit Info

**Command:**
```bash
git branch -v
```

**Output Example:**
```
  develop               abc1234 Fix database connection
* main                  def5678 Merge PR #42
  feature/api           ghi9012 Add REST endpoints
```

### 4. List Merged Branches

**Command:**
```bash
git branch --merged
```

Shows branches that have been merged into the current branch. Useful before cleanup.

### 5. List Unmerged Branches

**Command:**
```bash
git branch --no-merged
```

Shows branches that have not been merged yet.

---

## Merging Branches

### 1. Fast-Forward Merge

**Command:**
```bash
git checkout <target-branch>
git merge <source-branch>
```

**Example:**
```bash
git checkout main
git merge feature/user-authentication
```

When the target branch hasn't changed, Git simply moves the pointer forward (fast-forward merge).

**Visual:**
```
Before:
main          →  C1
feature-auth  →  C2 (C2 is ahead of C1)

After:
main          →  C2
feature-auth  →  C2
```

### 2. Three-Way Merge

**Command:**
```bash
git checkout main
git merge feature/payment-integration
```

When both branches have diverged, Git creates a merge commit.

**Visual:**
```
Before:
main     →  C1 → C3
feature  →  C2 → C4

After:
main     →  C1 → C3 → M (merge commit)
             ↘         ↗
feature  →  C2 → C4
```

### 3. Merge with Custom Commit Message

**Command:**
```bash
git merge <branch-name> -m "Custom merge message"
```

**Example:**
```bash
git merge feature/api -m "Merge API integration feature"
```

### 4. No-Fast-Forward Merge

**Command:**
```bash
git merge --no-ff <branch-name> -m "Merge branch message"
```

**Example:**
```bash
git merge --no-ff feature/database -m "Merge database schema updates"
```

Forces creation of a merge commit even if a fast-forward is possible. Useful for maintaining clear branch history.

### 5. Handling Merge Conflicts

When merging branches with conflicting changes:

**Step 1:** Identify conflicts
```bash
git merge feature/conflicting-branch
# Output: CONFLICT (content): Merge conflict in file.txt
```

**Step 2:** View conflicted files
```bash
git status
```

**Step 3:** Resolve conflicts manually
Open the conflicted file and look for:
```
<<<<<<< HEAD
  Your changes from main
=======
  Changes from feature branch
>>>>>>> feature/conflicting-branch
```

Choose which changes to keep or combine both.

**Step 4:** Mark as resolved
```bash
git add file.txt
```

**Step 5:** Complete the merge
```bash
git commit -m "Merge feature/conflicting-branch, resolve conflicts"
```

---

## Rebasing Branches

Rebasing rewrites commit history by replaying commits on top of another branch. Use with caution on shared branches.

### 1. Basic Rebase

**Command:**
```bash
git checkout <feature-branch>
git rebase <base-branch>
```

**Example:**
```bash
git checkout feature/new-feature
git rebase main
```

Replays all commits from `feature/new-feature` that aren't in `main` on top of `main`.

**Visual:**
```
Before:
main   →  C1 → C2
feature →  C3 → C4

After Rebase:
main   →  C1 → C2
feature →  C1 → C2 → C3' → C4'
```

### 2. Interactive Rebase

**Command:**
```bash
git rebase -i <base-branch>
```

**Example:**
```bash
git rebase -i main
```

Opens an editor to modify, squash, or reorder commits. Options include:
- `pick` - Use commit
- `reword` - Use commit but edit message
- `squash` - Combine with previous commit
- `drop` - Remove commit

### 3. Rebase with Continue (Resolving Conflicts)

If conflicts occur during rebase:

```bash
# Fix conflicts
git add .

# Continue rebase
git rebase --continue

# Or abort rebase
git rebase --abort
```

### 4. Merge vs. Rebase Comparison

**Merge Approach:**
```bash
git checkout main
git merge feature/auth
```
- Preserves complete history
- Creates merge commits
- Cleaner for public branches

**Rebase Approach:**
```bash
git checkout feature/auth
git rebase main
git checkout main
git merge --ff-only feature/auth
```
- Linear, cleaner history
- Rewrites commits (avoid on public branches)
- Better for local feature branches

---

## Deleting Branches

### 1. Delete a Local Branch

**Command:**
```bash
git branch -d <branch-name>
```

**Example:**
```bash
git branch -d feature/user-authentication
```

Safe deletion - warns if not fully merged.

### 2. Force Delete a Local Branch

**Command:**
```bash
git branch -D <branch-name>
```

**Example:**
```bash
git branch -D experimental-feature
```

Forces deletion regardless of merge status.

### 3. Delete a Remote Branch

**Command:**
```bash
git push origin --delete <branch-name>
```

**Example:**
```bash
git push origin --delete feature/old-feature
```

Removes the branch from the remote repository.

### 4. Cleanup Remote References

**Command:**
```bash
git remote prune origin
```

Removes stale remote-tracking branches that no longer exist on the remote.

---

## Advanced Branch Management

### 1. Rename a Branch

**Rename Current Branch:**
```bash
git branch -m <new-name>
```

**Example:**
```bash
git branch -m feature/auth-system
```

**Rename Specific Branch:**
```bash
git branch -m <old-name> <new-name>
```

**Example:**
```bash
git branch -m feature/old-auth feature/new-auth
```

### 2. View Branch Tracking

**Command:**
```bash
git branch -vv
```

Shows which remote branch each local branch tracks.

**Output Example:**
```
  develop                    abc1234 [origin/develop] Update docs
  feature/api                def5678 [origin/feature/api: ahead 2] Add endpoints
* main                        ghi9012 [origin/main] Initial commit
```

### 3. Set Upstream Branch

**Command:**
```bash
git branch -u <remote>/<branch> <local-branch>
```

**Example:**
```bash
git branch -u origin/develop develop
```

Links a local branch to track a remote branch.

### 4. Cherry-Pick Commits

Apply specific commits from one branch to another without full merge.

**Command:**
```bash
git cherry-pick <commit-sha>
```

**Example:**
```bash
git checkout main
git cherry-pick abc1234
```

Applies commit `abc1234` to the current branch.

**Cherry-Pick Multiple Commits:**
```bash
git cherry-pick abc1234 def5678 ghi9012
```

---

## Best Practices

### 1. **Naming Conventions**

Use clear, descriptive names:
```
✅ feature/user-login
✅ bugfix/header-alignment
✅ hotfix/critical-security-patch
✅ docs/api-documentation

❌ feature1
❌ fix-stuff
❌ temp-branch
```

### 2. **Branching Strategy**

Follow a structured strategy like Git Flow:
- `main` - Production releases
- `develop` - Integration branch
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Critical production fixes

### 3. **Keep Branches Up-to-Date**

Regularly sync with main branch:
```bash
git fetch origin
git rebase origin/main
```

### 4. **Delete Merged Branches**

Clean up after merging:
```bash
# Local cleanup
git branch -d feature/completed-feature

# Remote cleanup
git push origin --delete feature/completed-feature
```

### 5. **Use Pull Requests**

Always use PRs for code review:
```bash
git push origin feature/new-feature
# Then create PR on GitHub/GitLab
```

### 6. **Commit Messages**

Write clear commit messages:
```bash
git commit -m "feature: Add user authentication system

- Implement JWT-based authentication
- Add password hashing with bcrypt
- Create login and signup endpoints"
```

### 7. **Avoid Large, Long-Lived Branches**

Keep features small and merge frequently to reduce conflicts.

### 8. **Never Force Push to Shared Branches**

```bash
❌ git push --force origin main
✅ git push origin feature/my-feature (force push only on personal branches)
```

---

## Quick Reference Table

| Task | Command |
|------|---------|
| Create branch | `git branch <name>` |
| Create & switch | `git checkout -b <name>` |
| Switch branch | `git checkout <name>` |
| List all branches | `git branch -a` |
| Merge branch | `git merge <name>` |
| Rebase branch | `git rebase <name>` |
| Delete local branch | `git branch -d <name>` |
| Delete remote branch | `git push origin --delete <name>` |
| Rename branch | `git branch -m <new-name>` |
| View tracking | `git branch -vv` |

---

## Conclusion

Mastering Git branches is essential for collaborative development. Use this guide as a reference and practice these commands regularly. Remember to keep your branching strategy clear and consistent with your team.

**Happy coding! 🚀**
