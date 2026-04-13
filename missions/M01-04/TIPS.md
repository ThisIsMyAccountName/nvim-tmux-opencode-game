# M01-04 Tips

## Core Navigation
- `h,j,k,l` - move left, down, up, right.
- `i` - enter Insert mode to type in the file.
- `Esc` - return to Normal mode for movement and commands.
- `:w` - save current file.
- `:` - open command-line mode.
- `/text` - search forward for text.
- `n` / `N` - jump to next / previous search result.
- `<Space>` - LazyVim leader key (starts shortcut combos).

## Commands For This Task
- `:%s/<lookup>/<replace>/g` - replace lookup with replace in whole file; `%` means whole file, `g` means all matches per line.
- `dd` - delete current line.
- `/ <target_text>` - jump to each match for target text.
- `ciw` - replace current word.

## If You Get Stuck
- `u` / `Ctrl-r` - undo / redo.
- `:e!` - reload file and discard unsaved edits.
- `:q` / `:tabclose` - close current split / tab.
- `./stage reset` - reset mission workspace files.
