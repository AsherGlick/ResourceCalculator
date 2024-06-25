import enum
from typing import Optional


################################################################################
# TerminalColor
#
# An enum class that represents all of the colors that can be displayed in an
# ANSII terminal, mapped to the stringy integer that represents them.
################################################################################
class TerminalColor(enum.Enum):
    black = "0"
    red = "1"
    green = "2"
    yellow = "3"
    blue = "4"
    purple = "5"
    cyan = "6"
    white = "7"

    default = "9"


# Helper variable to reset any color
RESET = "\033[0m"


################################################################################
# get_color_escape_codes
#
# Creates an ANSII color escape code given different parameters about the color
# to be used.
################################################################################
def get_color_escape_code(
    bold: bool,
    foreground_color: Optional[TerminalColor],
    background_color: Optional[TerminalColor]
) -> str:
    return "".join([
        "\033[",
        ("1" if bold else "0"),
        (";3" + foreground_color.value if foreground_color is not None else ""),
        (";4" + background_color.value if background_color is not None else ""),
        "m",
    ])


################################################################################
# get_colored_text
#
# A function that wraps some input text in color escape codes.
################################################################################
def get_colored_text(
    text: str,
    bold: bool,
    foreground_color: Optional[TerminalColor],
    background_color: Optional[TerminalColor]
) -> str:
    return get_color_escape_code(bold, foreground_color, background_color) + text + RESET


################################################################################
# print_color_cube
#
# A helper text function that prints out all the color combinations to the
# terminal to test the terminal's color display.
################################################################################
def print_color_cube() -> None:
    colors = {
        TerminalColor.black: "K",
        TerminalColor.red: "R",
        TerminalColor.green: "G",
        TerminalColor.yellow: "Y",
        TerminalColor.blue: "B",
        TerminalColor.purple: "P",
        TerminalColor.cyan: "C",
        TerminalColor.white: "W",
        TerminalColor.default: "D",
        None: "N",
    }

    for bg, bg_shortcut in colors.items():
        for bold in [False, True]:
            for fg, fg_shortcut in colors.items():
                color_code = ("1" if bold else "0") + fg_shortcut + bg_shortcut
                print(get_colored_text(color_code, bold, fg, bg), end="")
        print()


################################################################################
# fg_gray
#
# A helper function for getting a grey colored text by making a bold black text
################################################################################
def fg_gray(string: str) -> str:
    return get_colored_text(
        text=string,
        bold=True,
        foreground_color=TerminalColor.black,
        background_color=None,
    )
