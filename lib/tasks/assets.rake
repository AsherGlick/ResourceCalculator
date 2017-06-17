require 'sprite_factory'

def make_sheet (name)
    SpriteFactory.run!("app/assets/images/items/#{name}", :output_style => "app/assets/stylesheets/#{name}.css.erb")
    system("pngquant --force --ext .png 256 --nofs app/assets/images/items/#{name}.png")
	system("convert -verbose -strip app/assets/images/items/#{name}.png app/assets/images/items/#{name}.png") # remove the sRGB data that pngquaint adds in versions < 2.6
	system("optipng -o7 app/assets/images/items/#{name}.png")
end

namespace :assets do
  desc 'recreate sprite images and css'
  task :resprite => :environment do 
    SpriteFactory.cssurl = "url(<%= asset_path 'items/$IMAGE'%>)"  # use a sass-rails helper method to be evaluated by the rails asset pipeline
    SpriteFactory.library = :chunkypng  # use simple chunkypng gem to handle .png sprite generation
    SpriteFactory.selector = "div.item_"  # change the css selector to use a div with a class prefixed by 'item_'
    SpriteFactory.layout = :packed  # pack the images into a rectangle instead of a line
    
    make_sheet("minecraft")
  end
end