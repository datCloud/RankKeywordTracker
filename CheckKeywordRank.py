from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import StaleElementReferenceException
# from selenium.webdriver.firefox.options import Options
import time, os, inspect

startTime = time.time()
timeByKeyword = []

# keywordsFile = open('C:\\Users\\git267\\Desktop\\keywords.txt', 'r')
currentDirectory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
keywordsFile = open(os.path.join(currentDirectory, 'keywords.txt'), 'r')
getDomain = False
keyWords = []
googleEmail = 'your_email@domail.com'
googlePwd = 'your_pwd'

for line in keywordsFile:
    if not getDomain:
        site = line.rstrip()
        getDomain = True
    else:
        keyWords.append(line.rstrip())

serpResultsPerSearch = []

# f = open('C:\\Users\\git267\\Desktop\\results.csv', 'w+')
f = open(os.path.join(currentDirectory, 'results.csv'), 'w+')

# binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'
# options = Options()
# options.add_argument('--headless')
# options.binary = binary

# cap = DesiredCapabilities().FIREFOX
# cap["marionette"] = False
#userProfile = webdriver.FirefoxProfile('%USERPROFILE%\\AppData\\Local\\Mozilla\\Firefox\\Profiles\\nn8i4u4j.CustomUser')
# userProfile = webdriver.FirefoxProfile('C:\\Users\\git267\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\yypjbsha.CloudProfile\\')
#driver = webdriver.Firefox(userProfile, capabilities=cap, executable_path="%USERPROFILE%\\AppData\\Local\\Geckodriver\\geckodriver.exe")
# driver = webdriver.Firefox(options=options)
driver = webdriver.Firefox()
# driver.manage().timeouts().pageLoadTimeout(10, TimeUnit.SECONDS);
driver.set_page_load_timeout(10)
driver.set_window_position(0, 0)
driver.set_window_size(800, 600)

def GetSerpPosition(pageUrl):
    keyWordIndex = []
    if pageUrl is not None:
        driver.get(pageUrl)
    time.sleep(3)
    startKeywordTime = time.time()
    searchInput = driver.find_element_by_xpath('//input[@class="gLFyf gsfi"]')
    ActionChains(driver).move_to_element(searchInput).click(searchInput).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).key_up(Keys.BACKSPACE).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).key_up(Keys.BACKSPACE).perform()
    if(len(keyWords) > 0):
        for keyWordLetter in keyWords[0]:
            searchInput.send_keys(keyWordLetter)
        # searchInput.send_keys(u'\ue007')
        searchInput.send_keys(Keys.RETURN)
        time.sleep(2)
        results = driver.find_elements_by_css_selector('.rc .r > a')
        foundInSERP = False
        for result in results:
            serpResultsPerSearch.append(result.get_attribute('href'))
        for index, item in enumerate(serpResultsPerSearch):
            if site in item:
                # serpList.append(index + 1)
                print(keyWords[0] + ' is at the poistion number ' + str(index + 1) + ' on SERP')
                f.write(keyWords[0] + ',' + item.rsplit('/', 1)[0] + ',/' + item.rsplit('/', 1)[1] + ',' + str(index + 1) + '\n')
                foundInSERP = True
                break
        if not foundInSERP:
            print(keyWords[0] + ' isn\'t at the top 100 on SERP')
            f.write(keyWords[0] + ',,,101\n')
        timeByKeyword.append(keyWords[0])
        timeByKeyword.append(startKeywordTime)
        keyWords.pop(0)
        serpResultsPerSearch.clear()
        driver.switch_to_default_content()
        GetSerpPosition(None)
    else:
        f.close()
        driver.quit()
        firstPageCounter = sum(map(lambda x : x <= 10, keyWordIndex))
        print('Keywords on the first page: ' + firstPageCounter)

        print('Finished!')
        # minTime = min(timeByKeyword)
        # maxTime = max(timeByKeyword)
        # print('Time taken in seconds: %s' % (time.time() - startTime))
        # print('Fastest keyword check: %s' % (timeByKeyword[timeByKeyword.index(min(timeByKeyword)) - 1]))
        # print(min(timeByKeyword))
        # print('Longest keyword check: %s' % (timeByKeyword[timeByKeyword.index(max(timeByKeyword)) - 1]))
        # print(max(timeByKeyword))

        

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

# Access site and get mpis TO DO
LoginGoogleAccount(googleEmail, googlePwd)
GetSerpPosition('https://www.google.com.br/search?q=google')
