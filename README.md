# Simple Node input examples

This repository shows examples of reading user input in Node.js (similar to Python's `input()`), defaulting to the built-in `readline` approach.

## Run

Interactive:

```powershell
node d:\Chat\main.js
```

Non-interactive (pipe):

```powershell
echo Alice | node d:\Chat\main.js
```

## Third-party libraries

If you prefer sync-like behavior or richer prompts, install one of:

- `prompt-sync`: `npm install prompt-sync`
- `readline-sync`: `npm install readline-sync`
- `inquirer`: `npm install inquirer`
- `prompts`: `npm install prompts`

## Publishing to GitHub

1. Create a new repository on GitHub (via the website or `gh repo create`).
2. Add the remote and push:

```powershell
git remote add origin https://github.com/<your-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

Or using `gh` (GitHub CLI):

```powershell
# from the project root
gh repo create <repo-name> --public --source=. --remote=origin --push
```

Replace `<your-username>` and `<repo-name>` accordingly.
