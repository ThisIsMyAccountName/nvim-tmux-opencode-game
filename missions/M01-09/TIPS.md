# M01-09 Tips

Objective: update two far-apart lines (top and bottom) quickly.

## Core Navigation
- `h,j,k,l` - move left, down, up, right.
- `i` - enter Insert mode to type in the file.
- `Esc` - return to Normal mode for movement and commands.
- `gg` / `G` - jump to top / bottom of file.
- `:w` - save current file.
- `:` - open command-line mode.
- `/text` - search forward for text.
- `n` / `N` - jump to next / previous search result.
- `<Space>` - LazyVim leader key (starts shortcut combos).

## Commands For This Task
- `ma` - place mark `a` at current location.
- `` `a `` - jump back to exact spot of mark `a`.
- `'a` - jump to line of mark `a`.
- `<C-o>` / `<C-i>` - go back / forward in jump history.
- `/ <target_text>` - jump to owner/value lines by search.
- `ciw` - replace current word.

## If You Get Stuck
- `u` / `Ctrl-r` - undo / redo.
- `:e!` - reload file and discard unsaved edits.
- `:q` / `:tabclose` - close current split / tab.
- `./stage reset` - reset mission workspace files.
