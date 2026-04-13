# M01-06 Tips

## Core Navigation
- `h,j,k,l` - move left, down, up, right.
- `i` - enter Insert mode to type in the file.
- `Esc` - return to Normal mode for movement and commands.
- `w` / `b` - jump to next / previous word.
- `:w` - save current file.
- `:` - open command-line mode.
- `<Space>` - LazyVim leader key (starts shortcut combos).

## Commands For This Task
- `:e <path_to_file>` - open a file in current window.
- `yiw` - copy current word into yank register.
- `ciw` then `Ctrl-r "` - replace current word by pasting the copied word.
- `p` / `P` - paste copied text after / before cursor.
- `ciw` - replace current word with the value you want.
- `/ <target_text>` - jump directly to key lines.
- `:vsplit <path_to_file>` - optional side-by-side compare view.
- `<C-w>w` - switch between split windows.

## If You Get Stuck
- `u` / `Ctrl-r` - undo / redo.
- `:e!` - reload file and discard unsaved edits.
- `:q` - close current split.
- `:only` - close other windows, keep current one.
- `./stage reset` - reset mission workspace files.
