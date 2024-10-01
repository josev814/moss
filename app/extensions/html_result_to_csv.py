import os
from bs4 import BeautifulSoup as bs
from csv import DictWriter, QUOTE_NONNUMERIC
import re

PY_FILE_MATCH = re.compile(
    f'([0-9a-z\-\/]+.py)\s\(([0-9]+%)\)$', re.I
)

def get_tr_rows(bs_html: bs) -> str | None:
    data = None
    for row in bs_html.find_all('tr'):
        # the html is badly structured
        # We're only pulling the first tr, because that gets all of the data we need
        data = row.get_text()
        break
    data_arr = []
    if data is not None:
        data_arr = data.split('\n')
        data_arr.pop(0) # removing default header row
    return data_arr

def get_row_links(bs_html: bs) -> list:
    links = []
    for row in bs_html.find_all('tr'):
        # the html is badly structured
        # We're pulling all links, because that gets what we need
        for link_tags in row.find_all('a'):
            link = link_tags.get('href')
            if link not in links:
                links.append(link)
        break
    return links

def convert_to_rows(csv_headers: list, data_arr: list, links: list) -> list:
    csv_rows = []
    while len(data_arr) > 2:
        csv_row = {}
        csv_row[csv_headers[0]] = links.pop(0)
        for i in range(3):
            col_data = data_arr.pop(0)
            matches = PY_FILE_MATCH.findall(col_data)
            if matches:
                f = i+1
                csv_row[f'File {f}'] = matches[0][0]
                csv_row[f'File {f} Percentage'] = matches[0][1]
            else:
                csv_row[csv_headers[-1]] = col_data
        csv_rows.append(
            csv_row
        )
    return csv_rows

def create_csv_file(assignment_dir: os.scandir, csv_file:str, csv_header: list, csv_rows: list) -> None:
    csv_path = os.path.join(assignment_dir.path, csv_file)
    with open(csv_path, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile, fieldnames=csv_header, quotechar='"', quoting=QUOTE_NONNUMERIC)
        writer.writeheader()
        for row in csv_rows:
            writer.writerow(row)



for language_dir in os.scandir('/assignments'):
    if not language_dir.is_dir():
        continue
    for assignment_dir in os.scandir(language_dir.path):
        if not assignment_dir.is_dir():
            continue
        for entry in os.scandir(assignment_dir.path):
            if entry.is_file() and entry.name.endswith('.html'):
                csv_file = f'{entry.name.split(".")[0]}.csv'
                if os.path.exists(os.path.join(assignment_dir.path, csv_file)):
                    continue
                html_data = None
                with open(entry.path, 'r') as htmlfile:
                    html_data = htmlfile.read()
                if html_data is None:
                    continue
                soup = bs(html_data, 'html.parser')
                data_arr = get_tr_rows(soup)
                links = get_row_links(soup)
                if len(data_arr) == 0 or len(links) == 0:
                    continue
                csv_header = [
                    'Comparison Link',
                    'File 1',
                    'File 1 Percentage',
                    'File 2',
                    'File 2 Percentage',
                    'Matched'
                ]
                csv_rows = convert_to_rows(csv_header, data_arr, links)
                create_csv_file(
                    assignment_dir, csv_file,
                    csv_header, csv_rows
                )
