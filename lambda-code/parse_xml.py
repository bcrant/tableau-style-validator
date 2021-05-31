import collections
from bs4 import BeautifulSoup
from helpers import get_style_rules, get_styles_from_dict, get_distinct_styles, get_all_colors


def get_tableau_styles(workbook_file):
    # Create Beautiful Soup XML object from .twb file
    wb_xml = BeautifulSoup(workbook_file, 'lxml')

    #
    # Call parsing functions and create new dictionary
    #
    style_dict = {
        **parse_workbook_style(wb_xml),
        **parse_worksheets(wb_xml),
        **parse_dashboards(wb_xml)
    }

    return style_dict


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
    wb['all_colors_in_wb'] = get_all_colors(xml_soup)

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
            # # TABLE STYLES
            # # (Excluding until later iterations)
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
        if dashboard.find('style') is not None and bool(dashboard.find('style').contents):
            db_style_rules = get_style_rules(dashboard.find('style'))
            for k, v in db_style_rules.items():
                db[k] = v

        #
        # DASHBOARD ZONES
        #
        if dashboard.find('zones') is not None:
            db_zones = dashboard.findAll('zones')

            # Formatted Text Items
            db_zones_text_styles = []
            for z_text in db_zones:
                db_text_style_attrs = get_styles_from_dict(z_text)
                if bool(db_text_style_attrs):
                    db_zones_text_styles += get_distinct_styles(db_text_style_attrs)

            # Get all text item values per unique key
            db_zones_text_styles_dict = collections.defaultdict(list)
            for d in db_zones_text_styles:
                for a, b in d.items():
                    db_zones_text_styles_dict[a].extend([b])
            db_text_styles = dict(db_zones_text_styles_dict.items())
            for k, v in db_text_styles.items():
                db_text_styles[k] = list(dict.fromkeys(v).keys())[0]

            # Normalize the key names for validation
            if db_text_styles.get('fontname') is not None:
                db_text_styles['font-family'] = db_text_styles.pop('fontname')
            if db_text_styles.get('fontsize') is not None:
                db_text_styles['font-size'] = db_text_styles.pop('fontsize')
            if db_text_styles.get('fontcolor') is not None:
                db_text_styles['font-color'] = db_text_styles.pop('fontcolor')

            db['db_text_styles'] = db_text_styles

            # Zone Style Items
            db_zone_styles = []
            for z_style in db_zones:
                z_style_list = [e.findAll('format') for e in z_style.findAll('zone-style')]
                for z_list in z_style_list:
                    db_zone_styles.extend([f.attrs for f in z_list])

            db_zone_styles_dict = collections.defaultdict(list)
            for z_style_pair in get_distinct_styles(db_zone_styles):
                db_zone_styles_dict[z_style_pair.get('attr')].extend([z_style_pair.get('value')])

            db['db_zone_styles'] = dict(db_zone_styles_dict.items())

        all_db_styles[db['db_name']] = db

    return {'dashboard_styles': all_db_styles}
