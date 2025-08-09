# Git Branch Strategy for Semantic-Release Workflow

This documentation outlines the git branching strategy optimized for semantic-release automation and small team/solo development.

## Branch Structure Overview

### Persistent Branches

- **`main`** - Production releases, protected branch
- **`develop`** - Integration branch for ongoing development

### Temporary Branches

- **`release-vX.Y.Z`** - Release preparation, deleted after merge
- **`feature/*`** - Individual features, deleted after merge to develop

## Workflow Strategy Summary

| Transition | Method | Reason |
|------------|--------|---------|
| **Feature → Develop** | Direct merge | Fast iteration for small teams |
| **Develop → Release** | Cherry-picking | Selective commit inclusion |
| **Release → Main** | Pull Request | Approval gate + semantic-release trigger |

## Detailed Workflows

### 1. Feature Development

```bash
# Create and develop feature
git checkout develop
git checkout -b feature/user-authentication
# ... make changes ...
git add . && git commit -m "feat: add user authentication"

# Merge to develop (direct merge for speed)
git checkout develop
git merge --squash feature/user-authentication
git commit -m "feat(user-authentication): [describe the changes]"
git push origin develop

# Cleanup feature branch
git branch -d feature/user-authentication
git push origin --delete feature/user-authentication
```

### 2. Release Preparation (Cherry-Picking)

```bash
# Create fresh release branch from main
git checkout main
git pull origin main
git checkout -b release-v1.2.0

# View available commits in develop
git log develop --oneline --graph

# Cherry-pick specific commits for release
git cherry-pick abc1234  # User authentication feature
git cherry-pick def5678  # Password reset feature
git cherry-pick ghi9012  # Critical bug fix
# Skip experimental features not ready for release

# Push release branch
git push origin release-v1.2.0
```

**Why Cherry-Picking over Full Merge:**

- ✅ **Selective releases** - Choose exactly which features to include
- ✅ **Quality control** - Exclude work-in-progress or experimental code
- ✅ **Clean history** - No merge commits cluttering release branch
- ✅ **Flexibility** - Can include commits from multiple feature branches

### 3. Release Execution

```bash
# Create Pull Request: release-v1.2.0 → main
# This can be done via GitHub UI or CLI:
gh pr create --base main --head release-v1.2.0 \
  --title "Release v1.2.0" \
  --body "## Release v1.2.0

### Features Included:
- User authentication (abc1234)
- Password reset functionality (def5678)  
- Critical login bug fix (ghi9012)

### Testing:
- [ ] All tests passing
- [ ] Manual testing completed
- [ ] Security review completed"

# After PR approval and merge:
# - Semantic-release automatically runs
# - Version tag created
# - GitHub release published
# - Contributors notified
```

### 4. Post-Release Cleanup

```bash
# After release PR is merged to main
git checkout main
git pull origin main

# Sync develop with released changes
git checkout develop  
git rebase main  # Include any release-specific fixes
git push origin develop

# Delete release branch
git branch -d release-v1.2.0
git push origin --delete release-v1.2.0
```

## Branch Lifecycle Management

### Persistent Branches (Never Delete)

- **`main`** - Always keep, production history
- **`develop`** - Always keep, continuous integration point

### Temporary Branches (Delete After Use)

- **`release-vX.Y.Z`** - Delete after successful merge to main
- **`feature/*`** - Delete after merge to develop

### Release Branch Naming

```bash
# Recommended naming convention:
release-v1.2.0    # Major.Minor.Patch
release-v2.0.0    # Major version
release-hotfix    # Emergency fixes
```

## Complete Release Cycle Example

```bash
# === DEVELOPMENT PHASE ===
# Feature 1
git checkout develop
git checkout -b feature/login
# ... develop ...
git checkout develop
git merge --squash feature/login
git commit -m "feat(login): [describe the changes]"
git branch -d feature/login
git push origin develop

# Feature 2  
git checkout -b feature/dashboard
# ... develop ...
git checkout develop
git merge --squash feature/dashboard
git commit -m "feat(dashboard): [describe the changes]"
git branch -d feature/dashboard
git push origin develop

# === RELEASE PHASE ===
# Prepare release
git checkout main && git pull
git checkout -b release-v1.2.0

# Select commits for release
git log develop --oneline  # Review available commits
git cherry-pick abc123     # Include login feature
git cherry-pick def456     # Include dashboard feature
# Skip xyz789 (experimental feature not ready)

git push origin release-v1.2.0

# Create PR: release-v1.2.0 → main
# After merge (triggers semantic-release):

# === CLEANUP PHASE ===
git checkout main && git pull
git checkout develop && git merge main
git push origin develop
git branch -d release-v1.2.0
git push origin --delete release-v1.2.0

# === CONTINUE DEVELOPMENT ===
git checkout -b feature/next-feature
# ... cycle continues ...
```

## Team-Size Specific Recommendations

### Small Team / Solo Development (Recommended)

```bash
# Fast iteration workflow
Feature → Develop: Direct merge (no PR overhead)
Develop → Release: Cherry-pick (selective releases)
Release → Main: Pull Request (approval + semantic-release)
```

**Benefits:**

- ✅ **Speed** - Minimal overhead for feature integration
- ✅ **Flexibility** - Easy to experiment and iterate
- ✅ **Quality gate** - Final approval on releases
- ✅ **Automation** - Semantic-release handles versioning

### Larger Teams

