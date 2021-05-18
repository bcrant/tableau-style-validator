import re
import json
import pprint
from bs4 import BeautifulSoup


def parse_tableau_styles():
    # Read file and create Beautiful Soup object
    infile = open('tests/c.twb', 'rw')

    contents = infile.read()
    soup = BeautifulSoup(contents, 'lxml')

    style_dict = {
        **parse_workbook_style(soup),
        **parse_worksheets(soup),
        **parse_dashboards(soup)
    }

    return pprint.pprint(style_dict)


def parse_workbook_style(xml_soup):

    workbook_style = xml_soup.find('style')

    wb = {}

    #
    # WORKBOOK STYLE
    #
    if workbook_style is not None:
        wb_style_rules = get_style_rules(workbook_style)

        for k, v in wb_style_rules.items():
            wb[k] = v

    #
    # ALL COLORS IN WORKBOOK
    #
    wb['all_colors'] = parse_all_colors(xml_soup)

    return {'workbook_styles': wb}


def parse_worksheets(xml_soup):

    worksheets = xml_soup.find_all('worksheet')

    all_ws_styles = {}

    for worksheet in worksheets:
        #
        # WORKSHEET NAME
        #
        ws = {
            'ws_name': worksheet['name']
        }

        #
        # WORKSHEET TITLE OR SUBTITLE STYLES
        #
        if worksheet.find('layout-options') is not None:
            title_styles = worksheet\
                .find('layout-options')\
                .find('title')

            if title_styles is not None:
                title_styles_list = get_styles_from_dict(title_styles)
                if bool(title_styles_list):
                    ws['ws_title_styles'] = title_styles_list

            title = title_styles\
                .find('formatted-text')\
                .findAll('run')

            for t in title:
                if bool(t.text):
                    ws['ws_title'] = t.text.strip()

        #
        # WORKSHEET TABLE AND PANE STYLES
        #
        if worksheet.find('table') is not None:
            #
            # CUSTOMIZED TOOLTIPS
            #
            tooltip_styles = worksheet\
                .find('table')\
                .find('panes')\
                .find('pane')\
                .find('customized-tooltip')

            if tooltip_styles is not None:
                tooltip_styles_list = get_styles_from_dict(tooltip_styles)
                if bool(tooltip_styles_list):
                    ws['ws_tooltip_styles'] = get_distinct_styles(tooltip_styles_list)

            #
            # CUSTOMIZED LABELS
            #
            label_styles = worksheet\
                .find('table')\
                .find('panes')\
                .find('pane')\
                .find('customized-label')

            if label_styles is not None:
                label_styles_list = get_styles_from_dict(label_styles)
                if bool(label_styles_list):
                    ws['ws_labels'] = get_distinct_styles(label_styles_list)

            # #
            # # (Excluding until later iterations) TABLE STYLES
            # #
            # table_elements = worksheet\
            #     .find('table')\
            #     .findAll('style', recursive=False)[0]\
            #     .contents[0]\
            #     .split('<style-rule element=\'')
            #
            # element_styles = {}
            # for element in table_elements:
            #     element_fmt = [
            #         fmt.strip()
            #         for fmt in element.split('\n')
            #     ]
            #     element_styles[element_fmt[0].split('\'')[0]] = list(filter(None, element_fmt[1:]))

        all_ws_styles[worksheet['name']] = ws

    return {'worksheet_styles': all_ws_styles}


def parse_dashboards(xml_soup):

    dashboards = xml_soup.find_all('dashboard')

    all_db_styles = {}

    for dashboard in dashboards:
        #
        # DASHBOARD NAME AND SIZE
        #
        db = {
            'db_name': dashboard['name'],
            'db_size': dashboard.find('size').attrs
        }

        #
        # DASHBOARD TITLE STYLES
        #
        if dashboard.find('layout-options') is not None:
            db_title_styles = dashboard \
                .find('layout-options') \
                .find('title')

            if db_title_styles is not None:
                db_title_styles_list = get_styles_from_dict(db_title_styles)
                if bool(db_title_styles_list):
                    db['db_title_styles'] = db_title_styles_list

                db_title = db_title_styles\
                    .find('formatted-text')\
                    .findAll('run')

                for t in db_title:
                    if bool(t.text):
                        db['db_title'] = t.text.strip()

        #
        # DASHBOARD ELEMENT STYLES (EXCLUDING ZONES)
        #
        if dashboard.find('style') is not None:
            db_style_rules = get_style_rules(dashboard.find('style'))

            for k, v in db_style_rules.items():
                db[k] = v

        all_db_styles[db['db_name']] = db

    return {'dashboard_styles': all_db_styles}


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

    return styles_list


def get_distinct_styles(style_dicts_list):
    return [dict(t) for t in {tuple(d.items()) for d in style_dicts_list}]


def get_style_rules(parent_node_soup):
    node_dict = {}

    node_styles = parent_node_soup\
        .contents[0]\
        .split('<style-rule element=\'')

    list_elements = [i.strip() for i in node_styles if i.strip()]

    for element in list_elements:
        element_name = element.split('\'')[0]
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

    return node_dict


def parse_all_colors(xml_soup):
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


if __name__ == "__main__":
    parse_tableau_styles()
