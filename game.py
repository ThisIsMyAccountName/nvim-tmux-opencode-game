#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
MISSIONS_ROOT = ROOT / "missions"
STATE_ROOT = ROOT / ".dojo"
SANDBOX_ROOT = STATE_ROOT / "sandboxes"
STATE_FILE = STATE_ROOT / "state.json"
PROGRESS_FILE = STATE_ROOT / "progress.json"
GLOBAL_TIPS_FILE = ROOT / "GLOBAL_TIPS.md"
GLOBAL_TIPS_SHORT_FILE = ROOT / "GLOBAL_TIPS_SHORT.md"


@dataclass
class Mission:
    id: str
    chapter: str
    order: int
    title: str
    brief: str
    objectives: list[str]
    start_file: str
    tips_file: str
    checks: list[dict[str, Any]]
    path: Path


def ensure_state_dirs() -> None:
    STATE_ROOT.mkdir(exist_ok=True)
    SANDBOX_ROOT.mkdir(exist_ok=True)


def read_json_file(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def write_json_file(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def load_missions() -> list[Mission]:
    missions: list[Mission] = []
    for mission_file in sorted(MISSIONS_ROOT.glob("*/mission.json")):
        raw = read_json_file(mission_file, None)
        if not isinstance(raw, dict):
            continue
        try:
            raw_objectives = raw.get("objectives", [])
            objectives = []
            if isinstance(raw_objectives, list):
                objectives = [str(item).strip() for item in raw_objectives if str(item).strip()]
            missions.append(
                Mission(
                    id=str(raw["id"]),
                    chapter=str(raw.get("chapter", "")).strip(),
                    order=int(raw.get("order", 0) or 0),
                    title=str(raw["title"]),
                    brief=str(raw.get("brief", "")).strip(),
                    objectives=objectives,
                    start_file=str(raw.get("start_file", "")).strip(),
                    tips_file=str(raw.get("tips_file", "")).strip(),
                    checks=list(raw.get("checks", [])),
                    path=mission_file.parent,
                )
            )
        except (KeyError, ValueError, TypeError):
            continue

    def mission_sort_key(mission: Mission) -> tuple[int, int, str]:
        chapter_index = 999
        if mission.id.startswith("M") and len(mission.id) >= 3:
            try:
                chapter_index = int(mission.id[1:3])
            except ValueError:
                chapter_index = 999
        order_index = mission.order if mission.order > 0 else 999
        return (chapter_index, order_index, mission.id)

    missions.sort(key=mission_sort_key)
    return missions


def find_mission(missions: list[Mission], mission_id: str) -> Mission | None:
    for mission in missions:
        if mission.id == mission_id:
            return mission
    return None


def load_state() -> dict[str, Any]:
    data = read_json_file(STATE_FILE, {})
    if not isinstance(data, dict):
        return {}
    return data


def save_state(state: dict[str, Any]) -> None:
    write_json_file(STATE_FILE, state)


def load_progress() -> dict[str, Any]:
    data = read_json_file(PROGRESS_FILE, {"completed": []})
    if not isinstance(data, dict):
        return {"completed": []}
    completed = data.get("completed", [])
    if not isinstance(completed, list):
        completed = []
    return {"completed": list(completed)}


def save_progress(progress: dict[str, Any]) -> None:
    write_json_file(PROGRESS_FILE, progress)


def sandbox_path(mission_id: str) -> Path:
    return SANDBOX_ROOT / mission_id


def current_tmux_session() -> str:
    if shutil.which("tmux") is None or not os.environ.get("TMUX"):
        return ""
    result = subprocess.run(
        ["tmux", "display-message", "-p", "#S"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def write_stage_control_script(sandbox: Path) -> None:
    script_path = sandbox / "stage"
    game_path = shlex.quote(str(ROOT / "game.py"))
    sandbox_value = shlex.quote(str(sandbox))
    script = f"""#!/usr/bin/env sh
set -e

SANDBOX={sandbox_value}

if [ $# -eq 0 ]; then
  cat <<'EOF'
Available commands:
  ./stage check
  ./stage reset
  ./stage next
  ./stage quit
EOF
  exit 0
fi

if [ ! -x ./stage ] && [ -x ../stage ]; then
  cd ..
fi

if [ "$(pwd)" != "$SANDBOX" ]; then
  cd "$SANDBOX"
fi

exec python3 {game_path} "$@"
"""
    script_path.write_text(script, encoding="utf-8")
    script_path.chmod(0o755)


def write_workspace_stage_script(workspace: Path) -> None:
    script_path = workspace / "stage"
    script = """#!/usr/bin/env sh
set -e

cd "$(dirname "$0")/.."
exec ./stage "$@"
"""
    script_path.write_text(script, encoding="utf-8")
    script_path.chmod(0o755)


def write_commands_file(mission: Mission, sandbox: Path) -> None:
    lines = [f"# {mission.id} - {mission.title}"]
    if mission.brief:
        lines.extend(["", mission.brief])
    lines.extend(["", "Goal:"])
    if mission.objectives:
        lines.extend([f"- {item}" for item in mission.objectives])
    else:
        lines.append("- Complete mission checks.")
    lines.extend(
        [
            "",
            "Commands:",
            "- ./stage check",
            "- ./stage reset",
            "- ./stage next",
            "- ./stage quit",
        ]
    )
    (sandbox / "COMMANDS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def setup_workspace(mission: Mission) -> Path:
    src = mission.path
    sandbox = sandbox_path(mission.id)
    if sandbox.exists():
        shutil.rmtree(sandbox)
    shutil.copytree(src, sandbox)

    workspace = sandbox / "workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    if GLOBAL_TIPS_FILE.exists():
        shutil.copy2(GLOBAL_TIPS_FILE, sandbox / "GLOBAL_TIPS.md")
    if GLOBAL_TIPS_SHORT_FILE.exists():
        shutil.copy2(GLOBAL_TIPS_SHORT_FILE, sandbox / "GLOBAL_TIPS_SHORT.md")
    write_stage_control_script(sandbox)
    write_workspace_stage_script(workspace)
    write_commands_file(mission, sandbox)
    return workspace


def tmux_session_exists(session_name: str) -> bool:
    result = subprocess.run(
        ["tmux", "has-session", "-t", session_name],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def kill_tmux_session(session_name: str) -> None:
    if session_name and shutil.which("tmux") is not None and tmux_session_exists(session_name):
        subprocess.run(["tmux", "kill-session", "-t", session_name], check=False)


def remove_sandbox(path: Path) -> None:
    if not path.exists():
        return
    try:
        cwd = Path.cwd().resolve()
        cwd.relative_to(path.resolve())
        os.chdir(ROOT)
    except ValueError:
        pass
    except FileNotFoundError:
        os.chdir(ROOT)
    shutil.rmtree(path)


def create_tmux_stage_session(session_name: str, sandbox: Path, start_file: str) -> None:
    nvim_target = f"workspace/{start_file}" if start_file else "workspace"
    subprocess.run(
        [
            "tmux",
            "new-session",
            "-d",
            "-s",
            session_name,
            "-c",
            str(sandbox),
            f"nvim -n {nvim_target}",
        ],
        check=True,
    )
    subprocess.run(
        [
            "tmux",
            "split-window",
            "-h",
            "-t",
            session_name,
            "-c",
            str(sandbox),
            "sh -lc 'clear; printf \"CURRENT MISSION\\n===============\\n\"; cat COMMANDS.md; if [ -f TIPS.md ]; then printf \"\\nMISSION-SPECIFIC TIPS\\n=====================\\n\"; cat TIPS.md; fi; if [ -f GLOBAL_TIPS_SHORT.md ]; then printf \"\\n\"; cat GLOBAL_TIPS_SHORT.md; fi; printf \"\\n\"; exec ${SHELL:-/bin/zsh}'",
        ],
        check=True,
    )
    subprocess.run(["tmux", "select-pane", "-L", "-t", session_name], check=True)


def launch_tmux(session_name: str, sandbox: Path, start_file: str) -> int:
    if shutil.which("tmux") is None:
        print("tmux is not installed or not in PATH.")
        return 1

    kill_tmux_session(session_name)

    try:
        create_tmux_stage_session(session_name, sandbox, start_file)
    except subprocess.CalledProcessError as exc:
        print(f"Failed to launch tmux session ({exc}).")
        return 1

    if os.environ.get("TMUX"):
        subprocess.run(["tmux", "switch-client", "-t", session_name], check=False)
    else:
        subprocess.run(["tmux", "attach", "-t", session_name], check=False)
    return 0


def run_check(check: dict[str, Any], workspace: Path) -> tuple[bool, str]:
    ctype = str(check.get("type", "")).strip()
    relative = str(check.get("path", "")).strip()
    target = workspace / relative if relative else workspace

    if ctype == "file_contains":
        value = str(check.get("value", ""))
        if not target.exists():
            return False, f"Missing file: {relative}"
        content = target.read_text(encoding="utf-8")
        if value in content:
            return True, f"{relative} contains expected text"
        return False, f"{relative} is missing expected text: {value!r}"

    if ctype == "file_not_contains":
        value = str(check.get("value", ""))
        if not target.exists():
            return False, f"Missing file: {relative}"
        content = target.read_text(encoding="utf-8")
        if value in content:
            return False, f"{relative} still contains forbidden text: {value!r}"
        return True, f"{relative} removed forbidden text"

    if ctype == "file_equals":
        expected = str(check.get("value", ""))
        if not target.exists():
            return False, f"Missing file: {relative}"
        actual = target.read_text(encoding="utf-8")
        if actual == expected:
            return True, f"{relative} matches expected content"
        return False, f"{relative} content does not match expected output"

    if ctype == "command_exit_zero":
        command = str(check.get("command", "")).strip()
        if not command:
            return False, "command_exit_zero missing command"
        command_cwd = workspace / relative if relative else workspace
        proc = subprocess.run(command, cwd=command_cwd, shell=True, text=True, capture_output=True)
        if proc.returncode == 0:
            return True, f"Command passed: {command}"
        output = (proc.stdout + "\n" + proc.stderr).strip()
        preview = "\n".join(output.splitlines()[:8])
        return False, f"Command failed ({command}):\n{preview}"

    return False, f"Unknown check type: {ctype}"


def get_active_mission(missions: list[Mission]) -> tuple[Mission | None, dict[str, Any], Path | None]:
    state = load_state()
    mission_id = str(state.get("active_mission", "")).strip()
    if not mission_id:
        return None, state, None
    mission = find_mission(missions, mission_id)
    if mission is None:
        return None, state, None
    workspace = Path(state.get("workspace", str(sandbox_path(mission.id) / "workspace")))
    return mission, state, workspace


def cmd_check(missions: list[Mission]) -> int:
    mission, _, workspace = get_active_mission(missions)
    if mission is None or workspace is None:
        print("No active mission.")
        return 1
    if not workspace.exists():
        print("Active workspace is missing. Start mission again.")
        return 1

    print(f"Checking {mission.id} in {workspace}")
    all_passed = True
    for check in mission.checks:
        passed, message = run_check(check, workspace)
        marker = "PASS" if passed else "FAIL"
        print(f"[{marker}] {message}")
        all_passed = all_passed and passed

    if not all_passed:
        print("Mission not complete yet.")
        return 1

    progress = load_progress()
    completed = progress.get("completed", [])
    if mission.id not in completed:
        completed.append(mission.id)
    progress["completed"] = completed
    save_progress(progress)
    print(f"Mission complete: {mission.id}")
    return 0


def cmd_reset(missions: list[Mission]) -> int:
    mission, _, workspace = get_active_mission(missions)
    if mission is None or workspace is None:
        print("No active mission.")
        return 1
    if not workspace.exists():
        print("Active workspace is missing. Start mission again.")
        return 1

    source_workspace = mission.path / "workspace"
    if not source_workspace.exists():
        print("Mission source workspace is missing.")
        return 1

    shutil.rmtree(workspace)
    shutil.copytree(source_workspace, workspace)
    write_workspace_stage_script(workspace)
    print(f"Workspace reset: {mission.id}")
    return 0


def cmd_start(missions: list[Mission], mission_id: str, session_base: str) -> int:
    mission = find_mission(missions, mission_id)
    if mission is None:
        print(f"Unknown mission: {mission_id}")
        return 1

    workspace = setup_workspace(mission)
    session_name = f"{session_base}-{mission.id.lower()}"
    origin_session = current_tmux_session()

    previous_state = load_state()
    if not origin_session:
        saved_origin = str(previous_state.get("origin_session", "")).strip()
        if saved_origin:
            origin_session = saved_origin

    save_state(
        {
            "active_mission": mission.id,
            "workspace": str(workspace),
            "session_name": session_name,
            "origin_session": origin_session,
        }
    )

    print(f"Started {mission.id} - {mission.title}")
    return launch_tmux(session_name, workspace.parent, mission.start_file)


def cmd_next(missions: list[Mission], session_base: str) -> int:
    active, state, _ = get_active_mission(missions)
    previous_session = str(state.get("session_name", "")).strip()
    previous_sandbox = sandbox_path(active.id) if active is not None else None
    origin_session = str(state.get("origin_session", "")).strip()

    if active is not None:
        check_result = cmd_check(missions)
        if check_result != 0:
            print("Stay on current stage until check passes.")
            return 1

    target: Mission | None = None
    if active is not None:
        for index, mission in enumerate(missions):
            if mission.id != active.id:
                continue
            if index + 1 < len(missions):
                target = missions[index + 1]
            break
    else:
        progress = load_progress()
        done = set(progress.get("completed", []))
        for mission in missions:
            if mission.id not in done:
                target = mission
                break

    if target is None:
        print("No next mission available.")
        return 0

    result = cmd_start(missions, target.id, session_base)

    if result == 0:
        if origin_session:
            new_state = load_state()
            new_state["origin_session"] = origin_session
            save_state(new_state)
        if previous_session:
            kill_tmux_session(previous_session)
        if previous_sandbox and previous_sandbox.exists():
            remove_sandbox(previous_sandbox)

    return result


def cmd_quit(missions: list[Mission]) -> int:
    mission, state, workspace = get_active_mission(missions)
    if mission is None or workspace is None:
        print("No active mission.")
        return 1

    session_name = str(state.get("session_name", "")).strip()
    origin_session = str(state.get("origin_session", "")).strip()

    if origin_session and origin_session != session_name and tmux_session_exists(origin_session):
        subprocess.run(["tmux", "switch-client", "-t", origin_session], check=False)

    if session_name:
        kill_tmux_session(session_name)

    remove_sandbox(workspace.parent)
    save_state({})
    print("Exited stage and removed sandbox.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Minimal mission runner")
    sub = parser.add_subparsers(dest="command")

    start = sub.add_parser("start", help="Start mission by id")
    start.add_argument("mission_id", help="Mission id, ex: M00-01")
    start.add_argument("--session", default="dojo", help="tmux session base name")

    nxt = sub.add_parser("next", help="Check current mission then start next")
    nxt.add_argument("--session", default="dojo", help="tmux session base name")

    sub.add_parser("check", help="Check active mission")
    sub.add_parser("reset", help="Reset active mission workspace files")
    sub.add_parser("quit", help="Exit stage and remove sandbox")
    return parser


def main(argv: list[str]) -> int:
    ensure_state_dirs()
    missions = load_missions()
    if not missions:
        print("No missions found.")
        return 1

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "start":
        return cmd_start(missions, args.mission_id, args.session)
    if args.command == "next":
        return cmd_next(missions, args.session)
    if args.command == "check":
        return cmd_check(missions)
    if args.command == "reset":
        return cmd_reset(missions)
    if args.command == "quit":
        return cmd_quit(missions)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
