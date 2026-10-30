# Daily Dev Workflow

A tiny Python CLI for planning and recording real development work. It helps you
keep a useful record of what you built, fixed, tested, or documented. It does not
manufacture commits, backdate activity, or promise a particular GitHub contribution
count.

## Requirements

- Python 3.10+
- Git
- A GitHub account and an authenticated Git remote when you are ready to publish

## Run locally

```bash
python -m devlog add "Add validation for malformed configuration files"
python -m devlog list
python -m devlog complete 1 --result "Added validation and tests for malformed config input"
python -m devlog list --all
python -m devlog report --days 7
python -m unittest discover -s tests -v
```

The first command creates `data/worklog.json`. This file is ignored by Git by
default so your personal task log is not accidentally published. Remove that
ignore rule if you intentionally want to share your work log.

## Publish as a new GitHub repository

1. Create an empty repository on GitHub named `daily-dev-workflow` (do not add a
   README or license there, because this project already has them).
2. In this folder, run:

```bash
git init
git add .
git commit -m "chore: create daily development work log"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/daily-dev-workflow.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. GitHub CLI can also create
the remote repository if installed and authenticated:

```bash
gh repo create daily-dev-workflow --public --source=. --remote=origin --push
```

## Building a healthy contribution history

Use the tool to plan and record real tasks, then make focused code, test,
documentation, or maintenance changes in the repository. Commit coherent changes
when they are ready for review. A task-log entry alone is not a substitute for
meaningful project work.

GitHub contribution squares are governed by GitHub's eligibility rules; 50 commits
do not guarantee 50 squares. Commits should use an email associated with your
GitHub account, and activity must meet GitHub's repository and branch rules.
See: https://docs.github.com/en/account-and-profile/concepts/contributions-on-your-profile

## Safety

- No GitHub token is needed by this local CLI.
- Do not put access tokens or passwords in this repository.
- Review `git diff` before committing.
- Keep tests passing and avoid splitting trivial changes just to inflate activity.

## License

MIT
