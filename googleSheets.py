# ----- IMPORTS -----

import gspread
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from math import floor

# --------------------





# ----- CONSTANTS AND PATHS -----

SHEET_NAME = 'Calendar'
JSON_PATH = 'credentials.json'
FEEDS_PATH = "https://spreadsheets.google.com/feeds"
SPREADSHEET_PATH = "https://www.googleapis.com/auth/spreadsheets"
DRIVE_FILE_PATH = "https://www.googleapis.com/auth/drive.file"
DRIVE_PATH = "https://www.googleapis.com/auth/drive"

SEMESTER_START_DATE = date(2021, 2, 15)

# -------------------------------





# ----- CREDENTIALS -----

scope = [FEEDS_PATH, SPREADSHEET_PATH, DRIVE_FILE_PATH, DRIVE_PATH]
creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_PATH, scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

data = sheet.get_all_values()

# ----------------------





# ----- COLORS -----

COLORS = {
    'DATE_INFO': Color(1, 0.9, 0.6),
    'P3': Color(1, 0.95, 0.80),
    'P2': Color(0.92, 0.60, 0.60),
    'P1': Color(0.64, 0.99, 0.93),
    'TEST': Color(0.84, 0.65, 0.74),
    'CURR_WEEK': Color(0.71, 0.65, 0.84),
    'DISTR': Color(0.43, 0.62, 0.92)
}

# ------------------





# ----- SECONDARY FUNCTIONS -----

def month_to_text(month):
    if month == 1:
        return 'ianuarie'
    elif month == 2:
        return 'februarie'
    elif month == 3:
        return 'martie'
    elif month == 4:
        return 'aprilie'
    elif month == 5:
        return 'mai'
    elif month == 6:
        return 'iunie'
    elif month == 7:
        return 'iulie'
    elif month == 8:
        return 'august'
    elif month == 9:
        return 'septembrie'
    elif month == 10:
        return 'octombrie'
    elif month == 11:
        return 'noiembrie'
    else:
        return 'decembrie'

def format_date(day, month, hour):
    return str(day) + ' ' + month_to_text(month) + ', ' + str(hour)

def get_color(text):
    if 'P3' in text:
        return COLORS['P3']
    elif 'P2' in text:
        return COLORS['P2']
    elif 'P1' in text:
        return COLORS['P1']
    elif 'TEST' in text:
        return COLORS['TEST']
    elif 'UPDATEWEEK' in text:
        return COLORS['CURR_WEEK']
    elif 'DISTR' in text:
        return COLORS['CURR_WEEK']
    else:
        return Color(1, 1, 1)

def correct_date(day, month, year, hour):
    errs = []
    h = int(hour.split(':')[0])
    m = int(hour.split(':')[1])

    errs.append(year != date.today().year)
    errs.append(month <= 0 or month > 12 or not isinstance(month, int))
    errs.append(day <= 0 or day > 31 or not isinstance(day, int))
    errs.append(h < 0 or h >= 24 or m < 0 or m >= 60)

    if sum(errs):
        return 0

    if ((not (month % 2) and month <= 5) or (month % 2 and month >= 8)) and day == 31:
        return 0

    if month == 2 and day > 28:
        return 0

    return 1

# -------------------------------





# ----- MAIN -----

def format_cell(row, col, text):
    fmt_date = CellFormat(
        backgroundColor=  COLORS['DATE_INFO']
    )

    fmt_info = CellFormat(
        backgroundColor= get_color(text)
    )

    col_char = chr(col + 64)

    format_cell_range(sheet, f'{col_char}{row}:{col_char}{row}', fmt_date)
    format_cell_range(sheet, f'{col_char}{row+1}:{col_char}{row+1}', fmt_info)

def update_cell(week, day, date, text):
    row =2*(week + 1)
    col = day + 2

    text = text.upper()
    format_cell(row, col, text)

    sheet.update_cell(row, col, date)
    sheet.update_cell(row + 1, col, text)

def write_date(inp):
    (date_in, text) = inp.split('. ')
    (day_in, month_in, year_in) = date_in.split('/')
    (year_in, hour_in) = year_in.split(', ')

    day_in = int(day_in)
    month_in = int(month_in)
    year_in = int(year_in)

    if not (correct_date(day_in, month_in, year_in, hour_in)):
        return 0

    dt = date(year_in, month_in, day_in)
    delta = dt - SEMESTER_START_DATE
    week_out = floor(delta.days/7 + 1)
    day_out = dt.weekday() + 1

    update_cell(week_out, day_out, format_date(day_in, month_in, hour_in), text)
    return 1

# ---------------------
