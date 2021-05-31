
#
# SLACK Alert formatting
#
class SlackAlerts:
    #
    # PASS
    #
    PASS_TESTS = str('  :white_check_mark:  *VALID STYLES*        ')

    # Fonts
    VALID_FONT_TYPE = str('  :white_check_mark:  ' + 'Font Type     ')
    VALID_FONT_SIZE = str('  :white_check_mark:  ' + 'Font Size     ')
    VALID_FONT_COLOR = str('  :white_check_mark:  ' + 'Font Color    ')

    # Borders
    VALID_BORDER_STYLE = str('  :white_check_mark:  ' + 'Border Style  ')
    VALID_BORDER_WIDTH = str('  :white_check_mark:  ' + 'Border Width  ')
    VALID_BORDER_COLOR = str('  :white_check_mark:  ' + 'Border Color  ')

    # Margins
    VALID_MARGIN = str('  :white_check_mark:  ' + 'Margin        ')
    VALID_MARGIN_TOP = str('  :white_check_mark:  ' + 'Margin Top    ')
    VALID_MARGIN_BOTTOM = str('  :white_check_mark:  ' + 'Margin Bottom ')
    VALID_PADDING = str('  :white_check_mark:  ' + 'Padding       ')

    # Background Color
    VALID_BACKGROUND_COLOR = str('  :white_check_mark:  ' + 'BG Color      ')

    #
    # FAIL
    #
    FAIL_TESTS = str('  :x:  *INVALID STYLES*   ')

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
        return str(f'{SlackAlerts.FAIL_TESTS}   {count} styles need revision.')


def slack_msg(alert, value, pos=None, valid=True, level=None, kind=None):
    # If you do not wish to see the valid statements,
    # you can comment this first "if valid" clause out.
    if valid:
        if 'font-size' in kind:
            return str(f'{alert} {str(value + "pt"):12s} found in {str(pos + "  ")}')
        else:
            return str(f'{alert} {str(value):12s} found in {str(pos + "  ")}')

    if not valid:
        if 'font-size' in kind:
            return str(f'{alert} {str(value + "pt"):12s} found in {str(pos)} of {str("*" + level + "*  ")}')
        else:
            return str(f'{alert} {str(value):12s} found in {str(pos)} of {str("*" + level + "*  ")}')

