import dryscrape


def get_email_by_cin_using_xpath(cin):
    # this code never really worked :(
    form_url = ('http://www.mca.gov.in/DCAPortalWeb/dca/MyMCALogin.do?'
                'method=setDefaultProperty&mode=31')
    sess = dryscrape.Session(base_url='http://www.mca.gov.in')
    sess.set_attribute('auto_load_images', False)
    sess.visit(form_url)
    xpath_div = "//*[@name='CompanyMasterEditForm']//input[@name='cmpnyID']"
    q = sess.at_xpath(xpath_div)
    q.set(cin)
    q.form().submit()
    return sess.body()
