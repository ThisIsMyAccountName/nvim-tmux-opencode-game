# nvim-game

An interactive terminal dojo for learning Neovim and tmux through small staged missions.

## Requirements

- Python 3.9+
- Neovim (`nvim`)
- tmux

## Quick start

From the project root:

```bash
python3 game.py next
```

Or start a specific mission:

```bash
python3 game.py start M00-01
```

`start` and `next` launch a tmux stage session with:

- left pane: Neovim in mission workspace
- right pane: mission objective + mission tips + compact global quick tips

When mission checks pass, move forward with:

```bash
./stage next
```

When done with the stage session entirely:

```bash
./stage quit
```

## Commands

From repo root:

- `python3 game.py start <MISSION_ID>` - start mission and launch tmux stage session
- `python3 game.py next` - run check on active mission, then start next mission on pass
- `python3 game.py check` - validate active mission
- `python3 game.py reset` - reset active mission workspace files to mission defaults
- `python3 game.py quit` - quit active stage, return to origin tmux session, remove sandbox

From inside a stage sandbox (or from `workspace/`):

- `./stage check`
- `./stage reset`
- `./stage next`
- `./stage quit`

## Stage behavior

- `./stage next` runs checks first; if checks fail, you stay on the current stage.
- `./stage reset` restores active `workspace/` files to original mission state.
- On successful `next`, the previous stage tmux session is killed and its sandbox is deleted.
- `./stage quit` switches back to the tmux session where the game was started (when available), then closes the stage session and deletes the stage sandbox.

## Sandbox layout

Each stage is created under `.dojo/sandboxes/<MISSION_ID>/` and contains:

- `workspace/` - editable mission files
- `mission.json` - mission metadata copied from source
- `GLOBAL_TIPS.md` - full shared command glossary (open on demand)
- `GLOBAL_TIPS_SHORT.md` - compact shared quick-reference shown in right pane
- `TIPS.md` - mission-specific command tips
- `COMMANDS.md` - minimal command reference for the stage
- `stage` - helper script for `check`, `next`, and `quit`
