#!/bin/bash

################################################################################
# This script generates images for all of the items in minecraft, as well as
# provides screenshots of their names so that another process (mc_ocr.py) can
# name all of the images according to their in-game name.
#
# This code was originally calibrated for minecraft running at GUI Scale 2 which
# gives 32 pixel square icons. It was run on Ubuntu 20.04 on an external monitor
# where there was no system bar. If running on a different setup then two
# variables may need to be adjusted to match the new location.
# $inventory_corner_x and $inventory_corner_y determine the top left corner of
# the inventory.
#
# In order to run this script have minecraft open and maximized on the leftmost
# monitor, the GUI scale set to 2, and the minecraft creative inventory open
# and scrolled to the top of the search tab (which contains all items). Then
# this program should take care of the rest. For Minecraft 1.17 it took about
# 32 minutes to full complete.
################################################################################

# Create the folders that will be filled by this program
mkdir -p image_text
mkdir -p diced_images

# This folder is not used in this file but is used in the mc_ocr.py
mkdir -p named_images

inventory_corner_x=782
inventory_corner_y=459

# Offset the screenshot location for hover text based on where the hover text appears 
text_screenshot_corner_x=$( expr $inventory_corner_x + 40 )
text_screenshot_corner_y=$( expr $inventory_corner_y - 8 )
text_screenshot_height=16

# Offset where the mouse should move to by half of the image size
mouse_hover_corner_x=$( expr $inventory_corner_x + 16 )
mouse_hover_corner_y=$( expr $inventory_corner_y + 16 )

# Start the image name numbering at 0
index=0

# Iterate through all of the pages of the minecraft creative inventory
# at the time of writing there were exactly 30 pages (Minecraft 1.17)
for number in {0..29}; do
	# Loop through all the rows of each page of the minecraft creative inventory
	for y in {0..4}; do
		# Loop through all the columns of each page of the minecraft creative inventory
		for x in {0..8}; do
			# Define the top left corner of the item's icon
			icon_xpos=$( expr $( expr $x \* 36 ) + $inventory_corner_x );
			icon_ypos=$( expr $( expr $y \* 36 ) + $inventory_corner_y );

			# Define the top left corner of the text-screenshot's position
			xpos=$( expr $( expr $x \* 36 ) + $text_screenshot_corner_x );
			ypos=$( expr $( expr $y \* 36 ) + $text_screenshot_corner_y );
			
			# Define the point in the middle of the item icon where the mouse should move
			xcursorpos=$( expr $( expr $x \* 36 ) + $mouse_hover_corner_x );
			ycursorpos=$( expr $( expr $y \* 36 ) + $mouse_hover_corner_y );

			# Define the width of the text-screenshot as the remaining horizontal width of a 1080p screen
			width=$( expr 1920 - $xpos )

			# Move the mouse to the scrollbar
			xdotool mousemove 1125 547

			# Delay before taking a screenshot so the game has plenty of time to catch up to the input
			sleep .5

			# Take a screenshot of the item icon and save it to the "diced_images" folder
			import -window root -crop "32x32+"$icon_xpos"+"$icon_ypos "diced_images/"$index".png"

			# Move the mouse over the item icon
			xdotool mousemove $xcursorpos $ycursorpos

			# Delay before taking a screenshot so the game has plenty of time to catch up to the input
			sleep .5

			# Take a screenshot of the hovertext for the item
			import -window root -crop $width"x"$text_screenshot_height"+"$xpos"+"$ypos "image_text/"$index".png"

			# Convert the text screenshot to grayscale and bump the contrast to maximum to get a black or white image
			convert  "image_text/"$index".png" -grayscale Rec709Luma -brightness-contrast 50x100% "image_text/"$index".png"

			# Increase the file index for the next run to save the next image with a different name
			index=$( expr $index + 1 )
		done
	done

	# Once the entire page has been processed, scroll to the next page
	xdotool click --repeat 5 --delay 200 5
done
