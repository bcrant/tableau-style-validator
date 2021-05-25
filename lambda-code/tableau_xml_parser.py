from bs4 import BeautifulSoup
from helpers import pp, get_style_rules, get_styles_from_dict, get_distinct_styles, get_all_colors


def get_tableau_styles(workbook_file):
    # Create Beautiful Soup XML object from .twb file and remove thumbnail hash
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

    # #
    # # ALL COLORS IN WORKBOOK
    # #
    # wb['all_colors'] = get_all_colors(xml_soup)

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
        # TODO: Need to parse Dashboard Zones to get all titles / text...
        #       consider using foo.findAll('formatted-text') or wb_xml.findAll('run')
        #       to search the entire document and make sure none are missed
        if dashboard.find('style') is not None and bool(dashboard.find('style').contents):
            db_style_rules = get_style_rules(dashboard.find('style'))
            for k, v in db_style_rules.items():
                db[k] = v

        all_db_styles[db['db_name']] = db

    return {'dashboard_styles': all_db_styles}


if __name__ == "__main__":
    get_tableau_styles()
