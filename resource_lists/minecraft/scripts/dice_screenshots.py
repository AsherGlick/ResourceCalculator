################################################################################
# This script generates images for all of the items in minecraft, as well as
# provides screenshots of their names so that another process (mc_ocr.py) can
# name all of the images according to their in-game name.
################################################################################

import math
import subprocess
import time

# Some constants about minecraft's UI that are scaled via the ui_size attribute
NATIVE_TEXT_SIZE = 8
NATIVE_INVENTORY_WIDTH = 195
NATIVE_INVENTORY_HEIGHT = 188
NATIVE_INVENTORY_LEFT_PADDING = 9
NATIVE_INVENTORY_TOP_PADDING = 44
NATIVE_ICON_SIZE = 16
NATIVE_ITEM_PADDING = 2
NATIVE_TEXT_X_OFFSET = 12
NATIVE_TEXT_Y_OFFSET = -12
NATIVE_SCROLLBAR_X_OFFSET = 168
NATIVE_SCROLLBAR_Y_OFFSET = 2


################################################################################
# get_inventory_left_offset
#
# Calculates the left offset of the inventory using minecraft's centering
# algorithm and returns the x pixel coordinate of the left side of the menu.
# The algorithm is a little confusing due to ui scaling. The center point is
# calculate in minecraft's native ui pixel size, not the users's screen pixel
# size. The conversion of screen pixels to ui pixles is rounded up, while the
# centerpoint algorithm is rounded down.
################################################################################
def get_inventory_left_offset(window_width: int, ui_size: int) -> int:
	native_screen_width: int = math.ceil(window_width / ui_size)
	native_inventory_left_offset = math.floor((native_screen_width - NATIVE_INVENTORY_WIDTH)/2)
	return native_inventory_left_offset * ui_size
def get_inventory_right_offset(window_width: int, ui_size: int) -> int:
	return window_width - get_inventory_left_offset(window_width, ui_size) - NATIVE_INVENTORY_WIDTH * ui_size;

def get_inventory_top_offset(window_height: int, ui_size: int) -> int:
	native_screen_height: int = math.ceil(window_height / ui_size)
	native_inventory_top_offset = math.floor((native_screen_height - NATIVE_INVENTORY_HEIGHT)/2)
	return native_inventory_top_offset * ui_size
def get_inventory_bottom_offset(window_height: int, ui_size: int) -> int:
	return window_height - get_inventory_top_offset(window_height, ui_size) - NATIVE_INVENTORY_HEIGHT * ui_size;

def mouse_move(x: int, y: int) -> None:
	subprocess.run(["xdotool", "mousemove", str(x), str(y)])


def take_screenshot(x: int, y: int, width: int, height: int, path: str) -> None:
	subprocess.run(["import", "-window", "root", "-crop", "{width}x{height}+{x}+{y}".format(width=width, height=height, x=x, y=y), path])


################################################################################
# screenshot_page
#
# This takes a screenshot of each item on a page as well as the name of the
# item that appears when the mouse is hovered over the item.
################################################################################
def screenshot_page(
	starting_count: int,
	first_item_x_coordinate: int,
	first_item_y_coordinate: int,
	ui_size: int,
	window_width: int,
) -> int:
	icon_count = starting_count
	text_count = starting_count
	icon_size: int = NATIVE_ICON_SIZE * ui_size
	icon_padding: int = NATIVE_ITEM_PADDING * ui_size
	text_size: int = NATIVE_TEXT_SIZE * ui_size
	text_x_offset: int = NATIVE_TEXT_X_OFFSET * ui_size
	text_y_offset: int = NATIVE_TEXT_Y_OFFSET * ui_size

	native_mouse_offset = 2

	horizontal_inventory_count = 9
	vertical_inventory_count = 5

	for y in range(vertical_inventory_count):
		for x in range(horizontal_inventory_count):

			x_location = first_item_x_coordinate + (x * (icon_padding + icon_size))
			y_location = first_item_y_coordinate + (y * (icon_padding + icon_size))

			take_screenshot(x_location, y_location, icon_size, icon_size, "diced_images/{}.png".format(icon_count))
			icon_count += 1

	for y in range(vertical_inventory_count):
		for x in range(horizontal_inventory_count):
			mouse_x_location = first_item_x_coordinate + (x * (icon_padding + icon_size)) + (ui_size * native_mouse_offset)
			mouse_y_location = first_item_y_coordinate + (y * (icon_padding + icon_size)) + (ui_size * native_mouse_offset)

			mouse_move(mouse_x_location, mouse_y_location)
			time.sleep(0.1)

			text_x_location = mouse_x_location + text_x_offset
			text_y_location = mouse_y_location + text_y_offset
			text_width = window_width - text_x_location

			image_path = "image_text/{}.png".format(text_count)

			take_screenshot(text_x_location, text_y_location, text_width, text_size, image_path)

			subprocess.run(["convert", image_path, "-grayscale", "Rec709Luma", "-brightness-contrast", "50x100%", image_path])

			text_count += 1


	return icon_count


def scroll_down(first_item_x_coordinate: int, first_item_y_coordinate: int, ui_size: int) -> None:

	scrollbar_x = first_item_x_coordinate + NATIVE_SCROLLBAR_X_OFFSET * ui_size
	scrollbar_y = first_item_y_coordinate + NATIVE_SCROLLBAR_Y_OFFSET * ui_size

	mouse_move(scrollbar_x, scrollbar_y)
	time.sleep(0.1)
	subprocess.run(["xdotool", "click", "--repeat", "5", "--delay", "200", "5"])


def main(
	ui_size: int,
	screen_width: int,
	screen_height: int,
	screen_offset_top: int,
	page_count:int,
) -> None:
	inventory_left_padding: int = NATIVE_INVENTORY_LEFT_PADDING * ui_size
	inventory_top_padding: int = NATIVE_INVENTORY_TOP_PADDING * ui_size

	first_item_x_coordinate = get_inventory_left_offset(screen_width, ui_size) + inventory_left_padding
	first_item_y_coordinate = get_inventory_top_offset(screen_height - screen_offset_top, ui_size) + inventory_top_padding + screen_offset_top

	count = 0

	for _ in range(page_count):
		count = screenshot_page(count, first_item_x_coordinate, first_item_y_coordinate, ui_size, screen_width)
		scroll_down(first_item_x_coordinate, first_item_y_coordinate, ui_size)

	count = screenshot_page(count, first_item_x_coordinate, first_item_y_coordinate, ui_size, screen_width)


main(
	ui_size = 2,
	screen_width = 1920,
	screen_height = 1080,
	screen_offset_top = 37, # how many pixels the title bar takes up (not fullscreen)
	page_count = 31,
)
