cd ~

wget http://pyyaml.org/download/libyaml/yaml-0.1.5.tar.gz
tar xzf yaml-0.1.5.tar.gz
rm yaml-0.1.5.tar.gz
cd yaml-0.1.5
./configure --prefix $HOME/ruby
make
make install

cd ~

wget http://cache.ruby-lang.org/pub/ruby/1.9/ruby-1.9.3-p484.tar.gz
tar xzf ruby-1.9.3-p484.tar.gz
rm ruby-1.9.3-p484.tar.gz
cd ruby-1.9.3-p484
./configure --prefix $HOME/ruby
make install

cd ~

wget https://nodejs.org/dist/latest/node-v6.6.0-linux-x64.tar.gz
tar xzf node-v6.6.0-linux-x64.tar.gz
rm node-v6.6.0-linux-x64.tar.gz


# Configure .zlogin to set the right environment variables
echo 'export GEM_HOME="$HOME/.gems"' >> $HOME/.zlogin
echo 'export GEM_PATH="$GEM_HOME"' >> $HOME/.zlogin
echo 'export PATH=$HOME/ruby/bin:$GEM_PATH/bin:$HOME/node-v6.6.0-linux-x64/bin:$PATH' >> $HOME/.zlogin
echo 'unset -f gem' >> $HOME/.zlogin
