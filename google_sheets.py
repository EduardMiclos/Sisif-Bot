# ----- IMPORTS -----

import gspread
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from math import floor

# --------------------





# ----- CONSTANTS AND PATHS -----

SHEET_NAME = 'Calendar Examene INFO AC'
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
sheets = [client.open(SHEET_NAME).get_worksheet(0), client.open(SHEET_NAME).get_worksheet(1)]

teste = sheets[0]
sesiune = sheets[1]

# ----------------------





# ----- COLORS -----

COLORS = {
    'EVEN_WEEK': Color(1, 0.9, 0.6),
    'ODD_WEEK': Color(0.96, 0.7, 0.42),
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
    months = ['ianuarie', 'februarie', 'martie', 'aprilie', 'mai', 'iunie', 'iulie', 'august', 'septembrie', 'octombrie', 'noiembrie', 'decembrie']
    return months[month - 1]

def format_date(day, month, hour):
    date_txt = str(day) + ' ' + month_to_text(month)
    if hour != '':
        date_txt += ', ' + str(hour)
    return date_txt

def get_color(text):
    if 'P3' in text:
        return COLORS['P3']
    elif 'P2' in text:
        return COLORS['P2']
    elif 'P1' in text:
        return COLORS['P1']
    elif 'TEST' in text:
        return COLORS['TEST']
    elif 'DISTR' in text:
        return COLORS['CURR_WEEK']
    else:
        return Color(1, 1, 1)

def correct_date(day, month, year, hour='00:00'):
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

def get_school_day():
    return date.today() - SEMESTER_START_DATE

def get_week(dt):
    return floor(dt.days / 7 + 1)

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

    format_cell_range(teste, f'{col_char}{row}:{col_char}{row}', fmt_date)
    format_cell_range(teste, f'{col_char}{row+1}:{col_char}{row+1}', fmt_info)

def update_cell(week, day, date, text):
    row =2*(week + 1)
    col = day + 2

    text = text.upper()
    format_cell(row, col, text)

    teste.update_cell(row, col, date)
    teste.update_cell(row + 1, col, text)

def format_week_cell(week):
    row = 2*(week + 1)
    col_char = 'B'

    clr_val = list(COLORS.values())

    fmt_prev_week = CellFormat(
        backgroundColor=clr_val[(week-1)%2]
    )

    fmt_curr_week = CellFormat(
        backgroundColor=COLORS['CURR_WEEK']
    )

    format_cell_range(teste, f'{col_char}{row- 2}:{col_char}{row}', fmt_prev_week)
    format_cell_range(teste, f'{col_char}{row}:{col_char}{row + 1}', fmt_curr_week)

def exams():
    dt = get_school_day()
    week = get_week(dt) - 15
    row = 2*week + 1

    EXAMS = []

    for rw in range(row, row + 3, 2):
        for col in range(3, 11):
            date = sesiune.cell(rw, col).value
            if date:
                info = sesiune.cell(rw + 1, col).value
                EXAMS.append((date, info))
    return EXAMS

def update_week():
    dt = get_school_day()
    if dt.days % 7 == 0:
        week = get_week(dt)
        format_week_cell(week)
        return 1
    return 0

def write_date(inp):
    (date_in, text) = inp.split('. ')
    (day_in, month_in, year_in) = date_in.split('/')

    if ':' in date_in:
        (year_in, hour_in) = year_in.split(', ')
    else:
        hour_in = ''

    day_in = int(day_in)
    month_in = int(month_in)
    year_in = int(year_in)

    if not (correct_date(day_in, month_in, year_in)):
        return 0

    dt = date(year_in, month_in, day_in)
    delta = dt - SEMESTER_START_DATE
    week_out = get_week(delta)
    day_out = dt.weekday() + 1

    update_cell(week_out, day_out, format_date(day_in, month_in, hour_in), text)
    return 1

# ---------------------
