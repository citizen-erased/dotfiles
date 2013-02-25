ln -s ~/dotfiles/gitconfig ~/gitconfig
ln -s ~/dotfiles/gitignore ~/gitignore

ln -s ~/dotfiles/.i3 ~/.i3

ln -s ~/dotfiles/.vim ~/.vim
ln -s ~/dotfiles/.vimrc ~/.vimrc

ln -s ~/dotfiles/.zshrc ~/.zshrc

mkdir -p ~/.mpd/playlists
touch ~/.mpd/{database,log,pid,state}
ln -s ~/dotfiles/.mpdconf ~/.mpdconf
