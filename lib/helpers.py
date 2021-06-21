import re
import os
import json
import collections
from textwrap import dedent
from dotenv import load_dotenv


#
# Runtime specific environment variables
#
def init_env(lambda_event):
    # Determine whether running in remotely in AWS Lambda or locally. Load environment variables.
    if os.getenv('AWS_EXECUTION_ENV') is None:
        print('Operating in local dev context, loading ./envs/.env file...')
        load_dotenv('./envs/.env')
    else:
        print('Operating in Lambda context...')
        os.environ['TABLEAU_PATH'] = '/tmp/'
        os.environ['STYLE_GUIDE_PATH'] = './example_style_guide.json'
        if lambda_event.get('RESOURCE_LUID'):
            os.environ['RESOURCE_LUID'] = lambda_event.get('RESOURCE_LUID')


#
# Print and output Formatters
#
def pp(json_dict):
    # I prefer this to pprint
    return json.dumps(json_dict, indent=4, sort_keys=True)


def left_align_list(style_list):
    return '\n'.join(map(str, style_list))


def fmt_output(valid_styles=None, invalid_styles=None):
    return dedent('''
{invalid}

{valid}

    '''.format(invalid=left_align_list(invalid_styles) if invalid_styles else None,
               valid=left_align_list(valid_styles) if valid_styles else None))


#
# Parsing patterns
#
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

    if parent_node_soup.contents:
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
        for line in str(s).split('\n'):
            if '#' in line.strip():
                hex_num = line.split('#')[1][:6]
                if hex_num not in colors_used and hex_num.isalnum():
                    colors_used.append(hex_num)

    hex_colors_used = ['#' + h for h in colors_used]

    return hex_colors_used


def one_to_many_dict(list_of_style_dicts):
    out_dict = collections.defaultdict(list)
    for style_dict in list_of_style_dicts:
        if style_dict is not None:
            for k, v in style_dict.items():
                out_dict[k].extend([v])
        many_dict = dict(out_dict.items())
        for kk, vv in many_dict.items():
            many_dict[kk] = list(dict.fromkeys(vv))

        # print('Getting valid styles dict...')
        # print('Input: ', list_of_style_dicts)
        # print('Output: ', many_dict)
        return many_dict
