from PIL import Image
import shutil

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
    "06010101BE":"j", # No minecraft item has a lower case j in it, this is manually added
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
    "8E5020508E":"X", # No minecraft item has a capital X in it so this is manually added
    "80403e4080":"Y",
    "868a92a2c2":"Z",
    "c0":"'",

    # JUNK CHARACTERS
    "ff": "",
    "ffff": "",
    "ffffff": "",
    "ffffffff": "",
    "ffffffffff": "",
}

# from https://stackoverflow.com/questions/25583312
def bool_array_to_hex(bool_array):
    zero_one = map(int, bool_array)
    n = int(''.join(map(str, zero_one)), 2)
    return '{:02x}'.format(n)


duplicate_names = {}


def main():
    # for image_index in range(0, 44):
    for image_index in range(0, 1350):
        text_image_filename = "image_text/" + str(image_index) + ".png"
        block_image_filename = "diced_images/" + str(image_index) + ".png"

        decoded_name = decode_image_text(text_image_filename)

        decoded_name = decoded_name.lower()
        decoded_name = decoded_name.replace("'", "")

        if decoded_name in duplicate_names:
            duplicate_names[decoded_name] += 1
            decoded_name = decoded_name + "_" + str(duplicate_names[decoded_name])

        else:
            duplicate_names[decoded_name] = 2

        target_file_name = "named_images/" + decoded_name + ".png"

        shutil.copyfile(block_image_filename, target_file_name)

################################################################################
#
################################################################################
def decode_image_text(filename):

    has_error = False

    letter_hexes = []

    letter_rows = []

    with Image.open(filename) as im:
        pixels = im.load()
        width, height = im.size

        for x in range(0,width,2):
            column_bits = []
            for y in range(0,height,2):
                
                color = pixels[x,y]
                if color > 128:
                    column_bits.append(True)
                else:
                    column_bits.append(False)

            column = bool_array_to_hex(column_bits)

            if column == "00":
                letter_hexes.append("".join(letter_rows))
                letter_rows = []
            else:
                letter_rows.append(column)


    decoded_letters = []

    for letterhex in letter_hexes:
        if letterhex == "":
            continue

        if len(letterhex) > 10:
            # print("Probably not a letter")
            continue

        if letterhex in letters:
            decoded_letters.append(letters[letterhex])

        else:
            print("Unknown Hex {} after {}?".format(letterhex, "".join(decoded_letters)))
            decoded_letters.append("_")
            has_error = True

    return "".join(decoded_letters)


main()