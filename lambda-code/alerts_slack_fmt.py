
#
# SLACK Alert formatting
#
class SlackAlerts:
    #
    # PASS
    #
    PASS_TESTS = str(' ✅\tVALID STYLES        ')

    # Fonts
    VALID_FONT_TYPE = str(' ✅\tVALID ' + 'Font Type     ')
    VALID_FONT_SIZE = str(' ✅\tVALID ' + 'Font Size     ')
    VALID_FONT_COLOR = str(' ✅\tVALID ' + 'Font Color    ')

    # Borders
    VALID_BORDER_STYLE = str(' ✅\tVALID ' + 'Border Style  ')
    VALID_BORDER_WIDTH = str(' ✅\tVALID ' + 'Border Width  ')
    VALID_BORDER_COLOR = str(' ✅\tVALID ' + 'Border Color  ')

    # Margins
    VALID_MARGIN = str(' ✅\tVALID ' + 'Margin        ')
    VALID_MARGIN_TOP = str(' ✅\tVALID ' + 'Margin Top    ')
    VALID_MARGIN_BOTTOM = str(' ✅\tVALID ' + 'Margin Bottom ')
    VALID_PADDING = str(' ✅\tVALID ' + 'Padding       ')

    # Background Color
    VALID_BACKGROUND_COLOR = str(' ✅\tVALID ' + 'BG Color      ')

    #
    # FAIL
    #
    FAIL_TESTS = str(' :x: INVALID STYLES      ')

    # Fonts
    INVALID_FONT_TYPE = str('  :warning:  *ALERT*  ' + 'Font Type     ')
    INVALID_FONT_SIZE = str('  :warning:  *ALERT*  ' + 'Font Size     ')
    INVALID_FONT_COLOR = str('  :warning:  *ALERT*  ' + 'Font Color    ')

    # Borders
    INVALID_BORDER_STYLE = str('  :warning:  *ALERT*  ' + 'Border Style  ')
    INVALID_BORDER_WIDTH = str('  :warning:  *ALERT*  ' + 'Border Width  ')
    INVALID_BORDER_COLOR = str('  :warning:  *ALERT*  ' + 'Border Color  ')

    # Margins
    INVALID_MARGIN = str('  :warning:  *ALERT*  ' + 'Margin        ')
    INVALID_MARGIN_TOP = str('  :warning:  *ALERT*  ' + 'Margin Top    ')
    INVALID_MARGIN_BOTTOM = str('  :warning:  *ALERT*  ' + 'Margin Bottom ')
    INVALID_PADDING = str('  :warning:  *ALERT*  ' + 'Padding       ')

    # Background Colors
    INVALID_BACKGROUND_COLOR = str('  :warning:  *ALERT*  ' + 'BG Color      ')


def slack_err_msg(count):
    if count == 0:
        return str(f'{SlackAlerts.PASS_TESTS}')
    else:
        return str(f'{SlackAlerts.FAIL_TESTS} {count} styles need revision.')


def slack_msg(alert, value, pos=None, valid=True, level=None, kind=None):
    # If you do not wish to see the valid statements,
    # you can comment this first "if valid" clause out.
    if valid:
        if 'font-size' in kind:
            return str(f'{alert} {str(value + "pt"):12s} found in {str(pos + ".")}')
        else:
            return str(f'{alert} {str(value):12s} found in {str(pos + ".")}')

    if not valid:
        if 'font-size' in kind:
            return str(f'{alert} {str(value + "pt"):12s} found in {str(pos)} of {str("*" + level + "*")}')
        else:
            return str(f'{alert} {str(value):12s} found in {str(pos)} of {str("*" + level + "*")}')

