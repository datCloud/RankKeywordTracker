from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import time

keywordsFile = open('C:\\Users\\git267\\Desktop\\keywords.txt', 'r')
getDomain = False
keyWords = []
googleEmail = 'your_email@gmail.com'
googlePwd = 'your_passowrd'

for line in keywordsFile:
    if not getDomain:
        site = line.rstrip()
        getDomain = True
    else:
        keyWords.append(line.rstrip())

serpResultsPerSearch = []

f = open('C:\\Users\\git267\\Desktop\\results.csv', 'w+')

binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options = Options()
options.add_argument('--headless')
options.binary = binary

cap = DesiredCapabilities().FIREFOX
cap["marionette"] = False
#userProfile = webdriver.FirefoxProfile('%USERPROFILE%\\AppData\\Local\\Mozilla\\Firefox\\Profiles\\nn8i4u4j.CustomUser')
userProfile = webdriver.FirefoxProfile('C:\\Users\\git267\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\yypjbsha.CloudProfile\\')
#driver = webdriver.Firefox(userProfile, capabilities=cap, executable_path="%USERPROFILE%\\AppData\\Local\\Geckodriver\\geckodriver.exe")
driver = webdriver.Firefox(options=options)
driver.set_window_position(0, 0)
driver.set_window_size(800, 600)

def GetWidth(pageUrl):
    if pageUrl is not None:
        driver.get(pageUrl)
    searchInput = driver.find_element_by_xpath('//input[@title="Pesquisar"]')
    ActionChains(driver).move_to_element(searchInput).click(searchInput).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).key_up(Keys.BACKSPACE).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).key_up(Keys.BACKSPACE).perform()
    if(len(keyWords) > 0):
        for keyWordLetter in keyWords[0]:
            searchInput.send_keys(keyWordLetter)
        searchInput.send_keys(u'\ue007')
        results = driver.find_elements_by_css_selector('.rc .r > a')
        foundInSERP = False
        for result in results:
            serpResultsPerSearch.append(result.get_attribute('href'))
        for index, item in enumerate(serpResultsPerSearch):
            if site in item:
                print(keyWords[0] + ' isn\'t at the poistion number ' + str(index + 1) + ' on SERP')
                f.write(keyWords[0] + ',' + item.rsplit('/', 1)[0] + ',/' + item.rsplit('/', 1)[1] + ',' + str(index + 1) + '\n')
                foundInSERP = True
                break
        if not foundInSERP:
            print(keyWords[0] + ' is at the top 100 on SERP')
            f.write(keyWords[0] + ',,,101\n')
        keyWords.pop(0)
        serpResultsPerSearch.clear()
        GetWidth(None)
    else:
        f.close()
        driver.quit()
        print('Finished!')
        

def LoginGoogleAccount(email, pwd):
    print('Performing Login...')
    driver.get('https://www.google.com/accounts/ServiceLoginAuth')
    emailInput = driver.find_element_by_xpath('//input[@aria-label="E-mail ou telefone"]')
    emailButton = driver.find_element_by_id('identifierNext')
    ActionChains(driver).move_to_element(emailInput).click(emailInput).send_keys(email).move_to_element(emailButton).click(emailButton).perform()
    time.sleep(3)
    pwdInput = driver.find_element_by_xpath('//input[@aria-label="Digite sua senha"]')
    pwdButton = driver.find_element_by_id('passwordNext')
    ActionChains(driver).move_to_element(pwdInput).click(pwdInput).send_keys(pwd).move_to_element(pwdButton).click(pwdButton).perform()
    time.sleep(3)
    print('Successful Login')

LoginGoogleAccount(googleEmail, googlePwd)
GetWidth('https://www.google.com.br/search?q=google')
