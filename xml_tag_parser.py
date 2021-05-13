import re
import pprint
from bs4 import BeautifulSoup


def parse_tableau_styles():
    infile = open('example_style_guide.xml', 'r')
    contents = infile.read()
    soup = BeautifulSoup(contents, 'lxml')

    parse_workbook_style(soup)

    style_dict = {
        **parse_workbook_style(soup),
        **parse_worksheets(soup),
        **parse_dashboards(soup)
    }

    return pprint.pprint(style_dict)


def parse_workbook_style(xml_soup):

    workbook_style = xml_soup.find('style')

    wb = {}

    if workbook_style is not None:
        wb_style = workbook_style\
            .contents[0]\
            .split('<style-rule element=\'')

        list_elements = [i.strip() for i in wb_style if i.strip()]

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

            wb[element_name] = element_style_dict

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
            # # Table Styles
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
            #
            #     element_styles[element_fmt[0].split('\'')[0]] = list(filter(None, element_fmt[1:]))

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

        all_ws_styles[worksheet['name']] = ws

    return all_ws_styles


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
            runs = dashboard\
                .find('layout-options')\
                .find('title')\
                .find('formatted-text')\
                .findAll('run', recursive=False)

            title = []
            title_font_attributes = []
            for run in runs:
                title.append(run.text)
                title_font_attributes.append({k: v for k, v in run.attrs.items()})

            db['db_title'] = title[0]
            db['db_title_font_attributes'] = list(filter(None, title_font_attributes))

        #
        # DASHBOARD ELEMENT STYLES (EXCLUDING ZONES)
        #
        if dashboard.find('style') is not None:
            # Dashboard Element Styles
            table_elements = dashboard\
                .findAll('style', recursive=False)[0]\
                .contents[0]\
                .split('<style-rule element=\'')

            list_elements = [i.strip() for i in table_elements if i.strip()]
            element_name = list_elements[0].split('\'')[0]

            element_style = [i.strip() for i in list_elements[0].split('\n')][1:]
            element_style_dict = {}
            for s in element_style:
                s_attrs = s.split(' ')[1:-1]
                tmp_dict = {}
                for item in s_attrs:
                    pairs = re.sub("\'", '', item).split('=')
                    it = iter(pairs)
                    pair_dict = dict(zip(it, it))
                    for k, v in pair_dict.items():
                        tmp_dict[k] = v
                element_style_dict[tmp_dict.get('attr')] = tmp_dict.get('value')

            db[element_name] = element_style_dict

        all_db_styles[dashboard['name']] = db

    return all_db_styles


if __name__ == "__main__":
    parse_tableau_styles()

# # PATHS WE WANT
# #
# # DASHBOARD <workbook><dashboards><dashboard>
# ...<dashboard name=""> # Dashboard Name
# ...<layout-options><title><formatted-text><run # Title stuff
# ...<style><style-rule element=""> # dash-subtitle, dash-container
# ...<style><style-rule element=""><format attr=""> # font-size, background-color, border-style
# ...<size minheight='620' minwidth='1000' />
# #
# # WORKSHEET <workbook><worksheets><worksheet>
# ...<worksheet name=""> # Worksheet Name
# ...<layout-options><title><formatted-text>  # Worksheet Title Formatting
# ...<table><style><style-rule element=""><format attr="">  # Axis, Header, Label, refline, legend
# ...<table><panes><pane><customized-tooltip><formatted-text><run # fontcolor, fontname, fontsize
# ...<table><panes><pane><customized-label><formatted-text><run # fontcolor, fontname, fontsize
