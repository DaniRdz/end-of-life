#!/usr/bin/python3
from requests_html import HTMLSession
from datetime import datetime
import requests
import csv

eol_products = ['apache',
                'tomcat',
                'docker-engine',
                'elasticsearch',
                'gitlab',
                'grafana',
                'jenkins',
                'mssqlserver',
                'mongodb',
                'mysql',
                'nginx',
                'openssl',
                'oracle-database',
                'php',
                'postgresql',
                'python',
                'sonar']

eol_urls = ['https://www.ibm.com/support/pages/lifecycle/search/?q=cognos%20analytics',
            'https://www.ibm.com/support/pages/lifecycle/search?q=IBM%20InfoSphere%20Information%20Server', 
            'https://www.ibm.com/support/pages/lifecycle/search/?q=rational%20clearquest']

eol_info = []

def format_date(date):
    return f"({datetime.strptime(date, '%Y-%m-%d').strftime('%d %b %Y')})"

def format_time_difference(diff):
    days = abs(diff.days)
    years = days // 365
    months = (days % 365) // 30
    weeks = (days % 365 % 30) // 7
    remaining_days = (days % 365 % 30) % 7

    years_s = f"{years} year{'s' if years != 1 else ''}"
    months_s = f"{months} month{'s' if months != 1 else ''}"
    weeks_s = f"{weeks} week{'s' if weeks != 1 else ''}"
    days_s = f"{remaining_days} day{'s' if remaining_days != 1 else ''}"

    string_parts = []

    if years > 0:
        string_parts.append(years_s)
    if months > 0:
        string_parts.append(months_s)
    if weeks > 0:
        string_parts.append(weeks_s)
    if remaining_days > 0:
        string_parts.append(days_s)

    time_str = ", ".join(string_parts)

    if diff.days == -1:
        days_count = "Ends Tomorrow"
    elif diff.days < 0:
        days_count = f"Ends in {time_str}"
    elif diff.days == 0:
        days_count = "Ends Today"
    elif diff.days == 1:
        days_count = "Ended Yesterday"
    else:
        days_count = f"Ended {time_str} ago"
    
    return days_count

def append_eol_info(mw_name, version, released, date_count, latest_version,latest_version_released, eol):
    eol_info.append({
           'mw': mw_name,
           'version': version,
           'released': released,
           'end_of_life': 'false' if eol == False or eol == '' else f'{date_count} {format_date(eol)}',
           'latest_version': f'{latest_version} {latest_version_released}'
       })


def get_eol_info(eol_product):
    response = requests.get(
    f'https://endoflife.date/api/{eol_product}.json')
    cycles = response.json()
    mw_name = eol_product
    today = datetime.now()
    date_count = ''
    
    for cycle in cycles:
        version = cycle['cycle']
        released = format_date(cycle['releaseDate'])
        eol = cycle['eol']
        latest_version = cycle['latest'] if 'latest' in cycle else ''
        latest_version_released = format_date(cycle['latestReleaseDate']) if 'latestReleaseDate' in cycle else ''

        if eol != False:
            diff_days_eol = (today - datetime.strptime( cycle['eol'], '%Y-%m-%d'))
            date_count = format_time_difference(diff_days_eol)
        
        append_eol_info(mw_name, version, released, date_count, latest_version, latest_version_released, eol)

def get_eol_url_info(eol_url):
    session = HTMLSession()
    page = session.get(eol_url)
    page.html.render()
    trs = page.html.find('tr')
    today = datetime.now()
    date_count = ''

    for tr in trs:
        tds = tr.find('td')
        if len(tds) > 0:
            mw_name = tds[1].text
            version = tds[2].text
            released = format_date(tds[5].text)
            eol = tds[6].text

            latest_version = ''
            latest_version_released = ''

            if eol != '':
                diff_days_eol = (today - datetime.strptime(eol, '%Y-%m-%d'))
                date_count = format_time_difference(diff_days_eol)
            append_eol_info(mw_name, version, released, date_count, latest_version,latest_version_released, eol)

    
for eol_product in eol_products:
    get_eol_info(eol_product)

#for eol_url in eol_urls:
#    get_eol_url_info(eol_url)

keys = eol_info[0].keys()

with open('end_of_life.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(eol_info)