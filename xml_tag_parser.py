from bs4 import BeautifulSoup
import re
import lxml
import pprint

infile = open('tableau_style_tags.xml', 'r')
contents = infile.read()
# # Replace tags with hyphens with underscores before parsing
# content = re.sub('<(.*?)>', lambda x: x.group(0).replace('style-rule', 'body'), contents)
soup = BeautifulSoup(contents, 'lxml')   # Optionally use 'lxml' here

#
# FORMAT CONTAINER 1: WORKSHEETS
#
worksheets = soup.find_all('worksheet')

ws = {}
for worksheet in worksheets:
    #
    # WORKSHEETS - Title Formatting
    #
    ws['name'] = worksheet['name']

    ws['title'] = None
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
        ws['title'] = title[0]
        ws['title_font_attributes'] = list(filter(None, title_font_attributes))

    #
    # WORKSHEETS - Table Styles
    #
    ws['table_styles'] = None
    if worksheet.find('table') is not None:
        table_styles = worksheet\
            .find('table')\
            .findAll('style', recursive=False)
        ws['table_styles'] = table_styles
        ws['table_styles'] = table_styles
        # Incomplete parsing here... tricky

    #
    # WORKSHEETS - Pane Styles (Custom Tooltips)
    #
    if worksheet.find('table') is not None:
        pane_styles = worksheet\
            .find('table')\
            .find('panes')\
            .find('pane')\
            .find('customized-tooltip')\
            .find('formatted-text')\
            .findAll('run', recursive=False)

        pane_style_attributes = []
        for ps in pane_styles:
            pane_style_attributes.append({k: v for k, v in ps.attrs.items()})

        ws['pane_style_attributes'] = list(filter(None, pane_style_attributes))

    pprint.pprint(ws)
    print('\n\n')





# # PATHS WE WANT
# #
# # WORKSHEET <workbook><worksheets><worksheet>
# ...<worksheet name=""> # Worksheet Name
# ...<layout-options><title><formatted-text>  # Worksheet Title Formatting
# ...<table><style>
# ...<table><style><style-rule element=""><format attr="">  # Axis, Header, Label, refline, legend
# ...<table><panes>
# ...<table><panes><pane><customized-tooltip><formatted-text><run # fontcolor, fontname, fontsize
#
# # DASHBOARD <workbook><dashboards><dashboard>
# ...<dashboard name=""> # Dashboard Name
# ...<layout-options><title><formatted-text><run # Title stuff
# ...<style><style-rule element=""> # dash-subtitle, dash-container
# ...<style><style-rule element=""><format attr=""> # font-size, background-color, border-style
# ...<size minheight='620' minwidth='1000' />
