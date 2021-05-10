from bs4 import BeautifulSoup
import pprint


def parse_tableau_styles():
    infile = open('tableau_style_tags.xml', 'r')
    contents = infile.read()
    soup = BeautifulSoup(contents, 'lxml')

    style_dict = {
        **parse_worksheets(soup)
    }

    return pprint.pprint(style_dict)


def parse_worksheets(xml_soup):

    worksheets = xml_soup.find_all('worksheet')

    all_ws_styles = {}

    for worksheet in worksheets:
        #
        # WORKSHEET TITLE STYLES
        #
        ws = {}
        if worksheet.find('layout-options') is not None:
            runs = worksheet\
                .find('layout-options')\
                .find('title')\
                .find('formatted-text')\
                .findAll('run', recursive=False)

            title = []
            title_font_attributes = []
            for run in runs:
                title.append(run.text)
                title_font_attributes.append({k: v for k, v in run.attrs.items()})
            ws['ws_title'] = title[0]
            ws['ws_title_font_attributes'] = list(filter(None, title_font_attributes))

        #
        # WORKSHEET TABLE AND PANE STYLES
        #
        if worksheet.find('table') is not None:
            # Table Styles
            table_elements = worksheet\
                .find('table')\
                .findAll('style', recursive=False)[0]\
                .contents[0]\
                .split('<style-rule element=\'')

            element_styles = {}
            for element in table_elements:
                for fmt in element.split('\n'):
                    element_fmt = [
                        fmt.strip()
                        for fmt in element.split('\n')
                    ]

                    element_styles[element_fmt[0].split('\'')[0]] = list(filter(None, element_fmt[1:]))

            # Pane Styles - Customized Tooltips
            pane_tooltip_styles = worksheet\
                .find('table')\
                .find('panes')\
                .find('pane')\
                .find('customized-tooltip')

            if pane_tooltip_styles is not None:
                ws['ws_pane_tooltip_attributes'] = get_pane_styles_from_dict(pane_tooltip_styles)

            # Pane Styles - Customized Labels
            pane_label_styles = worksheet\
                .find('table')\
                .find('panes')\
                .find('pane')\
                .find('customized-label')

            if pane_label_styles is not None:
                ws['ws_pane_label_attributes'] = get_pane_styles_from_dict(pane_label_styles)

        all_ws_styles[worksheet['name']] = ws

    return all_ws_styles


def get_pane_styles_from_dict(pane_styles_soup):
    # Get formatted text styles from customized label or tooltip
    pane_styles_fmt = pane_styles_soup\
        .find('formatted-text')\
        .findAll('run', recursive=False)

    pane_style_attribute_list = []
    for pane_style in pane_styles_fmt:
        pane_style_attribute_list.append({k: v for k, v in pane_style.attrs.items()})

    return list(filter(None, pane_style_attribute_list))


if __name__ == "__main__":
    parse_tableau_styles()

# # PATHS WE WANT
# #
# # WORKSHEET <workbook><worksheets><worksheet>
# ...<worksheet name=""> # Worksheet Name
# ...<layout-options><title><formatted-text>  # Worksheet Title Formatting
# ...<table><style><style-rule element=""><format attr="">  # Axis, Header, Label, refline, legend
# ...<table><panes><pane><customized-tooltip><formatted-text><run # fontcolor, fontname, fontsize
# ...<table><panes><pane><customized-label><formatted-text><run # fontcolor, fontname, fontsize
#
# # DASHBOARD <workbook><dashboards><dashboard>
# ...<dashboard name=""> # Dashboard Name
# ...<layout-options><title><formatted-text><run # Title stuff
# ...<style><style-rule element=""> # dash-subtitle, dash-container
# ...<style><style-rule element=""><format attr=""> # font-size, background-color, border-style
# ...<size minheight='620' minwidth='1000' />
