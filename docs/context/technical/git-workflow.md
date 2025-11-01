---
title: Git Workflow & Safety
category: technical
priority: MEDIUM
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 1500
load_when:
  - Committing changes
  - Creating PRs
  - Git operations
dependencies:
  - core/enforcement
tags: [git, commits, prs, version-control]
---

# Git Workflow & Safety

This document defines the Git workflow, safety protocols, and commit standards for the repository.

## Git Safety Protocol

**CRITICAL RULES - NEVER VIOLATE:**

### Absolute Restrictions

1. **NEVER update the git config** (user.name, user.email, etc.)
2. **NEVER run destructive/irreversible git commands** unless explicitly requested:
   - `git push --force` (especially to main/master)
   - `git reset --hard` (except with explicit confirmation)
   - `git clean -fd` without dry-run first
3. **NEVER skip hooks** unless explicitly requested:
   - `--no-verify` flag
   - `--no-gpg-sign` flag
4. **NEVER commit changes** unless user explicitly asks
5. **AVOID `git commit --amend`** unless:
   - User explicitly requested amend, OR
   - Adding edits from pre-commit hook (see below)

### Before Amending Commits

ALWAYS check:
```bash
# 1. Check authorship (don't amend others' commits)
git log -1 --format='%an %ae'

# 2. Check not pushed
git status  # Should show "Your branch is ahead"
```

**If both true**: Safe to amend.
**If either false**: Create NEW commit instead.

## Committing Changes

### Only Commit When

- User explicitly requests: "commit these changes"
- User says: "save this work"
- User asks: "create a commit"

**Never commit proactively** - it's too aggressive and violates user expectations.

### Commit Workflow

**1. Understand Current State (parallel commands):**
```bash
# Run all these in parallel
git status                    # See untracked files
git diff                      # See unstaged changes
git diff --cached             # See staged changes
git log --oneline -5          # Recent commit messages
```

**2. Analyze Changes:**
- Review staged and unstaged changes
- Identify nature of changes (feature, fix, refactor, docs, etc.)
- Draft concise commit message focusing on "why" not "what"

**3. Stage and Commit (parallel):**
```bash
# Add relevant files
git add [files]

# Create commit with Co-Authored-By trailer
git commit -m "$(cat <<'EOF'
[type]: [concise description of why]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Verify commit succeeded
git status
```

**Commit Message Format:**
```
[type]: [description]

[Optional body explaining why this change was made]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Commit Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring
- `docs`: Documentation changes
- `test`: Test additions/modifications
- `chore`: Maintenance tasks

### Pre-Commit Hook Workflow

**If commit fails due to pre-commit hook changes:**

1. **Check if safe to amend:**
   ```bash
   git log -1 --format='%an %ae'  # Check authorship
   git status                      # Check not pushed
   ```

2. **If safe to amend:**
   ```bash
   git add [files modified by hook]
   git commit --amend --no-edit
   ```

3. **If NOT safe to amend:**
   ```bash
   git add [files modified by hook]
   git commit -m "chore: apply pre-commit hook changes"
   ```

**Retry limit**: Only attempt amend ONCE per failed commit.

### Files to Never Commit

**Secrets and credentials:**
- `.env` files
- `credentials.json`
- API keys
- SSH keys
- Database passwords

**Warn user if they request committing these files.**

## Creating Pull Requests

### PR Workflow

**1. Understand Branch State (parallel commands):**
```bash
# Run all in parallel
git status                         # Untracked files
git diff                           # Unstaged changes
git diff --cached                  # Staged changes
git diff main...HEAD               # All changes since divergence
git log --oneline main..HEAD       # All commits in branch
```

**2. Analyze All Changes:**
- Review **ALL commits** (not just latest) that will be in PR
- Understand full scope of changes since branch diverged
- Draft PR summary covering all work

**3. Create PR (parallel operations):**
```bash
# Create branch if needed
git checkout -b [branch-name]

# Push with upstream tracking if needed
git push -u origin [branch-name]

# Create PR using gh CLI with HEREDOC
gh pr create --title "[title]" --body "$(cat <<'EOF'
## Summary
- [bullet point 1]
- [bullet point 2]
- [bullet point 3]

