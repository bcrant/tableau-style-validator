import re
import os
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from colorama import init, Fore, Back, Style
init(autoreset=True)


def init_env(lambda_event):
    # Determine whether running in remotely in AWS Lambda or locally. Load environment variables.
    if os.getenv('AWS_EXECUTION_ENV') is None:
        print('Operating in local dev context, loading ./envs/.env file...')
        load_dotenv('./envs/.env')
    else:
        print('Operating in Lambda context...')
        os.environ['TABLEAU_PATH'] = '/tmp/'
        if lambda_event.get('RESOURCE_LUID'):
            os.environ['RESOURCE_LUID'] = lambda_event.get('RESOURCE_LUID')


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


def pp(json_dict):
    # I prefer this to pprint
    return json.dumps(json_dict, indent=4, sort_keys=True)


def get_styles_from_dict(styles_soup):

    if styles_soup.find('formatted-text') is not None:

        # Get formatted text styles from customized label or tooltip
        style_runs = styles_soup\
            .find('formatted-text')\
            .findAll('run')

        styles_list = [
            style_run.attrs
            for style_run in style_runs
            if bool(style_run.attrs)
        ]
        # print('Getting styles from dict...')
        # print('Input: ', styles_soup)
        # print('Output: ', styles_list)
        return styles_list


def get_distinct_styles(style_dicts_list):
    # print('Getting distinct styles...')
    # print('Input: ', style_dicts_list)
    # print('Output: ', [dict(t) for t in {tuple(d.items()) for d in style_dicts_list}])
    return [dict(t) for t in {tuple(d.items()) for d in style_dicts_list}]


def get_style_rules(parent_node_soup):
    # Make sure not empty <style></style>
    node_dict = {}

    node_styles = parent_node_soup\
        .contents[0]\
        .split('<style-rule element=\'')

    list_elements = [i.strip() for i in node_styles if i.strip()]

    for element in list_elements:
        element_name = element.split('\'')[0]
        # TODO: Add support for Mark colors
        if 'mark' not in element_name:
            element_style = [i.strip() for i in element.split('\n')][1:]
            element_style_dict = {}
            for s in element_style:
                s_attrs = s.strip('<format').strip(' />').split(' ', 1)

                tmp_dict = {}
                for item in s_attrs:
                    pairs = re.sub("\'", '', item).split('=')
                    it = iter(pairs)
                    pair_dict = dict(zip(it, it))
                    for k, v in pair_dict.items():
                        tmp_dict[k] = v
                element_style_dict[tmp_dict.get('attr')] = tmp_dict.get('value')

            node_dict[element_name] = element_style_dict

    # print('Getting style rules...')
    # print('Input: ', parent_node_soup)
    # print('Output: ', node_dict)
    return node_dict


def get_all_colors(xml_soup):
    colors_used = []
    all_styles_list = xml_soup.findAll('style', recursive=True)
    for s in all_styles_list:
        for line in s.string.split('\n'):
            if '#' in line.strip():
                hex_num = line.split('#')[1][:6]
                if hex_num not in colors_used and hex_num.isalnum():
                    colors_used.append(hex_num)

    hex_colors_used = ['#' + h for h in colors_used]

    return hex_colors_used


# def convert_filetype():
#     """Convert local .twb to .xml file extension"""
#     # (This function does not appear to be necessary, commenting out for now)
#     tableau_file_path = 'example_style_guide_two.twb'
#     base = os.path.splitext(tableau_file)[0]
#     os.rename(tableau_file, base + '.xml')
