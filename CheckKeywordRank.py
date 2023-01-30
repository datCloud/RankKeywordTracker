from selenium import webdriver
import time, os, inspect
from datetime import datetime
import base64
from getpass import getpass
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager


chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

startTime = time.time()
timeByKeyword = []

currentDirectory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
keywordsFile = open(os.path.join(currentDirectory, 'keywords.txt'), 'r', encoding='utf-8')
getDomain = False
keyWords = []

for line in keywordsFile:
    if not getDomain:
        site = line.rstrip()
        getDomain = True
    else:
        keyWords.append(line.rstrip())

serpResultsPerSearch = []

folderName = 'results'
if not os.path.exists(folderName):
    os.makedirs(folderName)

currentDateWithTimestamp = datetime.now()

f = open(os.path.join(currentDirectory, folderName, f'{currentDateWithTimestamp.strftime("%Y%m%d_%H%M%S")}_{site}.csv'), 'w+', encoding='utf-8')

# driver = webdriver.Firefox()
driver.set_page_load_timeout(10)
driver.set_window_position(0, 0)
driver.maximize_window()

def GetSerpPosition(pageUrl):
    keyWordIndex = []
    if pageUrl is not None:
        driver.get(pageUrl)
    time.sleep(3)
    startKeywordTime = time.time()
    searchInput = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.gLFyf')))
    ActionChains(driver).move_to_element(searchInput).click(searchInput).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).key_up(Keys.BACKSPACE).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).key_up(Keys.BACKSPACE).perform()
    if(len(keyWords) > 0):
        for keyWordCharacter in keyWords[0]:
            searchInput.send_keys(keyWordCharacter)
        searchInput.send_keys(Keys.RETURN)
        time.sleep(2)
        results = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.g [data-header-feature] > div > a')))
        foundInSERP = False
        for result in results:
            serpResultsPerSearch.append(result.get_attribute('href'))
        for index, item in enumerate(serpResultsPerSearch):
            if site in item:
                keyWordIndex.append(index + 1)
                print(f'{keyWords[0]} is at the position #{str(index + 1)} on SERP')
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
        driver.switch_to.default_content
        GetSerpPosition(None)
    else:
        f.close()
        driver.quit()
        firstPageCounter = list(filter(lambda x : x <= 10, keyWordIndex))
        print(f'Keywords on the first page: {len(firstPageCounter)}')
        print('Finished!')        

def LoginGoogleAccount(email, pwd):
    print('Performing Login...')
    driver.get('https://accounts.google.com/signin/v2/identifier')
    emailInput = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="E-mail ou telefone"]')))
    emailInput.send_keys(email, Keys.ENTER)
    # emailButton = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'identifierNext')))
    # ActionChains(driver).move_to_element(emailInput).click(emailInput).send_keys(email).move_to_element(emailButton).click(emailButton).perform()
    time.sleep(5)
    pwdInput = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Digite sua senha"]')))
    pwdInput.send_keys(pwd, Keys.ENTER)
    # pwdButton = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, 'passwordNext')))
    # ActionChains(driver).move_to_element(pwdInput).click(pwdInput).send_keys(pwd, Keys.ENTER).perform()
    time.sleep(3)
    print('Successful Login!\n')
    GetSerpPosition('https://www.google.com.br/search?q=google')

def CheckLocalCredentials():
    try:
        userDataFile = open(os.path.join(currentDirectory, 'user.auth'), 'r', encoding='utf-8')
        userDataList = []

        for line in userDataFile:
            userDataList.append(line)

        googleEmail = base64.b64decode(userDataList[0]).decode()
        googlePwd = base64.b64decode(userDataList[1]).decode()
    except:
        googleEmail = input('Type your Google e-mail: ')
        googlePwd = getpass()

        userDataFile = open(os.path.join(currentDirectory, 'user.auth'), 'w+', encoding='utf-8')
        userDataFile.write(f'{base64.b64encode(googleEmail.encode()).decode()}\n{base64.b64encode(googlePwd.encode()).decode()}')
        userDataFile.close()

    LoginGoogleAccount(googleEmail, googlePwd)


# Access site and get mpis TO DO
CheckLocalCredentials()
