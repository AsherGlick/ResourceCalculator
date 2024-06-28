from PIL import Image # type:ignore
from typing import List, Dict, Tuple, Optional
import shutil
import json
import math

letters = {
    "042a2a2a1e":"a",
    "fe1222221c":"b",
    "1c22222214":"c",
    "1c222212fe":"d",
    "1c2a2a2a1a":"e",
    "207ea0a0":"f",
    "192525253e":"g",
    "fe1020201e":"h",
    "be":"i",
    "06010101BE":"j",  # No minecraft item has a lower case j in it, this is manually added
    "fe081422":"k",
    "fc02":"l",
    "3e2018201e":"m",
    "3e2020201e":"n",
    "1c2222221c":"o",
    "3f14242418":"p",
    "182424143f":"q",
    "3e10202010":"r",
    "122a2a2a24":"s",
    "20fc22":"t",
    "3c0202023e":"u",
    "3804020438":"v",
    "3c020e023e":"w",
    "2214081422":"x",
    "390505053e":"y",
    "22262a3222":"z",
    "7ea0a0a07e":"A",
    "fea2a2a25c":"B",
    "7c82828244":"C",
    "fe8282827c":"D",
    "fea2a28282":"E",
    "fea0a08080":"F",
    "7c8282a2bc":"G",
    "fe202020fe":"H",
    "82fe82":"I",
    "04020202fc":"J",
    "fe2020508e":"K",
    "fe02020202":"L",
    "fe402040fe":"M",
    "fe402010fe":"N",
    "7c8282827c":"O",
    "fea0a0a040":"P",
    "7c8282847a":"Q",
    "fea0a0a05e":"R",
    "44a2a2a29c":"S",
    "8080fe8080":"T",
    "fc020202fc":"U",
    "f00c020cf0":"V",
    "fe040804fe":"W",
    "8E5020508E":"X",  # No minecraft item has a capital X in it so this is manually added
    "80403e4080":"Y",
    "868a92a2c2":"Z",
    "c0":"'", # This is needed for things like "Jack o'Lantern"
}


################################################################################
# Converts an array of booleans into a hex string assuming each bool represents
# a 1 or 0 in a bytes.
#
# from https://stackoverflow.com/questions/25583312
################################################################################
def bool_array_to_hex(bool_array: List[bool]) -> str:
    zero_one = map(int, bool_array)
    n = int(''.join(map(str, zero_one)), 2)
    return '{:02x}'.format(n)


# Keep track of any duplicate names so we can append an integer suffix
duplicate_names: Dict[str,int] = {}


################################################################################
# Run through each file generated with dice_screenshots.sh and attempt to read
# the text screenshot to rename the icon screenshot. Duplicate names will be
# appended with a _2 or _3 etc.
################################################################################
def main(ui_size: int) -> None:
    item_ordering = []
    for i in range(37):
        item_ordering += parse_page(i, ui_size)

    with open("item_ordering.json", 'w') as f:
        json.dump(item_ordering, f)



def parse_page(page_index: int, ui_size: int) -> List[str]:
    item_ordering = []
    for y in range(5):
        for x in range(9):
            raw_icon_path = "raw_images/{page}-{y}-{x}-icon.png".format(
                page=page_index,
                x=x,
                y=y,
            )
            raw_text_path = "raw_images/{page}-{y}-{x}-text.png".format(
                page=page_index,
                x=x,
                y=y
            )

            decoded_name = decode_image_text(raw_text_path, ui_size)
            print(decoded_name)
            item_ordering.append(decoded_name)

            # Convert to lowercase and strip symbols
            decoded_name = decoded_name.lower()
            decoded_name = decoded_name.replace("'", "")

            if decoded_name in duplicate_names:
                duplicate_names[decoded_name] += 1
                decoded_name = decoded_name + "_" + str(duplicate_names[decoded_name])
            else:
                duplicate_names[decoded_name] = 1

            target_file_name = "named_images/" + decoded_name + ".png"

            shutil.copyfile(raw_icon_path, target_file_name)

    return item_ordering


endpurple_light = "2a0a59"
background_light = "ffffff"

endpurple_dark = "260558"
background_dark = "8b8b8b"

VALID_TEXT_COLORS = set([
    (252, 252, 252), # White
    (84, 252, 252), # Teal
    (252, 168, 0), # Orange
    (252, 252, 84), # Yellow
    (252, 84, 252), # Purple
])
################################################################################
# Read the text-image file and attempt to decode the letters. This is done by
# looking at one column at a time and from top to bottom converting each pixel
# into a 1 or a 0. White pixels become 1's and black pixels becomes 0's. This
# data is then converted into a hexadecimal string and added to the character
# identifier. When a column of all black pixels is found the character
# identifier is used to look up what character it is from the `letters` map.
# The mapped character is then added to the output string and the character
# identifier is reset for the next character.
#
# Because there is some noise data at the end we filter out anything that is
# longer then 10 pixels wide. We also have a set of "bad" characters in the
# `letters` map which usually correspond to vertical white lines of varying
# widths.
#
# This decoder does not handles spaces currently because it has not been a
# required feature, because spaces get stripped out later in the pipeline.
################################################################################
def decode_image_text(filename: str, ui_size: int) -> str:

    has_error = False

    letter_hexes: List[str] = []

    letter_rows: List[str] = []

    with Image.open(filename) as im:
        pixels = im.convert("RGB").load()
        width, height = im.size

        # Track the previous blue channel value for the purple blue outline box
        # that outlines the hover textbox we are parsing so we can determine
        # when the line ends and we can stop searching for more letters.
        previous_outline_blue_channel: Optional[int] = None


        # Iterate over all the columns and rows, but skip each other row/column
        # because all the pixels in the text screenshots are 2x2 blocks of
        # color because minecraft is at GUI scale 2.
        for x in range(0, width, ui_size):
            outline_blue_channel = pixels[x, 0][2]

            # Trace the purple blue outline box to determine when the textbox
            # ends to stop searching for more letters
            if (
                previous_outline_blue_channel != None
                and outline_blue_channel < previous_outline_blue_channel - 20
            ):
                break
            previous_outline_blue_channel = outline_blue_channel

            column_bits = []
            for y in range(3 * ui_size, height, ui_size):
                
                color = pixels[x,y]
                if color in VALID_TEXT_COLORS:
                    column_bits.append(True)
                else:
                    column_bits.append(False)

            column = bool_array_to_hex(column_bits)

            if column == "00":
                letter_hexes.append("".join(letter_rows))
                letter_rows = []
            else:
                letter_rows.append(column)


    decoded_letters: List[str] = []

    for letterhex in letter_hexes:
        if letterhex == "":
            continue

        if len(letterhex) > 10:
            # print("Probably not a letter")
            continue

        if letterhex in letters:
            decoded_letters.append(letters[letterhex])

        else:
            raise ValueError("Unknown Hex {} after {}? ({})".format(letterhex, "".join(decoded_letters), filename))

    if len(decoded_letters) == 0:
        raise ValueError("Zero Length Name {}".format(filename))

    return "".join(decoded_letters)

# Run the OCR renamer
main(
    ui_size=2,
)