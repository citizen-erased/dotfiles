#!/bin/python

import os
import sys
import inspect
import argparse
from subprocess import call

#----------------------------------------------------------------------------#
# globals
#----------------------------------------------------------------------------#

dry_run = True

pwd = os.getcwd()
home = os.path.expanduser('~')


#----------------------------------------------------------------------------#
# setup functions
#----------------------------------------------------------------------------#

def setup_sudo():
    pass


def setup_slim():
    pass

def setup_x():
    pass


def setup_yaourt():
    pass


def setup_rtorrent():
    pass


def setup_web():
    pacman('chromium', 'flashplugin')


def setup_git():
    pacman('git')
    symlink('.gitconfig', 'gitignore')


def setup_zsh():
    """
    Installs zsh and oh-my-zsh.
    """
    pacman('zsh')
    command('curl -L https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh | sh')
    symlink('.zshrc')


def setup_vim():
    bundle_dir = os.path.join(home, '.vim', 'bundle')
    symlink('.vimrc', '.vim')
    gitClone('https://github.com/nvie/vim-flake8.git', bundle_dir)
    gitClone('https://github.com/scrooloose/nerdtree.git', bundle_dir)
    gitClone('https://github.com/scrooloose/syntastic.git', bundle_dir)


def setup_i3():
    pacman('i3', 'dmenu', 'conky')
    symlink('.i3')


def setup_mpd():
    symlink('.mpdconf', '.ncmpcpp/config', '.config/systemd/user/mpd.service')

    base_dir = os.path.join(home, '.mpd')
    touch(['database', 'log', 'pid', 'state'], base_dir)

    print('ensure the following line is in .xinitrc before exec <session>:')
    print('systemd --user &')


def setup_misc():
    pacman('feh', 'htop', 'ranger', 'openssh', 'rsync')
    symlink('.fehbg')


#----------------------------------------------------------------------------#
# setup utility functions
#----------------------------------------------------------------------------#

def ensureDir(directory):
    if not os.path.exists(directory):
        print('creating directory: %s' % dir)
        if not dry_run:
            os.makedirs(directory)


def symlink(*args):
    """
    Symlinks a dotfile.

    args:
        Each arg is either a src string or a (src, dst) tuple.

    src should be relative to the current dotfiles directory.
    dst should be relative to the current home directory.
    """
    for arg in args:
        if isinstance(arg, tuple):
            src, dst = arg
        else:
            src, dst = arg, arg

        src = os.path.join(pwd, src)
        dst = os.path.join(home, dst)

        ensureDir(os.path.dirname(dst))
        command('ln -s %s %s' % (src, dst))

def touch(files, base_dir=None):
    """
    files: a list of files.
    base_dir: specifies which directory files is relative to.
    """
    ensureDir(base_dir)

    for filename in files:
        if base_dir:
            filename = os.path.join(base_dir, filename)
        command('touch %s' % filename)


def pacman(*progs):
    pac_args = ' '.join(progs)
    command('sudo pacman -Sy %s' % pac_args)


def gitClone(url, dst=''):
    command('git clone %s %s' % (url, dst))

def command(cmd):
    print(cmd)

    if not dry_run:
        return_code = call(cmd, shell=True)


#----------------------------------------------------------------------------#
# main functions
#----------------------------------------------------------------------------#

def getFunctions():
    all_funcs = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
    functions = []

    for name, func in all_funcs:
        if name.startswith('setup_'):
            functions.append({
                'function_name' : name,
                'command_name'  : name.replace('setup_', '', 1),
                'function'      : func,
            })

    return sorted(functions, key=lambda x: x['command_name'])


def parseArgs():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--dry-run', '-d', action='store_true',
        help='If specified no changes will be made.')

    setup_cmds = [info['command_name'] for info in getFunctions()]
    subparsers = parser.add_subparsers(help='', dest='setup_type')

    # "all" subparser
    subparser = subparsers.add_parser('all', help='setup all software.')

    # "all-except" subparser
    subparser = subparsers.add_parser('all-except', help='setup everything except the software specified.')
    for info in getFunctions():
        subparser.add_argument('--' + info['command_name'],
            action='store_true', help=info['function'].__doc__)

    # "only" subparser
    subparser = subparsers.add_parser('only', help='setup only the software specified.')
    for info in getFunctions():
        subparser.add_argument('--' + info['command_name'],
            action='store_true', help=info['function'].__doc__)

    return parser.parse_args()


if __name__ == '__main__':
    args = parseArgs()
    infos = getFunctions()

    if args.setup_type == 'all-except':
        infos = [f for f in infos if not getattr(args, f['command_name'])]
    elif args.setup_type == 'only':
        infos = [f for f in infos if getattr(args, f['command_name'])]

    for func_info in infos:
        print()
        print('-------- setup %s --------' % func_info['command_name'])
        func_info['function']()

