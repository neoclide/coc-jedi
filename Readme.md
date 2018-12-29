# coc-jedi

Jedi integration for [coc.nvim](https://github.com/neoclide/coc.nvim).

This plugin start a python server which attached to neovim/vim, and make the
nodejs part communicate with python server by use notification, it would never
block your vim.

**Note:** only basic completion working, **don't use it seriously.**

## Install

Use plugin manager, like [vim-plug](https://github.com/junegunn/vim-plug) by add:

    Plug 'neoclide/coc.nvim', {'do': { -> coc#util#install()}}
    Plug 'neoclide/coc-jedi', {'do': 'yarn install'}

to your `init.vim` and run:

    :PlugInstall

Restart your vim.

**Note:** no need to use lazyload for this plugin.

**Note:** this plugin contains vim part, it can't be installed by `:CocInstall`
command.

## Features

- [x] Completion
- [ ] Signature help, support current active param.
- [ ] Hover for documentation, show full path & doc string.
- [ ] Goto definition.
- [ ] Goto references.
- [ ] Document symbols.

## Configuration

TODO

## F.A.Q

TODO

## License

MIT
