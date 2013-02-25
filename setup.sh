#!/bin/sh

ln -s ~/dotfiles/.xinitrc ~/.xinitrc

ln -s ~/dotfiles/gitconfig ~/gitconfig
ln -s ~/dotfiles/gitignore ~/gitignore

ln -s ~/dotfiles/.i3 ~/.i3

ln -s ~/dotfiles/.vim ~/.vim
ln -s ~/dotfiles/.vimrc ~/.vimrc

ln -s ~/dotfiles/.zshrc ~/.zshrc

ln -s ~/dotfiles/.fehbg ~/.fehbg

mkdir -p ~/.mpd/playlists
touch ~/.mpd/{database,log,pid,state}
ln -s ~/dotfiles/.mpdconf ~/.mpdconf
mkdir -p ~/.config/systemd/user
ln -s ~/dotfiles/.config/systemd/user/mpd.service ~/.config/systemd/user/mpd.service 
echo "make sure the following line is in .xinitrc before exec <session>:"
echo "systemd --user &"
