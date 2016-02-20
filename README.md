# Scraper

A friend wanted fetch data from a website and I started this project. What I thought was easy, turned out to be difficult since the site used JavaScript.

## Prerequisites / Assumptions / Fixtures

This script reads from a excel sheet called `cin.xlsx`. This sheet contains about 14699 rows. The first two rows have headers etc.

The second column contains the unique CIN number and the last column contains the email.

Keep this file in the same directory where script is running.

## Requirements

    pip install -r requirements.txt

There is a module which uses dryscape, however it did not really work and I did not investigate further.

If you want to use Phantom JS code, install Node and Phantom JS:

    npm install -g phantomjs-prebuilt

and install the selenium python package:

    pip install selenium-2.52.0

## Code

The scraper, which uses Robobrowser:

    def get_email_by_cin(cin):
        url = 'http://www.mca.gov.in/mcafoportal/viewCompanyMasterData.do'
        browser = RoboBrowser()
        browser.open(url)
        form = browser.get_forms()[-1]
        form['companyID'].value = cin
        browser.submit_form(form)
        table = browser.find('table', attrs={'class': 'result-forms'})
        email_header = table.find('td', text='Email Id')
        email_row = email_header.findNext('td')
        email = str.strip(email_row.text)
        return email.lower()

With Dryscape:

    def get_email_by_cin(cin):
        form_url = ('http://www.mca.gov.in/DCAPortalWeb/dca/MyMCALogin.do?'
                    'method=setDefaultProperty&mode=31')
        sess = dryscrape.Session(base_url='http://www.mca.gov.in')
        sess.visit(form_url)
        xpath_div = "//*[@name='CompanyMasterEditForm']//input[@name='cmpnyID']"
        q = sess.at_xpath(xpath_div)
        q.set(cin)
        q.form().submit()
        return sess.body()

With Selenium + Phantom JS:

    import selenium.webdriver
    from selenium.common.exceptions import NoSuchElementException

    def get_email_by_cin(cin):
        driver = selenium.webdriver.PhantomJS()
        try:
            driver.get('http://www.mca.gov.in/DCAPortalWeb/dca/MyMCALogin.do?method=setDefaultProperty&mode=31')
            driver.find_element_by_id("cin").send_keys(cin)
            driver.find_element_by_xpath('//*[@id="Default"]').click()
            email = driver.find_element_by_xpath('//*[@id="DataBlock1"]/tbody/tr[19]/td[2]').text
            return email.strip().lstrip(':').strip()
        except NoSuchElementException:
            return None

I made use of Robobrowser code with multi processing support from Python. A contrived example on which the code I wrote:

    def job(params):
        # do your job here
        pass

    if __name__ == '__main__':
        for i in range(5):
            p = multiprocessing.Process(target=job, args=(i, ))
            p.start()

check `multiprocessor_example.py` for a complete code.

## Usage

I used multiple machines and ran multiple processes. To scrape data for CIN, 5000 to 10,000:

    python multi-script.py --start=5000 --end=10000
