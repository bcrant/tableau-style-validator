from bs4 import BeautifulSoup
import lxml
import pprint

infile = open('tableau_style_tags.xml', 'r')
contents = infile.read()
soup = BeautifulSoup(contents, 'lxml')   # Optionally use 'lxml' here
# print(soup.prettify())

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

    pprint.pprint(ws)
    print('\n\n')

    # print(worksheet.findChildren('layout-options'))
    # print(type(worksheet.findChildren('layout-options')))

    # print(worksheet.find('layout-options').next_siblings)
    # .find('title').find('formatted-text'))

    # print(worksheet.find_all(.prettify(), '\n\n')
    # print(layout-options><title><formatted-text>)


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
