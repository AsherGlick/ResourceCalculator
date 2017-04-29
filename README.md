ResourceCaluclator.com is a website that can be used to calculate required resources from a list of final requirements, and tell you how to get from the raw resources to the final resources.



Publishing
==========
In order to release a new version of the website to production just push to the master branch.
More information can be found in .gitlab-ci.yml


Compiling Spritesheets
======================
sprite sheets are compiled with the sprite factory gem
in order to run the sprite factory gem use the command `sf items --layout packed --selector div.item_` while in the `public` folder

This will generate a new `images.css` and `images.png` as of the time of writing these are the standards we use (instead of having something in scss or another image path)
Image compression is also useful but there is no project standard for this yet so we have been using https://tinypng.com/ to do it for us


```
sudo apt-get install imagemagick libmagickwand-dev
sudo gem install rmagick
gem install sprite-factory
```
