from bs4 import BeautifulSoup


infile = open('tableau_style_tags.xml', 'r')
contents = infile.read()
soup = BeautifulSoup(contents, 'xml') # Optionally use 'lxml' here
# print(soup.prettify())

#
# FORMAT CONTAINER 1: WORKSHEETS
#
worksheets = soup.find_all('worksheet')
for worksheet in worksheets:
    print(worksheet['name'])
    print(worksheet.prettify(), '\n\n')


# #
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
