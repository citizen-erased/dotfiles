set nocompatible
syntax on

set autoindent
set smartindent

set tabstop=4
set shiftwidth=4
set expandtab

set showmatch

set ruler
set number

set incsearch
set hls

set hidden
set scrolloff=5
set showcmd

set backup
set backupdir=~/.vim/backup
set directory=~/.vim/tmp

execute pathogen#infect()

filetype plugin on

set t_Co=256
colorscheme xoria256
