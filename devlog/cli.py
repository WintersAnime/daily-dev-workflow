"""A small, honest work log for tracking real development work."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_FILE = Path("data/worklog.json")


def load_tasks(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"Cannot read work log {path}: {exc}") from exc
    if not isinstance(data, list):
        raise ValueError("Work log must contain a JSON list.")
    return data


def save_tasks(path: Path, tasks: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(tasks, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def add_task(path: Path, description: str) -> dict:
    description = description.strip()
    if len(description) < 8:
        raise ValueError("Describe the real task in at least 8 characters.")
    tasks = load_tasks(path)
    task_id = max((t["id"] for t in tasks), default=0) + 1
    task = {
        "id": task_id,
        "description": description,
        "status": "open",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "completed_at": None,
        "result": None,
    }
    tasks.append(task)
    save_tasks(path, tasks)
    return task


def complete_task(path: Path, task_id: int, result: str) -> dict:
    result = result.strip()
    if len(result) < 8:
        raise ValueError("Describe what you actually changed or learned (at least 8 characters).")
    tasks = load_tasks(path)
    for task in tasks:
        if task["id"] == task_id:
            if task["status"] == "done":
                raise ValueError(f"Task #{task_id} is already complete.")
            task["status"] = "done"
            task["result"] = result
            task["completed_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            save_tasks(path, tasks)
            return task
    raise ValueError(f"Task #{task_id} was not found.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="devlog", description="Track real development work.")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="Work-log JSON path")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Record a task you intend to do")
    add.add_argument("description")

    done = sub.add_parser("complete", help="Record the result of completed work")
    done.add_argument("task_id", type=int)
    done.add_argument("--result", required=True)

    listing = sub.add_parser("list", help="List tracked tasks")
    listing.add_argument("--all", action="store_true", help="Include completed tasks")

    report = sub.add_parser("report", help="Show a contribution-work summary")
    report.add_argument("--days", type=int, default=7)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "add":
            task = add_task(args.file, args.description)
            print(f"Added task #{task['id']}: {task['description']}")
        elif args.command == "complete":
            task = complete_task(args.file, args.task_id, args.result)
            print(f"Completed task #{task['id']}: {task['description']}")
        elif args.command == "list":
            tasks = load_tasks(args.file)
            if not args.all:
                tasks = [t for t in tasks if t["status"] == "open"]
            if not tasks:
                print("No matching tasks.")
            for task in tasks:
                print(f"#{task['id']} [{task['status']}] {task['description']}")
                if task["result"]:
                    print(f"    Result: {task['result']}")
        elif args.command == "report":
            if args.days < 1:
                parser.error("--days must be at least 1")
            tasks = load_tasks(args.file)
            done = [t for t in tasks if t["status"] == "done"]
            print(f"Tasks recorded: {len(tasks)}")
            print(f"Completed: {len(done)}")
            print(f"Open: {len(tasks) - len(done)}")
            print("Note: this is a work log, not a count of GitHub profile contributions.")
        return 0
    except (ValueError, KeyError, OSError) as exc:
        parser.error(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
