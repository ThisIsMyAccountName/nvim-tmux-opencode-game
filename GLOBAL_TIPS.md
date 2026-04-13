========================================
Core Navigation
- `h,j,k,l` - move left, down, up, right.
- `i` - enter Insert mode to type in the file.
- `Esc` - return to Normal mode for movement and commands.
- `w` / `b` - jump to next / previous word.
- `gg` / `G` - jump to top / bottom of file.
- `:w` - save current file.
- `:` - open command-line mode.
- `/ <target_text>` - search forward for target text.
- `n` / `N` - jump to next / previous search result.
- `<Space>` - LazyVim leader key (starts shortcut combos).

Editing Basics
- `r` - replace one character under cursor.
- `ciw` - replace current word.
- `cw` - replace from cursor to end of current word.
- `dd` - cut/delete current line.
- `p` / `P` - paste after / before cursor.
- `u` / `Ctrl-r` - undo / redo.

Multi-Window Basics
- `:e <path_to_file>` - open a file in current window.
- `:vsplit <path_to_file>` - open a file in vertical split.
- `<C-w>w` - switch between split windows.
- `<C-w>h` / `<C-w>l` - move to left / right split.
- `:only` - keep current window, close others.

Stage commands
- `./stage check` - run mission checks.
- `./stage reset` - reset mission workspace files.
- `./stage next` - move to next mission if checks pass.
- `./stage quit` - exit stage session.

========================================
