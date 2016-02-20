import time
import random

import requests
from robobrowser import RoboBrowser
from openpyxl import load_workbook

user_agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
               'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.9.2a1pre) Gecko',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
               'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; sv-SE) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
               'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0']


def get_email_by_cin(cin):
    url = 'http://www.mca.gov.in/mcafoportal/viewCompanyMasterData.do'
    browser = RoboBrowser()
    browser.session.headers['User-Agent'] = random.choice(user_agents)
    browser.open(url)
    form = browser.get_forms()[-1]
    form['companyID'].value = cin
    browser.submit_form(form)
    table = browser.find('table', attrs={'class': 'result-forms'})
    if not table:
        return None
    email_header = table.find('td', text='Email Id')
    if not email_header:
        return None
    email_row = email_header.findNext('td')
    email = str.strip(email_row.text)
    return email.lower()


def job():
    workbook = load_workbook('cin.xlsx')
    worksheet = workbook.active

    count = 0
    for row in worksheet.rows[1650:]:
        cin = row[1].value
        cin = str.strip(cin)
        try:
            email = get_email_by_cin(cin=cin)
        except requests.exceptions.ConnectionError:
            print('Too many requests, sleeping at CIN: {}'.format(cin))
            time.sleep(60)
            email = get_email_by_cin(cin=cin)
        if not email:
            print('Invalid CIN: {}'.format(cin))
            email = ''
        print('CIN: {}, email: {}'.format(cin, email))
        row[-1].value = email
        time.sleep(2)

        count = count + 1
        if count % 25 == 0:
            workbook.save('results.xlsx')
            time.sleep(5)

    workbook.save('results.xlsx')

if __name__ == '__main__':
    job()
