# Useful git scripts

# Option 1. remove all history and keep only the current state:

# Step 1.
```
git checkout --orphan latest_branch
```

# Step 2.
```
git add -A
```

# Step 3.
```
git commit -am "Clean slate"
```

# Step 4.
```
git branch -D main
```

# Step 5.
```
git branch -m main
```

# Step 6.
```
git push -f origin main
```

# > 🔥 WARNING: This will rewrite history and force-push, erasing all previous commits on the main branch.

# Option 2. Deleting the Repository and Starting Fresh (Alternative)

# If you want to eliminate all history with zero trace, and do not need to preserve stars, issues, or forks:

# 1. Delete the GitHub repository via the Settings > Danger Zone > "Delete this repository".

# 2. Create a new repository with the same name.

# 3. Push only the desired content:

```
rm -rf .git
git init
git remote add origin https://github.com/username/repo.git
git add .
git commit -m "Initial commit"
git push -u origin main
```