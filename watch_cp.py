from pathlib import Path
import sys
import time

import run_judge


POLL_SECONDS = 0.30


def snapshot(paths: list[Path]) -> dict[Path, int | None]:
    state: dict[Path, int | None] = {}
    for path in paths:
        state[path] = path.stat().st_mtime_ns if path.exists() else None
    return state


def detect_change(
    previous: dict[Path, int | None], current: dict[Path, int | None]
) -> str | None:
    for path in previous:
        if previous[path] != current[path]:
            return path.name
    return None


def run_once(reason: str, code_file: Path) -> None:
    now = time.strftime("%H:%M:%S")
    print(f"\n[{now}] {reason}")
    exit_code = run_judge.main(code_file)
    if exit_code == 0:
        print(f"[{now}] Run complete")
    else:
        print(f"[{now}] Run complete (status {exit_code})")


def main() -> int:
    arg_file = sys.argv[1] if len(sys.argv) > 1 else None
    code_file = run_judge.resolve_code_file(arg_file)
    watch_files = [
        code_file,
        run_judge.INPUT_FILE,
        run_judge.EXPECTED_FILE,
    ]

    print("CP watch mode started.")
    print(f"Watching: {code_file.name}, inputs.txt, expected.txt")
    print("Save a file to auto-run. Press Ctrl+C to stop.")

    previous = snapshot(watch_files)
    run_once("Initial run", code_file)

    try:
        while True:
            time.sleep(POLL_SECONDS)
            current = snapshot(watch_files)
            changed_file = detect_change(previous, current)
            if changed_file is not None:
                run_once(f"Change detected in {changed_file}", code_file)
                previous = current
    except KeyboardInterrupt:
        print("\nWatch mode stopped.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