## Test plan
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**PR Title Format:**
- Clear, descriptive (50-60 characters)
- Indicates type of change (feat, fix, refactor, etc.)

**PR Body Format:**
```markdown
## Summary
- Bullet 1: Key change
- Bullet 2: Key change
- Bullet 3: Key change

## Test plan
- [ ] Test item 1
- [ ] Test item 2
- [ ] Test item 3

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Best Practices

1. **Review all commits**: Don't summarize just the latest commit
2. **Comprehensive summary**: Cover all work in the branch
3. **Specific test plan**: Actionable verification steps
4. **Link related issues**: Use `Closes #123` syntax
5. **Return PR URL**: Always provide the PR link after creation

## Git Commands Reference

### Safe Daily Commands

```bash
# Status and diffs
git status
git diff
git diff --cached
git log --oneline -10

# Staging
git add [file]
git add .
git reset HEAD [file]  # Unstage

# Committing
git commit -m "message"
git commit --amend --no-edit  # Only after verification

# Branching
git checkout -b [branch]
git branch -l
git switch [branch]

# Pushing
git push
git push -u origin [branch]
```

### Commands Requiring Extra Caution

```bash
# Force operations (only with explicit user permission)
git push --force              # Warn if pushing to main/master
git reset --hard HEAD~1       # Confirm before running
git clean -fd                 # Dry-run first with -n

# Amend operations (verify authorship first)
git commit --amend
git rebase -i HEAD~3          # NEVER use -i flag (requires interactive input)
```

### Prohibited Commands

```bash
# NEVER run without explicit user request
git config --global user.name
git config --global user.email
git push --force origin main
git reset --hard origin/main
```

## Using `gh` CLI for GitHub Operations

### PR Operations
```bash
# Create PR
gh pr create --title "title" --body "body"

# List PRs
gh pr list

# View PR
gh pr view 123

# Check PR status
gh pr status

# Merge PR
gh pr merge 123
```

### Issue Operations
```bash
# Create issue
gh issue create --title "title" --body "body"

# List issues
gh issue list

# View issue
gh issue view 123
```

### Other Operations
```bash
# View repo
gh repo view

# View comments on PR
gh api repos/owner/repo/pulls/123/comments
```

## Common Workflows

### Feature Development
```bash
# 1. Create branch
git checkout -b feature/description

# 2. Make changes
[edit files]

# 3. Check status
git status

# 4. Stage changes
git add [files]

# 5. Commit
git commit -m "feat: add new feature"

# 6. Push
git push -u origin feature/description

# 7. Create PR
gh pr create --title "feat: add new feature" --body "[description]"
```

### Bug Fix
```bash
# 1. Create branch
git checkout -b fix/issue-description

# 2. Make fixes
[edit files]

# 3. Commit
git commit -m "fix: resolve issue with X"

# 4. Push and PR
git push -u origin fix/issue-description
gh pr create --title "fix: resolve issue with X" --body "[description]"
```

### Quick Fix on Main
```bash
# Only for trivial changes after user approval
git add [file]
git commit -m "fix: typo in documentation"
git push
```

## Troubleshooting

### Commit Failed Due to Pre-Commit Hook

**Scenario**: Pre-commit hook modified files, commit failed.

**Solution**:
```bash
# 1. Check if safe to amend
git log -1 --format='%an %ae'
git status

# 2. If safe (your commit, not pushed)
git add [modified files]
git commit --amend --no-edit

# 3. If NOT safe
git add [modified files]
git commit -m "chore: apply pre-commit hook changes"
```

### Accidentally Staged Wrong Files

```bash
# Unstage specific file
git reset HEAD [file]

# Unstage all
git reset HEAD
```

### Need to Edit Last Commit Message

```bash
# Only if not pushed and you're the author
git commit --amend -m "new message"
```

### Accidentally Committed Secret

```bash
# If not pushed yet
git reset --soft HEAD~1
git reset HEAD [secret-file]
echo "[secret-file]" >> .gitignore

# If pushed - alert user immediately, may need git-filter-repo
```

## Related Documentation

- **Enforcement Rules**: `docs/context/core/enforcement.md`
- **Pre-Commit Hooks**: `.git/hooks/pre-commit`
- **MANIFEST.json**: Repository file registry
