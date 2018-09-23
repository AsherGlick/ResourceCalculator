class CalculatorController < ApplicationController
  def index

	def class_from_string(str)
	  str.split('::').inject(Object) do |mod, class_name|
	    mod.const_get(class_name)
	  end
	end

	class_name = params[:gamename].slice(0,1).capitalize + params[:gamename].slice(1..-1)
  	@game_name = params[:gamename]
    @item_list = class_from_string(class_name).item_list
    @styles = class_from_string(class_name).styles
  end
end
