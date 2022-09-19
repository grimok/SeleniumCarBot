import sys
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from selenium.webdriver.support.wait import WebDriverWait

import random


#
# Bunu implemente edelim, hem menü için hem temiz görünüm açısından çok daha güzel durucak
#
def log(message, logLevel=0):
    match logLevel:
        case 0:
            print("[DEBUG] " + message)
            return
        case 1:
            print("[INFO] " + message)
        case 2:
            print("[WARNING] " + message)
        case 3:
            print("[ERROR/SEVERE] " + message)
        case default:
            print(message)


class SearchAgent:
    driver = None
    loadingURL = None
    sucess = 0
    totalcars = 0
    targetList = []

    def __init__(self, loadingURL: str):
        print('Initing!')
        self.loadingURL = loadingURL
        options = Options()
        options.page_load_strategy = 'eager'
        disableInfoBar = ['enable-automation']
        options.add_experimental_option('excludeSwitches', disableInfoBar)
        # options.add_argument("--disable-extensions")

        ua = UserAgent()
        rua = ua.chrome

        # EXTENSION INIT
        print("Initializing Extensions")
        # options.add_extension('C:\\Users\\redacted\\Desktop\\CRX3-Creator-master\\Browsec.crx')
        try:
            options.add_extension('Buster.crx')
        except:
            print("Extension setup has failed! Please check extension file is installed!")
        print("Extension setup completed.")
        # EXTENSION END

        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 '
                         'Safari/537.36'})
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.delete_cache()
        self.driver.get(self.loadingURL)
        self.check_captcha()
        self.checkCookie()
        self.driver.get(loadingURL)
        self.check_captcha()
        self.checkCookie()

    #
    # Test edemedim hiç captchaya rastlayamadım
    # Made by: KardasLand
    # This is not working! Google reCaptcha finds this is automation control!
    # This code will be changed 2Captcha API Later
    #
    def check_captcha(self):
        # self.driver.switch_to.default_content()
        # try:
        time.sleep(15)
        # if len(self.driver.find_elements(By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.recaptcha.net/recaptcha/api2/anchor?']")) > 0:
        if len(self.driver.find_elements(By.ID, "sec-cpt-if")) > 0:
            log("Captcha detected.", 1)

            ids = self.driver.find_elements(By.XPATH, '//*[@id]')

            log("Main IDS")
            for ii in ids:
                # print ii.tag_name
                print(str(ii.get_attribute('id')))  # id name as string

            # allelements = list(self.driver.find_elements(By.XPATH, './/*'))
            # for x in allelements:
            #    log(str(x.id))

            frame = self.driver.find_element(By.ID, "sec-cpt-if")
            self.driver.switch_to.frame(frame)
            ids = self.driver.find_elements(By.XPATH, '//*[@id]')
            log("Main iFrame IDS")
            for ii in ids:
                # print ii.tag_name
                print(str(ii.get_attribute('id')))  # id name as string

            inner_frame = self.driver.find_element(By.XPATH, '//*[@id="g-recaptcha"]/div/div/iframe')
            print(str(inner_frame.get_attribute('src')))

            self.driver.switch_to.frame(inner_frame)

            ids = self.driver.find_elements(By.XPATH, '//*[@id]')
            log("Inner iFrame IDS")
            for ii in ids:
                # print ii.tag_name
                print(str(ii.get_attribute('id')))  # id name as string

            # time.sleep(500)
            # WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it(
            #    (By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))

            captchaButton = self.driver.find_element(By.XPATH, '//*[@id="recaptcha-anchor"]')
            self.driver.execute_script("arguments[0].click()", captchaButton)

            time.sleep(2)

            self.driver.switch_to.default_content()

            frame = self.driver.find_element(By.ID, "sec-cpt-if")
            self.driver.switch_to.frame(frame)

            ids = self.driver.find_elements(By.XPATH, '//*[@title]')
            captchaWindow = None
            log("MainWindow IDS")
            for ii in ids:
                # print ii.tag_name
                print(str(ii.get_attribute('title')))  # id name as string
                if (ii.get_attribute('title').__eq__("recaptcha challenge expires in two minutes")):
                    captchaWindow = ii

            self.driver.switch_to.frame(captchaWindow)

            time.sleep(2)

            ids = self.driver.find_elements(By.XPATH, '//*[@class]')
            log("CaptchaFrame Classes")
            for ii in ids:
                # print ii.tag_name
                print(str(ii.get_attribute('class')))  # id name as string

            actions = ActionChains(self.driver)
            actions.send_keys(Keys.TAB * 2)
            time.sleep(4)
            actions.send_keys(Keys.ENTER)
            actions.perform()

            # shadow = Shadow(self.driver) element = shadow.get_shadow_element(self.driver.find_element(
            # By.CLASS_NAME, "button-holder.help-button-holder"), "button#solver-button")

            # log(str(element.title))

            time.sleep(2000)

            # def expand_shadow_element(driver, element):
            #    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
            #    return shadow_root

            # outer = expand_shadow_element(self.driver, self.driver.find_element(By.CLASS_NAME, "button-holder.help-button-holder"))
            # inner = outer.find_element(By.ID, "solver-button")
            # inner.click()

            # shadow_root = self.driver.find_element(By.CLASS_NAME, 'button-holder.help-button-holder').shadow_root
            # element_in_shadow_root = shadow_root.find_element(By.ID, 'solver-button')
            # self.driver.execute_script("arguments[0].click()", element_in_shadow_root)
        else:
            log("There is no captcha, moving on.")
        # except:
        #    log("There is no captcha, moving on.")

    def delete_cache(self):
        self.driver.execute_script("window.open('');")
        time.sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(2)
        self.driver.get('chrome://settings/clearBrowserData')  # for old chromedriver versions use cleardriverData
        time.sleep(2)
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB * 3 + Keys.DOWN * 3)  # send right combination
        actions.perform()
        time.sleep(2)
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB * 4 + Keys.ENTER)  # confirm
        actions.perform()
        time.sleep(5)  # wait some time to finish
        self.driver.close()  # close this tab
        self.driver.switch_to.window(self.driver.window_handles[0])  # switch back

    def eraseCache(self):
        self.driver.execute_script("window.localStorage.clear()")
        self.driver.delete_all_cookies()
        time.sleep(2)
        self.delete_cache()

    def loadSiteOnNewTab(self, url: str):
        self.driver.execute_script("window.open('');")
        time.sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(url)

    def returnMainTab(self):
        time.sleep(2)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def checkCookie(self):
        time.sleep(7)
        try:
            self.driver.find_element(By.XPATH,
                                     '//*[@id="mde-consent-modal-container"]/div[2]/div[2]/div[1]/button').click()
        except:
            print("I did not find any cookie :>")

    def checkPageSize(self) -> int:
        time.sleep(10)
        pageElement = self.driver.find_element(By.CLASS_NAME, 'pagination')
        links = list(pageElement.find_elements(By.TAG_NAME, "li"))
        pageSize = int(
            links[-2].get_attribute("innerHTML").split("data-touch=\"link\"", maxsplit=1)[0].rsplit("\"", 1)[0].split(
                "Seite ", maxsplit=2)[1])
        print(f'Active pages: {pageSize}')
        return pageSize

    def listCars(self):
        self.targetList = []
        self.driver.implicitly_wait(10)
        time.sleep(2)
        elements = list(self.driver.find_elements(By.XPATH, '//a[@href]'))
        print(f'Loaded elements : {len(elements)}')

        for x in elements:
            if x.get_attribute("href").find("action=eyeCatcher") != -1:
                self.targetList.append(x.get_attribute("href"))

        print(f'Filtered : {len(self.targetList)}')

    def betaTest(self):
        self.driver.execute_script("window.localStorage.clear()")
        testList = []
        self.driver.get(f"https://suchen.mobile.de/fahrzeuge/search.html?adLimitation=ONLY_FSBO_ADS"
                                  f"&damageUnrepaired=NO_DAMAGE_UNREPAIRED&isSearchRequest=true&makeModelVariant1"
                                  f".makeId=1900&makeModelVariant1.modelId=9&pageNumber="
                                  f"{1}&ref=srpPreviousPage&scopeId=C&sortOption.sortBy=relevance&refId=23bbd1ef-2fa1"
                                  f"-4123-ab94-2d4af888c843")
        self.driver.implicitly_wait(10)
        time.sleep(10)
        self.check_captcha()
        elements = list(self.driver.find_elements(By.XPATH, '//a[@data-listing-id]'))
        log(f'Finded elements: {len(elements)}', 1)
        for x in elements:
            print(x)
        time.sleep(600)

    def writeMail(self):
        msgbox = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id=\"vip-contact-form\"]/div/div[1]/textarea")))
        msgbox.clear()
        print("Passed!")
        time.sleep(2)
        msgbox.send_keys("a")
        time.sleep(2)
        nameTxtBox = self.driver.find_element(By.XPATH, "//*[@id=\"vip-contact-form\"]/div/div[2]/div[1]/div/div/input")
        nameTxtBox.clear()
        nameTxtBox.send_keys("b")
        time.sleep(2)
        email = self.driver.find_element(By.XPATH, "//*[@id=\"contact-type-email-section\"]/div/div/input")
        email.clear()
        email.send_keys("yigityilmaz1923@hotmail.com")

    # Success hesaplamasını değiştirdim daha güzel bir sonuç veriyor artık
    # Ama sanki page hesaplaması bir garip olmuş tam verimli çalışmıyor gibi
    def sendMails(self):
        print("Sending Mails!")
        page = 1
        for y in range(1, 51):
            log("Entering page #" + page)
            self.eraseCache()
            self.loadSiteOnNewTab(f"https://suchen.mobile.de/fahrzeuge/search.html?adLimitation=ONLY_FSBO_ADS"
                                  f"&damageUnrepaired=NO_DAMAGE_UNREPAIRED&isSearchRequest=true&makeModelVariant1"
                                  f".makeId=1900&makeModelVariant1.modelId=9&pageNumber="
                                  f"{y}&ref=srpPreviousPage&scopeId=C&sortOption.sortBy=relevance&refId=23bbd1ef-2fa1"
                                  f"-4123-ab94-2d4af888c843")
            self.check_captcha()
            self.checkCookie()
            self.listCars()
            for x in self.targetList:
                self.totalcars += 1
                self.driver.execute_script("window.localStorage.clear()")
                self.driver.delete_all_cookies()
                self.driver.set_window_size(random.randint(512, 1024), random.randint(512, 1920))
                time.sleep(2)
                print(f'Entering car #{page}')
                print(x)
                self.loadSiteOnNewTab(x)
                self.checkCookie()
                try:
                    self.writeMail()
                    self.sucess += 1
                except:
                    print("The car has been closed :<")
                ratio = (self.sucess / self.totalcars) * 100
                print(f'Success rate : {ratio}%')
                self.returnMainTab()
                page += 1
            self.returnMainTab()
