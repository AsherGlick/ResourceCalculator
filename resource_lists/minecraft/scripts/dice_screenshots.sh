#!/bin/bash

# mkdir -p screenshots
mkdir -p image_text
mkdir -p diced_images
mkdir -p named_images
# # Take a screenshot
# import -window root ./screenshots/0.png


inventory_corner_x=782
inventory_corner_y=459

text_screenshot_corner_x=$( expr $inventory_corner_x + 40 )
text_screenshot_corner_y=$( expr $inventory_corner_y - 8 )
text_screenshot_height=16


mouse_hover_corner_x=$( expr $inventory_corner_x + 16 )
mouse_hover_corner_y=$( expr $inventory_corner_y + 16 )

index=0

for number in {0..29}; do
# for number in {0..0}; do
	# Take a screenshot
	# import -window root -crop 1080x1920+0+0 ./screenshots/$number.png
	

	for y in {0..4}; do
		for x in {0..8}; do
			icon_xpos=$( expr $( expr $x \* 36 ) + $inventory_corner_x );
			icon_ypos=$( expr $( expr $y \* 36 ) + $inventory_corner_y );

			xpos=$( expr $( expr $x \* 36 ) + $text_screenshot_corner_x );
			ypos=$( expr $( expr $y \* 36 ) + $text_screenshot_corner_y );
			
			xcursorpos=$( expr $( expr $x \* 36 ) + $mouse_hover_corner_x );
			ycursorpos=$( expr $( expr $y \* 36 ) + $mouse_hover_corner_y );

			width=$( expr 1920 - $xpos )

			xdotool mousemove 1125 547

			sleep .5

			import -window root -crop "32x32+"$icon_xpos"+"$icon_ypos "diced_images/"$index".png"

			xdotool mousemove $xcursorpos $ycursorpos

			sleep .5

			import -window root -crop $width"x"$text_screenshot_height"+"$xpos"+"$ypos "image_text/"$index".png"

			convert  "image_text/"$index".png" -grayscale Rec709Luma -brightness-contrast 50x100% "image_text/"$index".png"
			# convert $file -crop "32x32+"$xpos"+"$ypos "diced_images/"$index".png"
			index=$( expr $index + 1 )
			# exit
		done
	done


	# Scroll to the next page
	xdotool click --repeat 5 --delay 200 5
done


# import -window root -crop 100x100+500+500 $HOME/Desktop/testfile.png


# ################################################################################
# # Slice up the screenshots into individual items. You may need to adjust the
# # top left corner if you are using a machine with a different task bar. This
# # was calibrated for Ubuntu 20.10. In order to find out what the offset should
# # be just take a screenshot and open it up in your favorite image editor. I
# # used Gimp for this. There should be a ruler that allows you to determine the
# # location of your curser, or a selection of the image. Gimp's is on the select
# # tool, it will give you a position as well as a width and height. Just change
# # the position here to match the position your image editor is giving you.
# # Everything else should stay the same. When running this took a few seconds
# # per screenshot to generate all of the diced images from that screenshot
# #
# # For 1.17 which had 30 pages (0-29) it took 3:03
# ################################################################################
# mkdir -p diced_images

# # Image Size = 32
# # Offset Size = 36
# # Top Left Corner= 782,459
# index=0
# for file in ./screenshots/*; do
# 	echo $file
# 	for y in {0..4}; do
# 		for x in {0..8}; do
# 			xpos=$( expr $( expr $x \* 36 ) + 782 );
# 			ypos=$( expr $( expr $y \* 36 ) + 459 );

# 			convert $file -crop "32x32+"$xpos"+"$ypos "diced_images/"$index".png"
# 			index=$( expr $index + 1 )
# 		done
# 	done
# done


# This does not work
# ################################################################################
# # Brute force match the old images to the new images. This is not perfect as
# # slight color shifts will cause a delta, but it will allow for *some* of the
# # captured images to be removed from the list, hopefully leaving with a more
# # reasonable set of images to tag with item names.
# # This will take a long time to run.
# ################################################################################
# mkdir -p duplicate_images

# tcompare() {
# 	value=$( compare -metric PAE "$1" "$2" /dev/null 2>&1 | cut -d'(' -f1-1 )

# 	# echo $value

# 	num1=10000
# 	if (( $(echo "$num1 > $value" |bc -l) )); then
# 		echo "  Found Match" $1 $2 $value
# 		mv $2 duplicate_images/
# 	fi
# }

# N=16
# (
# for existing_file in ../items/*; do
# # for existing_file in test_old_images/*; do
# 	echo "Testing" $existing_file
# 	for new_file in diced_images/*; do
# 		((i=i%N)); ((i++==0)) && wait
# 		tcompare "$existing_file" "$new_file" &
# 	done
# 	wait
# done
# )