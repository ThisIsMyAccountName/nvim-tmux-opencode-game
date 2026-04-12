# nvim-game

An interactive terminal dojo for learning Neovim, tmux, and an agent-driven workflow.

This repository currently includes the guided campaign MVP (Chapter 0 and Chapter 1).

## Requirements

- Python 3.9+
- Neovim (`nvim`) installed
- tmux installed

## Quick start

From the project root:

```bash
python3 game.py next
python3 game.py status
```

`next` and `start` now launch a mission tmux sandbox by default.
Starting a new stage removes the previously active stage sandbox automatically.

If you only want to prepare files without opening tmux:

```bash
python3 game.py next --no-launch
```

When you think the mission is complete:

```bash
python3 game.py check
python3 game.py hint
python3 game.py next
```

## Commands

- `python3 game.py list` - show all missions and progress
- `python3 game.py start <MISSION_ID>` - start mission and launch sandbox tmux
- `python3 game.py next` - check current mission, then move to next and launch tmux
- `python3 game.py status` - show active mission details
- `python3 game.py hint [level]` - show all hints, or one hint level
- `python3 game.py check` - validate active mission
- `python3 game.py reset` - reload current stage workspace from mission source
- `python3 game.py exit` - exit active mission tmux session
- `python3 game.py launch` - open a tmux session with mission workspace

## Sandbox layout per stage

Every stage creates a fresh sandbox under `.dojo/sandboxes/<MISSION_ID>/` with:

- `workspace/` - editable mission files
- `mission.json` - copied stage metadata
- `COMMANDS.md` - stage-specific command list and objectives
- `COMMANDS.md` includes a best-fit command path, fallback path, and stage-specific Neovim/tmux references
- `stage` - helper script so you can run `./stage check`, `./stage hint`, etc.

Inside a sandbox you can exit the stage session with `./stage exit`.
When available, it switches back to your original tmux session, then deletes the stage session.

From inside a stage:

- Run `./stage` to see all available stage commands.
- If your prompt is in `workspace/`, you can run `./stage ...` there too.
- Run `./stage next` to check current stage and move to the next one on pass.

Hints are now progressive and explicit: `./stage hint` prints all hint levels for the active mission.

## Campaign scope (current)

- Chapter 0: warmup mission flow
- Chapter 1: Neovim core navigation and editing

Upcoming chapters:

- Chapter 2: deeper Neovim editing power
- Chapter 3: tmux fundamentals
- Chapter 4: cross-tool relay drills
- Chapter 5: opencode workflow missions
# nvim-tmux-opencode-game
