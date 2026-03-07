#!/usr/bin/env sh
set -eu

REPO_URL="https://github.com/Arpit955-ux/CHATBOT.git"
REPO_PUSH_URL="https://Arpit955-ux@github.com/Arpit955-ux/CHATBOT.git"

cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

if ! command -v git >/dev/null 2>&1; then
  echo "Error: git is not installed."
  exit 1
fi

if [ ! -d .git ]; then
  echo "Error: this folder is not a git repository."
  exit 1
fi

git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_PUSH_URL"
git config credential.username Arpit955-ux

printf "GitHub Personal Access Token (repo scope): "
stty -echo
read -r GITHUB_PAT
stty echo
printf "\n"

if [ -z "$GITHUB_PAT" ]; then
  echo "Error: token cannot be empty."
  exit 1
fi

git branch -M main

# Store credentials for this host via git's credential helper.
printf "protocol=https\nhost=github.com\nusername=Arpit955-ux\npassword=%s\n\n" "$GITHUB_PAT" | git credential approve

# Push current HEAD to main.
git push -u "$REPO_URL" HEAD:main

echo "Push completed successfully."
