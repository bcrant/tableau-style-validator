from textwrap import dedent
from helpers import left_align_list


#
# SLACK Alert formatting
#
class SlackAlerts:
    #
    # PASS
    #
    PASS_TESTS = str('{:2s}  *{:19s}*'.format(str(':white_check_mark:'), str('VALID STYLES')))

    # Fonts
    VALID_FONT_TYPE = str('{:4s}  {:4s}  {:12}'.format(str(':ballot_box_with_check:'), str('VALID'), str('Font Type')))
    VALID_FONT_SIZE = str('{:4s}  {:4s}  {:13}'.format(str(':ballot_box_with_check:'), str('VALID'), str('Font Size')))
    VALID_FONT_COLOR = str('{:4s}  {:4s}  {:12}'.format(str(':ballot_box_with_check:'), str('VALID'), str('Font Color')))

    # Borders
    VALID_BORDER_STYLE = str('  :ballot_box_with_check:  ' + 'Border Style  ')
    VALID_BORDER_WIDTH = str('  :ballot_box_with_check:  ' + 'Border Width  ')
    VALID_BORDER_COLOR = str('  :ballot_box_with_check:  ' + 'Border Color  ')

    # Margins
    VALID_MARGIN = str('  :ballot_box_with_check:  ' + 'Margin        ')
    VALID_MARGIN_TOP = str('  :ballot_box_with_check:  ' + 'Margin Top    ')
    VALID_MARGIN_BOTTOM = str('  :ballot_box_with_check:  ' + 'Margin Bottom ')
    VALID_PADDING = str('  :ballot_box_with_check:  ' + 'Padding       ')

    # Background Color
    VALID_BACKGROUND_COLOR = str('  :ballot_box_with_check:  ' + 'BG Color      ')

    #
    # FAIL
    #
    FAIL_TESTS = str('{:2s}  *{:16s}*'.format(str(':x:'), str('INVALID STYLES')))

    # Fonts
    INVALID_FONT_TYPE = str('{:4s}  {:4s}  {:12}'.format(str(':warning:'), str('ALERT'), str('Font Type')))
    INVALID_FONT_SIZE = str('{:4s}  {:4s}  {:12}'.format(str(':warning:'), str('ALERT'), str('Font Size')))
    INVALID_FONT_COLOR = str('{:4s}  {:4s}  {:12}'.format(str(':warning:'), str('ALERT'), str('Font Color')))

    # Borders
    INVALID_BORDER_STYLE = str('  :warning:  ALERT  ' + 'Border Style  ')
    INVALID_BORDER_WIDTH = str('  :warning:  ALERT  ' + 'Border Width  ')
    INVALID_BORDER_COLOR = str('  :warning:  ALERT  ' + 'Border Color  ')

    # Margins
    INVALID_MARGIN = str('  :warning:  ALERT  ' + 'Margin        ')
    INVALID_MARGIN_TOP = str('  :warning:  ALERT  ' + 'Margin Top    ')
    INVALID_MARGIN_BOTTOM = str('  :warning:  ALERT  ' + 'Margin Bottom ')
    INVALID_PADDING = str('  :warning:  ALERT  ' + 'Padding       ')

    # Background Colors
    INVALID_BACKGROUND_COLOR = str('  :warning:  ALERT  ' + 'BG Color      ')


def slack_err_msg(invalid_count):
    if invalid_count > 0:
        return str(f'  {SlackAlerts.FAIL_TESTS}   {invalid_count} styles need revision  ')
    else:
        return str(f'\n  :white_check_mark:  No invalid styles found in component  ')


def slack_valid_msg(valid_count):
    if valid_count > 0:
        return str(f'  {SlackAlerts.PASS_TESTS}   {valid_count} valid styles found  ')
    else:
        return str(f'\n  :exclamation:  No valid styles found in component  ')


def slack_msg(alert, value, pos=None, valid=True, level=None, kind=None):
    # If you do not wish to see the valid statements,
    # you can comment this first "if valid" clause out.
    if valid:
        if 'font-size' in kind:
            return str('  {}  `{:16s}`  found in _{}_ of {}  '
                       .format(str(alert), str(value + "pt"), str(pos), str(level)))
        else:
            return str('  {}  `{:16s}`  found in _{}_ of {}  '
                       .format(str(alert), str(value), str(pos), str(level)))

    if not valid:
        if 'font-size' in kind:
            return str('  {}  `{:16s}`  found in _{}_ of {}  '
                       .format(str(alert), str(value + "pt"), str(pos), str(level)))
        else:
            return str('  {} `{:16s}`  found in _{}_ of {}  '
                       .format(str(alert), str(value), str(pos), str(level)))


def fmt_slack_output(valid_styles=None, invalid_styles=None):
    return dedent('''
{spacer}
{invalid}
{spacer}
{valid}
{spacer}
    '''.format(spacer='\n\n',
               invalid=left_align_list(invalid_styles) if invalid_styles else None,
               valid=left_align_list(valid_styles) if valid_styles else None))
