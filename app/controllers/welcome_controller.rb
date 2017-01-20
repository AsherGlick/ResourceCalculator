class WelcomeController < ApplicationController
  def index
    @item_list = Recipes.item_list
  end
end