```bash
# Code review workflow  
Feature → Develop: Pull Request (code review)
Develop → Release: Cherry-pick (selective releases)
Release → Main: Pull Request (release approval)
```

**Additional considerations:**

- Branch protection rules on `develop`
- Required reviewers for feature PRs
- Automated testing on all branches

## Cherry-Picking Best Practices

### Selecting Commits for Release

```bash
# Good commits to include:
✅ Completed features
✅ Bug fixes  
✅ Performance improvements
✅ Security updates
✅ Documentation updates

# Commits to skip:
❌ Work-in-progress features
❌ Experimental code
❌ Debug commits  
❌ "WIP" or "temp" commits
❌ Breaking changes without migration path
```

### Cherry-Pick Commands

```bash
# Basic cherry-pick
git cherry-pick <commit-hash>

# Cherry-pick without commit (review first)
git cherry-pick -n <commit-hash>

# Cherry-pick range of commits
git cherry-pick <start-hash>^..<end-hash>

# Cherry-pick with custom commit message
git cherry-pick <commit-hash> --edit

# Handle conflicts during cherry-pick
git cherry-pick <commit-hash>
# ... resolve conflicts ...
git add .
git cherry-pick --continue
```

## Integration with Semantic-Release

### How It Works

1. **Release branch merged to main** → Triggers semantic-release workflow
2. **Semantic-release analyzes commits** → Determines version bump (major/minor/patch)
3. **Automatic actions:**
   - Creates git tag (e.g., `v1.2.0`)
   - Generates changelog from commit messages  
   - Creates GitHub release
   - Comments on PRs/issues included in release
   - Triggers build/artifact workflows

### Commit Message Format (Important)

Use conventional commits for proper semantic-release detection:

```bash
feat: add user authentication system       # Minor version bump
fix: resolve login timeout issue          # Patch version bump  
perf: improve database query performance   # Major version bump
docs: update API documentation            # No version bump
chore: update dependencies                # No version bump

# Breaking changes (major version bump)
feat!: redesign authentication API
feat: new auth system

BREAKING CHANGE: Authentication API completely redesigned
```

## Automation and Shortcuts

### Helpful Git Aliases

```bash
# Add to ~/.gitconfig
[alias]
    # Quick branch switching
    co = checkout
    sw = switch

    # Release workflow shortcuts
    release-start = "!f() { git checkout main && git pull && git checkout -b release-v$1; }; f"
    release-clean = "!f() { git checkout main && git pull && git checkout develop && git merge main && git push; }; f"

    # Cherry-pick helpers
    cp = cherry-pick
    cpc = cherry-pick --continue
    cpa = cherry-pick --abort

    # Log helpers
    commits = log --oneline --graph --decorate
    release-commits = "!f() { git log develop --oneline --since='$1 days ago'; }; f"
```

### Release Checklist Script

```bash
#!/bin/bash
# release-checklist.sh

echo "🚀 Release Checklist"
echo "1. ✅ All features tested and ready?"
echo "2. ✅ Documentation updated?"  
echo "3. ✅ Breaking changes documented?"
echo "4. ✅ Security review completed?"
echo "5. ✅ Performance testing done?"
echo ""
echo "Ready to create release branch? (y/n)"
read -r response
if [[ $response == "y" ]]; then
    echo "🌟 Creating release branch..."
    git checkout main && git pull
    echo "Enter version (e.g., 1.2.0):"
    read -r version
    git checkout -b "release-v$version"
    echo "✨ Release branch release-v$version created!"
    echo "Next steps:"
    echo "1. Cherry-pick commits: git cherry-pick <hash>"
    echo "2. Push branch: git push origin release-v$version"  
    echo "3. Create PR to main"
fi
```

## Troubleshooting

### Common Issues and Solutions

**Cherry-pick conflicts:**

```bash
# When conflicts occur during cherry-pick
git status                    # See conflicted files
# ... resolve conflicts manually ...
git add .
git cherry-pick --continue   # Complete the cherry-pick
```

**Accidentally included wrong commit:**

```bash
# Remove last commit from release branch
git reset --hard HEAD~1

# Or use interactive rebase to edit history
git rebase -i HEAD~3
```

**Need to add forgotten commit:**

```bash
# Add more commits to existing release branch
git cherry-pick <additional-commit>
git push origin release-v1.2.0 --force-with-lease
```

**Semantic-release not triggering:**

```bash
# Verify workflow file
cat .github/workflows/semantic-release.yaml

# Check if push to main triggered workflow
# Go to Actions tab in GitHub repository
# Verify semantic-release job ran successfully
```

## Branch Protection Setup (Optional)

For additional safety, configure branch protection:

### Main Branch Protection

- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Require branches to be up to date  
- ✅ Restrict pushes (admins only)
- ✅ Do not allow force pushes

### Develop Branch Protection (Optional)

- ✅ Require status checks to pass
- ✅ Allow direct pushes (for fast iteration)
- ❌ Don't require PR reviews (for small teams)

## Summary

This git branch strategy provides:

- ✅ **Controlled releases** - Choose exactly what goes into each release
- ✅ **Quality assurance** - Approval gates and testing on release branches  
- ✅ **Automation** - Semantic-release handles versioning and notifications
- ✅ **Clean history** - Clear separation between development and production
- ✅ **Team scalability** - Works for solo developers and larger teams
- ✅ **Flexibility** - Easy to adapt for different project needs

The combination of cherry-picking for selective releases and semantic-release for automation creates an optimal workflow for maintaining high-quality software releases.
