# M01-08 Tips

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
- `:vsplit <path_to_file>` - open another file in a split.
- `<C-w>w` - switch between split windows.
- `<C-w>h` / `<C-w>l` - move to left / right split.
- `/ <target_text>` - jump to lines containing target text.
- `viw` - visually select current word.
- `yiw` - copy current word.
- `ciw` then `Ctrl-r "` - replace current word by pasting copied text.
- `v` - start visual selection.
- `y` - copy selected text.
- `c` - change selected text.
- `p` - paste copied text over selected text.

## If You Get Stuck
- `u` / `Ctrl-r` - undo / redo.
- `:e!` - reload file and discard unsaved edits.
- `:q` - close current split.
- `:only` - close other windows, keep current one.
- `./stage reset` - reset mission workspace files.
