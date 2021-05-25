import re
import json
from colorama import Fore, Back, Style
from bs4 import BeautifulSoup


class Alerts:
    FONT_TYPE = str(Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + ' ⚠️️\tALERT ' + Style.NORMAL + Fore.RESET + 'Font Type  ' + Style.RESET_ALL)
    FONT_SIZE = str(Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + ' ⚠️\tALERT ' + Style.NORMAL + Fore.RESET + 'Font Size  ' + Style.RESET_ALL)
    FONT_COLOR = str(Back.BLACK + Fore.LIGHTYELLOW_EX + Style.BRIGHT + ' ⚠️\tALERT ' + Style.NORMAL + Fore.RESET + 'Font Color ' + Style.RESET_ALL)
    PASS_TESTS = str(Back.BLACK + Fore.GREEN + Style.BRIGHT + ' ✅\tVALID STYLES   ' + Style.RESET_ALL)
    FAIL_TESTS = str(Back.BLACK + Fore.RED + Style.BRIGHT + ' ❌\tINVALID STYLES   ' + Style.RESET_ALL)


def err_msg(count):
    if count == 0:
        return print(f'{Alerts.PASS_TESTS}')
    else:
        return print(f'{Alerts.FAIL_TESTS} {count} styles need revision.')


def pp(json_dict):
    # I prefer this to pprint
    return json.dumps(json_dict, indent=4, sort_keys=True)


def get_styles_from_dict(styles_soup):
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
