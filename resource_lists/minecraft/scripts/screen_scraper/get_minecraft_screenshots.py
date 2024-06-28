################################################################################
# This script generates images for all of the items in minecraft, as well as
# provides screenshots of their names so that another process (mc_ocr.py) can
# name all of the images according to their in-game name.
################################################################################

import math
import subprocess
import time
from PIL import Image
import pyautogui

# Some constants about minecraft's UI that are scaled via the ui_size attribute
NATIVE_TEXT_SIZE = 8 + 3 # 3 extra for the border bar
NATIVE_ICON_SIZE = 16
NATIVE_ITEM_PADDING = 2
NATIVE_TEXT_X_OFFSET = 12
NATIVE_TEXT_Y_OFFSET = -12 - 3 # 3 extra for the border bar
NATIVE_SCROLLBAR_X_OFFSET = 168
NATIVE_SCROLLBAR_Y_OFFSET = 2
FIRST_ITEM_X_OFFSET_FROM_ANCHOR = 6
FIRST_ITEM_Y_OFFSET_FROM_ANCHOR = 73


def mouse_move(x: int, y: int) -> None:
    subprocess.run(["xdotool", "mousemove", str(x), str(y)])
    # pyautogui.moveTo(x, y)


def take_screenshot(x: int, y: int, width: int, height: int, path: str) -> Image.Image:
    subprocess.run(["import", "-window", "root", "-crop", "{width}x{height}+{x}+{y}".format(width=width, height=height, x=x, y=y), path])
    return Image.open(path)

    # Alternate form using pyautogui
    # item_page_screenshot = pyautogui.screenshot(region=(
    #     x,
    #     y,
    #     x + width),
    #     y + height)
    # ))

################################################################################
# screenshot_page
#
# This takes a screenshot of each item on a page as well as the name of the
# item that appears when the mouse is hovered over the item.
################################################################################
def screenshot_page(
    page: int,
    first_item_x_coordinate: int,
    first_item_y_coordinate: int,
    ui_size: int,
    window_width: int,
):
    icon_size: int = NATIVE_ICON_SIZE * ui_size
    icon_padding: int = NATIVE_ITEM_PADDING * ui_size
    text_size: int = NATIVE_TEXT_SIZE * ui_size
    text_x_offset: int = NATIVE_TEXT_X_OFFSET * ui_size
    text_y_offset: int = NATIVE_TEXT_Y_OFFSET * ui_size

    native_mouse_offset = 2

    horizontal_inventory_count = 9
    vertical_inventory_count = 5

    # Screenshot each item
    item_page_screenshot = take_screenshot(
        first_item_x_coordinate,
        first_item_y_coordinate,
        horizontal_inventory_count * (icon_padding + icon_size),
        vertical_inventory_count * (icon_padding + icon_size),
        "raw_images/{page}-icon-page.png".format(page=page)
    )
    for y in range(vertical_inventory_count):
        for x in range(horizontal_inventory_count):

            x_location = x * (icon_padding + icon_size)
            y_location = y * (icon_padding + icon_size)

            cropped_image: Image.Image = item_page_screenshot.crop((x_location, y_location, x_location + icon_size, y_location + icon_size))
            cropped_image.save("raw_images/{page}-{y}-{x}-icon.png".format(
                page=page,
                y=y,
                x=x,
            ))

    # Screenshot each hover textbox
    for y in range(vertical_inventory_count):
        for x in range(horizontal_inventory_count):
            mouse_x_location = first_item_x_coordinate + (x * (icon_padding + icon_size)) + (ui_size * native_mouse_offset)
            mouse_y_location = first_item_y_coordinate + (y * (icon_padding + icon_size)) + (ui_size * native_mouse_offset)

            mouse_move(mouse_x_location, mouse_y_location)
            time.sleep(0.1)

            text_x_location = mouse_x_location + text_x_offset
            text_y_location = mouse_y_location + text_y_offset
            text_width = window_width - text_x_location

            image_path = "raw_images/{page}-{y}-{x}-text.png".format(page=page, y=y, x=x)
            take_screenshot(text_x_location, text_y_location, text_width, text_size, image_path)

            # subprocess.run(["convert", color_image_path, "-grayscale", "Rec709Luma", "-brightness-contrast", "50x100%", image_path])


def scroll_down(
    first_item_x_coordinate: int,
    first_item_y_coordinate: int,
    ui_size: int
) -> None:

    scrollbar_x = first_item_x_coordinate + NATIVE_SCROLLBAR_X_OFFSET * ui_size
    scrollbar_y = first_item_y_coordinate + NATIVE_SCROLLBAR_Y_OFFSET * ui_size

    mouse_move(scrollbar_x, scrollbar_y)
    time.sleep(0.1)
    subprocess.run(["xdotool", "click", "--repeat", "5", "--delay", "200", "5"])




def main():
    anchor_position = pyautogui.locateOnScreen("menu_anchor.png")
    if anchor_position is None:
        raise ValueError("No Anchor found")

    page = 0
    while True:
        x = anchor_position.left + FIRST_ITEM_X_OFFSET_FROM_ANCHOR
        y = anchor_position.top + FIRST_ITEM_Y_OFFSET_FROM_ANCHOR

        screenshot_page(
            page=page,
            first_item_x_coordinate=x,
            first_item_y_coordinate=y,
            ui_size=2,
            window_width=1920,
        )

        try:
            pyautogui.locateOnScreen("completed_scrollbar.png")
            at_page_end = True
        except pyautogui.ImageNotFoundException:
            at_page_end = False
        
        if at_page_end:
            break

        scroll_down(x, y, 2)
        page += 1
main()
