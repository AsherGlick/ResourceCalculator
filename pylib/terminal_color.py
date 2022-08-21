FG_BLACK       = "\033[0;30m"
FG_BLACK_BOLD  = "\033[1;30m"
FG_RED         = "\033[0;31m"
FG_RED_BOLD    = "\033[1;31m"
FG_GREEN       = "\033[0;32m"
FG_GREEN_BOLD  = "\033[1;32m"
FG_YELLOW      = "\033[0;33m"
FG_YELLOW_BOLD = "\033[1;33m"
FG_BLUE        = "\033[0;34m"
FG_BLUE_BOLD   = "\033[1;34m"
FG_PURPLE      = "\033[0;35m"
FG_PURPLE_BOLD = "\033[1;35m"
FG_CYAN        = "\033[0;36m"
FG_CYAN_BOLD   = "\033[0;36m"
FG_WHITE       = "\033[0;37m"
FG_WHITE_BOLD  = "\033[1;37m"

BLACK  = 0
RED    = 1
GREEN  = 2
YELLOW = 3
BLUE   = 4
PURPLE = 5
CYAN   = 6
WHITE  = 7

RESET = "\033[0m"


def fg_gray(string: str) -> str:
    return FG_BLACK_BOLD + string + RESET
