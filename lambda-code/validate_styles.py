from textwrap import dedent
from tableau_xml_parser import get_tableau_styles
from helpers import Alerts, err_msg, one_to_many_dict


def validate_styles(style_guide_json, workbook_file):
    #
    # Parse styles from Tableau Workbook file
    #
    styles = get_tableau_styles(workbook_file)

    # Workbook styles
    wb_styles = styles.get('workbook_styles')
    test_workbook(wb_styles, style_guide_json)

    # Dashboard styles
    db_styles = styles.get('dashboard_styles')
    test_dashboards(db_styles, style_guide_json)

    # Worksheet styles
    ws_styles = styles.get('worksheet_styles')
    test_worksheets(ws_styles, style_guide_json)

    return


def test_workbook(workbook_styles, sg):
    # print('Workbook Styles at time of testing:\n', pp(workbook_styles))
    print(dedent('''
    
        Validating all top-level WORKBOOK styles...
        '''))

    valid_wb_styles_list = []
    wb_err_count = 0

    for item in workbook_styles:
        styles = workbook_styles.get(item)
        print('STYLES', styles)
        for style in styles:
            s = styles.get(style)
            if s is not None:
                if 'font-size' in style:
                    if s not in sg.get('font-sizes'):
                        print(f'{Alerts.INVALID_FONT_SIZE} {str(s + "pt"):20s} found in {str(item + ".")}')
                        wb_err_count += 1
                    else:
                        print(f'{Alerts.VALID_FONT_SIZE} {str(s + "pt"):20s} found in {str(item + ".")}')
                        valid_wb_styles_list.append({'font-size': str(s + "pt")})

                if 'font-family' in style:
                    if s not in sg.get('fonts'):
                        print(f'{Alerts.INVALID_FONT_TYPE} {str(s):20s} found in {str(item + ".")}')
                        wb_err_count += 1
                    else:
                        print(f'{Alerts.VALID_FONT_TYPE} {str(s):20s} found in {str(item + ".")}')
                        valid_wb_styles_list.append({'font-type': str(s)})

                if 'color' in style:
                    if s.upper() not in sg.get('font-colors'):
                        print(f'{Alerts.INVALID_FONT_COLOR} {str(s.upper()):20s} found in {str(item + ".")}')
                        wb_err_count += 1
                    else:
                        print(f'{Alerts.VALID_FONT_COLOR} {str(s.upper()):20s} found in {str(item + ".")}')
                        valid_wb_styles_list.append({'font-color': str(s.upper())})

    err_msg(wb_err_count)

    return print(one_to_many_dict(valid_wb_styles_list))


