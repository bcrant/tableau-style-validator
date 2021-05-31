from colorama import init, Fore, Back, Style
init(autoreset=True)


#
# Alert formatting
#
rm_fmt = Style.RESET_ALL
pass_fmt_on = Back.BLACK + Style.BRIGHT
pass_fmt_off = Style.NORMAL
fail_fmt_on = Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT
fail_fmt_off = Style.NORMAL + Fore.RESET


class Alerts:
    #
    # PASS
    #
    PASS_TESTS = str(Back.BLACK + Fore.GREEN + Style.BRIGHT + ' ✅\tVALID STYLES        ' + rm_fmt)

    # Fonts
    VALID_FONT_TYPE = str(pass_fmt_on + ' ✅\tVALID ' + pass_fmt_off + 'Font Type     ' + rm_fmt)
    VALID_FONT_SIZE = str(pass_fmt_on + ' ✅\tVALID ' + pass_fmt_off + 'Font Size     ' + rm_fmt)
    VALID_FONT_COLOR = str(pass_fmt_on + ' ✅\tVALID ' + pass_fmt_off + 'Font Color    ' + rm_fmt)

    # Borders
    VALID_BORDER_STYLE = str(pass_fmt_on + ' ✅\tVALID ' + pass_fmt_off + 'Border Style  ' + rm_fmt)
    VALID_BORDER_WIDTH = str(pass_fmt_on + ' ✅\tVALID ' + pass_fmt_off + 'Border Width  ' + rm_fmt)
    VALID_BORDER_COLOR = str(pass_fmt_on + ' ✅\tVALID ' + pass_fmt_off + 'Border Color  ' + rm_fmt)

    # Margins
    VALID_MARGIN = str(pass_fmt_on + ' ✅\tVALID ' + pass_fmt_off + 'Margin        ' + rm_fmt)
    VALID_MARGIN_TOP = str(pass_fmt_on + ' ✅\tVALID ' + pass_fmt_off + 'Margin Top    ' + rm_fmt)
    VALID_MARGIN_BOTTOM = str(pass_fmt_on + ' ✅\tVALID ' + pass_fmt_off + 'Margin Bottom ' + rm_fmt)
    VALID_PADDING = str(pass_fmt_on + ' ✅\tVALID ' + pass_fmt_off + 'Padding       ' + rm_fmt)

    # Background Color
    VALID_BACKGROUND_COLOR = str(pass_fmt_on + ' ✅\tVALID ' + pass_fmt_off + 'BG Color      ' + rm_fmt)

    #
    # FAIL
    #
    FAIL_TESTS = str(Back.BLACK + Fore.RED + Style.BRIGHT + ' ❌\tINVALID STYLES      ' + rm_fmt)

    # Fonts
    INVALID_FONT_TYPE = str(fail_fmt_on + ' ⚠️️\tALERT ' + fail_fmt_off + 'Font Type     ' + rm_fmt)
    INVALID_FONT_SIZE = str(fail_fmt_on + ' ⚠️\tALERT ' + fail_fmt_off + 'Font Size     ' + rm_fmt)
    INVALID_FONT_COLOR = str(fail_fmt_on + ' ⚠️\tALERT ' + fail_fmt_off + 'Font Color    ' + rm_fmt)

    # Borders
    INVALID_BORDER_STYLE = str(fail_fmt_on + ' ⚠️️\tALERT ' + fail_fmt_off + 'Border Style  ' + rm_fmt)
    INVALID_BORDER_WIDTH = str(fail_fmt_on + ' ⚠️\tALERT ' + fail_fmt_off + 'Border Width  ' + rm_fmt)
    INVALID_BORDER_COLOR = str(fail_fmt_on + ' ⚠️\tALERT ' + fail_fmt_off + 'Border Color  ' + rm_fmt)

    # Margins
    INVALID_MARGIN = str(fail_fmt_on + ' ⚠️️\tALERT ' + fail_fmt_off + 'Margin        ' + rm_fmt)
    INVALID_MARGIN_TOP = str(fail_fmt_on + ' ⚠️\tALERT ' + fail_fmt_off + 'Margin Top    ' + rm_fmt)
    INVALID_MARGIN_BOTTOM = str(fail_fmt_on + ' ⚠️\tALERT ' + fail_fmt_off + 'Margin Bottom ' + rm_fmt)
    INVALID_PADDING = str(fail_fmt_on + ' ⚠️\tALERT ' + fail_fmt_off + 'Padding       ' + rm_fmt)

    # Background Colors
    INVALID_BACKGROUND_COLOR = str(fail_fmt_on + ' ⚠️\tALERT ' + fail_fmt_off + 'BG Color      ' + rm_fmt)


def err_msg(count):
    if count == 0:
        return print(f'{Alerts.PASS_TESTS}')
    else:
        return print(f'{Alerts.FAIL_TESTS} {count} styles need revision.')


def msg(alert, value, pos=None, valid=True, level=None, kind=None):
    if valid:
        if 'font-size' in kind:
            return print(f'{alert} {str(value + "pt"):20s} found in {str(pos + ".")}')
        else:
            return print(f'{alert} {str(value):20s} found in {str(pos + ".")}')

    if not valid:
        if 'font-size' in kind:
            return print(f'{alert} {str(value + "pt"):20s} found in {str(pos):20s} of dashboard {str(level + ".")}')
        else:
            return print(f'{alert} {str(value):20s} found in {str(pos):20s} of dashboard {str(level + ".")}')