def test_dashboards(dashboard_styles, sg):
    # print('Dashboard Styles at time of testing:\n', pp(dashboard_styles))
    print(dedent('''

    Validating each DASHBOARD in workbook...
    '''))

    valid_db_styles_list = []
    db_err_count = 0
    for dashboard in dashboard_styles:
        dashboard_style = dashboard_styles.get(dashboard)
        db_name = dashboard_style.get('db_name')
        for item in dashboard_style:
            styles = dashboard_style.get(item)
            print('STYLES', styles)
            if isinstance(styles, dict):
                for style in styles:
                    s = styles.get(style)
                    if s is not None:
                        if 'font-size' in style:
                            if s not in sg.get('font-sizes'):
                                print(f'{Alerts.INVALID_FONT_SIZE} {str(s + "pt"):20s} found in {str(item):20s} of dashboard {str(db_name)}.')
                                db_err_count += 1
                            else:
                                print(f'{Alerts.VALID_FONT_SIZE} {str(s + "pt"):20s} found in {str(item + ".")}')
                                valid_db_styles_list.append({'font-size': str(s + "pt")})

                        if 'font-family' in style:
                            if s not in sg.get('fonts'):
                                print(f'{Alerts.INVALID_FONT_TYPE} {str(s):20s} found in {str(item):20s} of dashboard {str(db_name)}.')
                                db_err_count += 1
                            else:
                                print(f'{Alerts.VALID_FONT_TYPE} {str(s):20s} found in {str(item + ".")}')
                                valid_db_styles_list.append({'font-type': str(s)})

                        # This excludes dashboard zone styles (background color, border colors) to only get font color.
                        if 'db_zone_styles' not in item:
                            if 'color' in style:
                                if s.upper() not in sg.get('font-colors'):
                                    print(f'{Alerts.INVALID_FONT_COLOR} {str(s.upper()):20s} found in {str(item):20s} of dashboard {str(db_name)}.')
                                    db_err_count += 1
                                else:
                                    print(f'{Alerts.VALID_FONT_COLOR} {str(s.upper()):20s} found in {str(item + ".")}')
                                    valid_db_styles_list.append({'font-color': str(s.upper())})

                        # Dashboard Zone styles
                        else:
                            # Convert any singular string items to list before validating as lists
                            if isinstance(s, str):
                                s = list(s)
                            for val in s:
                                if 'border-color' in style:
                                    if val.upper() not in sg.get('border-colors'):
                                        print(
                                            f'{Alerts.INVALID_BORDER_COLOR} {str(val.upper()):20s} found in {str(item):20s} of dashboard {str(db_name)}.')
                                        db_err_count += 1
                                    else:
                                        print(f'{Alerts.VALID_BORDER_COLOR} {str(val.upper()):20s} found in {str(item + ".")}')
                                        valid_db_styles_list.append({'border-color': str(val.upper())})
    
                                if 'border-width' in style:
                                    if val not in sg.get('border-width'):
                                        print(
                                            f'{Alerts.INVALID_BORDER_WIDTH} {str(val):20s} found in {str(item):20s} of dashboard {str(db_name)}.')
                                        db_err_count += 1
                                    else:
                                        print(f'{Alerts.VALID_BORDER_WIDTH} {str(val):20s} found in {str(item + ".")}')
                                        valid_db_styles_list.append({'border-width': str(val)})
    
                                if 'border-style' in style:
                                    if val not in sg.get('border-style'):
                                        print(
                                            f'{Alerts.INVALID_BORDER_STYLE} {str(val):20s} found in {str(item):20s} of dashboard {str(db_name)}.')
                                        db_err_count += 1
                                    else:
                                        print(f'{Alerts.VALID_BORDER_STYLE} {str(val):20s} found in {str(item + ".")}')
                                        valid_db_styles_list.append({'border-style': str(val)})
    
                                if 'margin' in style:
                                    if val not in sg.get('margin'):
                                        print(
                                            f'{Alerts.INVALID_MARGIN} {str(val):20s} found in {str(item):20s} of dashboard {str(db_name)}.')
                                        db_err_count += 1
                                    else:
                                        print(f'{Alerts.VALID_MARGIN} {str(val):20s} found in {str(item + ".")}')
                                        valid_db_styles_list.append({'margin': str(val)})
    
                                if 'margin-top' in style:
                                    if val not in sg.get('margin-top'):
                                        print(
                                            f'{Alerts.INVALID_MARGIN_TOP} {str(val):20s} found in {str(item):20s} of dashboard {str(db_name)}.')
                                        db_err_count += 1
                                    else:
                                        print(f'{Alerts.VALID_MARGIN_TOP} {str(val):20s} found in {str(item + ".")}')
                                        valid_db_styles_list.append({'margin-top': str(val)})
    
                                if 'margin-bottom' in style:
                                    if val not in sg.get('margin-bottom'):
                                        print(
                                            f'{Alerts.INVALID_MARGIN_BOTTOM} {str(val):20s} found in {str(item):20s} of dashboard {str(db_name)}.')
                                        db_err_count += 1
                                    else:
                                        print(f'{Alerts.VALID_MARGIN_BOTTOM} {str(val):20s} found in {str(item + ".")}')
                                        valid_db_styles_list.append({'margin-bottom': str(val)})
    
                                if 'background-color' in style:
                                    if val.upper() not in sg.get('background-colors'):
                                        print(
                                            f'{Alerts.INVALID_BACKGROUND_COLOR} {str(val.upper()):20s} found in {str(item):20s} of dashboard {str(db_name)}.')
                                        db_err_count += 1
                                    else:
                                        print(f'{Alerts.VALID_BACKGROUND_COLOR} {str(val.upper()):20s} found in {str(item + ".")}')
                                        valid_db_styles_list.append({'background-color': str(val.upper())})
    
                                if 'padding' in style:
                                    if val not in sg.get('padding'):
                                        print(
                                            f'{Alerts.INVALID_PADDING} {str(val):20s} found in {str(item):20s} of dashboard {str(db_name)}.')
                                        db_err_count += 1
                                    else:
                                        print(f'{Alerts.VALID_PADDING} {str(val):20s} found in {str(item + ".")}')
                                        valid_db_styles_list.append({'padding': str(val)})

    err_msg(db_err_count)
    return print(one_to_many_dict(valid_db_styles_list))


def test_worksheets(worksheet_styles, sg):
    # print('Worksheet Styles at time of testing:\n', pp(worksheet_styles))
    print(dedent('''

    Validating each WORKSHEET in workbook...
    '''))

    valid_ws_styles_list = []
    ws_err_count = 0
    for worksheet_style in worksheet_styles:
        worksheet = worksheet_styles.get(worksheet_style)
        ws_name = worksheet_style
        for item in worksheet:
            styles = worksheet.get(item)
            for style_dict in styles:
                if isinstance(style_dict, dict):
                    for style in style_dict:
                        s = style_dict.get(style)
                        if s is not None:
                            if 'fontsize' in style:
                                if s not in sg.get('font-sizes'):
                                    print(f'{Alerts.INVALID_FONT_SIZE} {str(s + "pt"):20s} found in {str(item):20s} of worksheet {str(ws_name)}.')
                                    ws_err_count += 1
                                else:
                                    print(f'{Alerts.VALID_FONT_SIZE} {str(s + "pt"):20s} found in {str(item + ".")}')
                                    valid_ws_styles_list.append({'font-size': str(s + "pt")})

                            if 'fontname' in style:
                                if s not in sg.get('fonts'):
                                    print(f'{Alerts.INVALID_FONT_TYPE} {str(s):20s} found in {str(item):20s} of worksheet {str(ws_name)}.')
                                    ws_err_count += 1
                                else:
                                    print(f'{Alerts.VALID_FONT_TYPE} {str(s):20s} found in {str(item + ".")}')
                                    valid_ws_styles_list.append({'font-type': str(s)})

                            if 'fontcolor' in style:
                                if s.upper() not in sg.get('font-colors'):
                                    print(f'{Alerts.INVALID_FONT_COLOR} {str(s.upper()):20s} found in {str(item):20s} of worksheet {str(ws_name)}.')
                                    ws_err_count += 1
                                else:
                                    print(f'{Alerts.VALID_FONT_COLOR} {str(s.upper()):20s} found in {str(item + ".")}')
                                    valid_ws_styles_list.append({'font-color': str(s.upper())})

    err_msg(ws_err_count)

    return print(one_to_many_dict(valid_ws_styles_list))


if __name__ == "__main__":
    validate_styles()
