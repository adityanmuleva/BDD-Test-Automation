import os, sys
# sys.path.append(os.path.join((os.path.realpath(__file__)).split("common_lib")[0]))
import selenium
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, \
    ElementNotVisibleException
from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import *
from selenium.webdriver.support.color import Color
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import subprocess
import logging


class ServerWebSeleniumUtils:
    def __init__(self, working_browser="Chrome"):
        """
        This __init__ method will get executed by default when the ServerWebSeleniumUtils instance is created
        This method will check the browser version present in the test machine and will auto fetch the driver supported version
        :param working_browser: Browser which must be used for testing
        This method will save the global "web_driver_global" to stay connected for controlling the  Browser Session
        """
        if working_browser.casefold() == "chrome":
            options = webdriver.ChromeOptions()
            # options.add_argument("--no-sandbox")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.set_capability('acceptInsecureCerts', True)
            web_driver_global = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        else:
            assert False, "Mentioned browser '{}' not supported. Supported browsers: chrome".format(working_browser)

        logging.info("====> Initialized Selenium Web driver of class ServerWebSeleniumUtils for  Server <===")
        logging.info("Web Server Browser Selected is --> '{}'".format(working_browser))
        logging.info("Web Server Selenium Driver initiated is --> '{}'".format(web_driver_global))
        logging.info("Web Server Selenium Driver Title--> '{}'".format(web_driver_global.title))
        self.web_driver_global = web_driver_global

    def fetchDriver(self):
        """
        This method is to fetch the driver which is loaded
        :return: Driver in control
        """
        try:
            logging.info("Driver in control is '{}'".format(self.web_driver_global))
            return self.web_driver_global
        except Exception as err:
            logging.error(err)
            assert False

    def refresh_page(self):
        """
        This method is to refresh  page
        :return: if pass return True
        """
        try:
            logging.info("About to refresh  page")
            self.web_driver_global.refresh()
            logging.info(" page refresh successfully !")
        except Exception as err:
            logging.error(err)
            assert False

    def NavigateToFrame(self, xpath):
        """
        This method is to Navigate to mentioned frame in browser
        :param path: xpath that needs to be navigated
        :return: True if successful, else return False
        """
        try:
            logging.info("Navigating the Frame '{}'".format(xpath))
            self.web_driver_global.switch_to.frame(self.web_driver_global.find_element_by_xpath(xpath))
            logging.info("Navigated To {} Frame successfully".format(xpath))
            return True
        except Exception as err:
            logging.error(err)
            assert False

    def NavigateToParentFrame(self):
        """
        This method is to Navigate to mentioned frame in browser
        :return: True if successful, else return False
        """
        try:
            logging.info("Navigating the Parent Frame")
            self.web_driver_global.switch_to.parent_frame()
            logging.info("Navigated To Parent Frame successfully")
            return True
        except Exception as err:
            logging.error(err)
            assert False

    def OpenURLAndNavigateFrameAndVerifyXpathPresent(self, URL, frame_xpath, xpath, timeout=10):
        """
        This method is to open mentioned url in browser and verify if expected xpath is found
        :param URL: URL to be opened
        :param path: xpath that needs to be checked after after URL is opened
        :param timeout: timeout in seconds
        :return: True if successful, else return False
        """
        try:
            logging.info("Opening the URL '{}'".format(URL))
            self.web_driver_global.get(URL)
            self.NavigateToFrame(frame_xpath)
            status = self.CheckIfXpathExist(xpath)
            if status:
                logging.info("Opened {} Page URL successfully".format(URL))
                return True
            else:
                logging.error("Failed to Open {} Page URL".format(URL))
                return False
        except Exception as err:
            logging.error(err)
            assert False

    def OpenURLAndVerifyXpathPresent(self, URL, xpath, timeout=10):
        """
        This method is to open mentioned url in browser and verify if expected xpath is found
        :param URL: URL to be opened
        :param path: xpath that needs to be checked after after URL is opened
        :param timeout: timeout in seconds
        :return: True if successful, else return False
        """
        try:
            logging.info("Opening the URL '{}'".format(URL))
            self.web_driver_global.get(URL)
            status = self.CheckIfXpathExist(xpath)
            if status:
                logging.info("Opened {} Page URL successfully".format(URL))
                return True
            else:
                logging.error("Failed to Open {} Page URL".format(URL))
                return False
        except Exception as err:
            logging.error(err)
            assert False

    def OpenURL(self, URL, timeout=10):
        """
        This method is to open mentioned url in browser
        :param URL: URL to be opened
        :param timeout: timeout in seconds
        :return: True if successful, else return False
        """
        try:
            logging.info("Opening the URL '{}'".format(URL))
            self.web_driver_global.get(URL)
            logging.info("Opened {} Page URL successfully".format(URL))
            return True
        except Exception as err:
            logging.error(err)
            assert False

    def WaitForXpath(self, xpath, timeout=10):
        """
        This method is to Wait till the expected xpath is clickable/ appears, Default Timeout= 5 seconds
        :param xpath: xpath of the element to wait for
        :param timeout: timeout in seconds
        :return: True if successful, else return False
        """
        try:
            elem = WebDriverWait(self.web_driver_global, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            logging.info("found xpath {}".format(xpath))
            return True
        except NoSuchElementException:
            err = "No such element with xpath {}".format(xpath)
            logging.error(err)
            return False
        except TimeoutException:
            err = "TIMEOUT: Unable to find xpath {}".format(xpath)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def WaitForXpathtoDisappear(self, xpath, timeout=10):
        """
        This method is to Wait till the expected xpath is Disappers or becomes invisible Default Timeout= 5 seconds
        :param xpath: xpath of the element to wait for
        :param timeout: timeout in seconds
        :return: True if successful, else return False
        """
        try:
            time.sleep(5)  ## As there is a delay even though below logic added, will remove after root cause
            timeout_start = time.time()
            while time.time() < timeout_start + timeout:
                try:
                    WebDriverWait(self.web_driver_global, 1).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                except TimeoutException:
                    logging.info("xpath '{}' is invisibe/ not present".format(xpath))
                    return True
            logging.error("xpath '{}' is visible. Expected to disappear/ become invicible".format(xpath))
            return False
        except Exception as err:
            logging.error(err)
            return False

    def WaitForLink(self, link_text, timeout=10):
        """
        This method is to wait for mentioned link text to be clickable/ available in given timeout.
        :param link_text: text of the link
        :param timeout: Timeout in seconds for link. Default= 10 seconds
        :return: True if link text is cleared, else return False
        """
        try:
            elem = WebDriverWait(self.web_driver_global, timeout).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text)))
            logging.info("link with text {} is available".format(link_text))
            return True
        except NoSuchElementException:
            err = "link with text {} is not available".format(link_text)
            logging.error(err)
            return False
        except TimeoutException:
            err = "Timeout: Unable to find link with text {}".format(link_text)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def IsTextExistsInXpath(self, xpath, TEXT, timeout=10):
        """
        This method is to verify if the provided TEXT exists in the xpath
        :param xpath: xpath of the element
        :param TEXT: text to find in the provided xpath
        :param timeout: timeout in seconds
        :return: True if successful, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = self.web_driver_global.find_element_by_xpath(xpath)

            # print("Element.text==>" , elem.text)
            # print("Element Attribute==>" , elem.get_attribute('value'))
            # print("Element Property==>" , elem.get_property('value'))

            if (str(elem.text) == str(TEXT) or elem.get_attribute('value') == str(TEXT) or elem.get_attribute(
                    'textContent') == str(TEXT)):
                logging.info("found expected text '{}' in xpath {}".format(elem.text, xpath))
                return True
            else:
                err = "Could not find {} with TEXT '{}', actual found '{}' '{}'".format(xpath, TEXT, elem.text,
                                                                                        elem.get_attribute(
                                                                                            'textContent'))
                logging.error(err)
                return False
        except Exception as err:
            logging.error(err)
            return False

    def getText_In_Xpath(self, xpath, timeout=10):
        """
        This method is to get the text present in the provided xpath
        :param xpath: xpath of the element to wait for
        :param timeout: timeout in seconds
        :return: text if successful, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            element = self.web_driver_global.find_element_by_xpath(xpath)
            logging.info("found text '{}' in {}".format(element.text, xpath))
            return element.text
        except Exception as err:
            logging.error(err)
            return False

    def GetAttributeTextValueInXpath(self, xpath, timeout=10):
        """
        This method is to get the element value in 'value' attribute
        :param xpath: xpath of the element
        :param timeout: timeout in seconds
        :return: attribute text value if successful, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = self.web_driver_global.find_element_by_xpath(xpath)
            logging.info("found text '{}' in {}".format(elem.get_attribute('value'), xpath))
            return elem.get_attribute('value')
        except Exception as err:
            logging.error(err)
            return False

    def GetValueofAttributeInXpath(self, xpath, attribute, timeout=10):
        """
        This method is to get the element value of mentioned attribute
        :param xpath: xpath of the element
        :param attribute: attribute name whose value needs to be fetched
        :param timeout: timeout in seconds
        :return: specified attribute value if successful, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = self.web_driver_global.find_element_by_xpath(xpath)
            logging.info("found text '{}' in {}".format(elem.get_attribute(attribute), xpath))
            return elem.get_attribute(attribute)
        except Exception as err:
            logging.error(err)
            return False

    def GetMultipleElements_ListByValueInXpath(self, xpath, timeout=10):
        """
        This method is to get the all the element text values in the mentioned element xpath value attribute
        :param xpath: xpath of the element
        :param timeout: timeout in seconds
        :return: list of text values if successful, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = self.web_driver_global.find_elements_by_xpath(xpath)
            newlist = []
            for eachele in elem:
                newlist.append(eachele.get_attribute('value'))
            logging.info("Found following Text values in {} xpath 'value' attribute: {}".format(xpath, newlist))
            return newlist
        except Exception as err:
            logging.error(err)
            return False

    def GetMultipleElements_TextListInXpath(self, xpath, timeout=10):
        """
        This method is to get the all the element text values in the mentioned element xpath.text
        :param xpath: xpath of the element
        :param timeout: timeout in seconds
        :return: list of text values if successful, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = self.web_driver_global.find_elements_by_xpath(xpath)
            newlist = []
            for eachele in elem:
                newlist.append(eachele.text)
            logging.info("Found following Text values in {} xpath: {}".format(xpath, newlist))
            return newlist
        except Exception as err:
            logging.error(err)
            return False

    def GetMultipleElements_ListByAttributeInXpath(self, xpath, attribute, timeout=10):
        """
        This method is to get the all the element values in the mentioned element xpath attribute
        :param xpath: xpath of the element
        :param attribute: attribute name whose value needs to be fetched
        :param timeout: timeout in seconds
        :return: list of text values if successful, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = self.web_driver_global.find_elements_by_xpath(xpath)
            newlist = []
            for eachele in elem:
                newlist.append(eachele.get_attribute(attribute))
            logging.info("Found following values in {} xpath with attribute {}: {}".format(xpath, attribute, newlist))
            return newlist
        except Exception as err:
            logging.error(err)
            return False

    def GetSelectedOptionText(self, xpath, timeout=10):
        """
        This method is to get the Default Selected option in the mentioned element xpath
        :param xpath: xpath of the element
        :param timeout: timeout in seconds
        :return: default selected option if successful, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            select = Select(self.web_driver_global.find_element_by_xpath(xpath))
            selected_option = select.first_selected_option
            logging.info("got text {} in {}".format(selected_option.text, xpath))
            return selected_option.text
        except Exception as err:
            logging.error(err)
            return False

    def GetEncodedTextInXpath(self, xpath, timeout=10):
        """
        This method is to get the encoded text in the mentioned element xpath
        :param xpath: xpath of the element
        :param timeout: timeout in seconds
        :return: encoded text in UTF-8 format if successful, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = self.web_driver_global.find_element_by_xpath(xpath)
            logging.info("found following encoded text {} in xpath {}".format(str((elem.text).encode("utf-8")), xpath))
            return str(elem.text.encode("utf-8"))
        except Exception as err:
            logging.error(err)
            return False

    def isXpathEnabled(self, xpath, sleep=0):
        """
        This method is to check if the mentioned element xpath is enabled
        :param xpath: xpath of the element
        :param sleep: any delay in seconds to be added before starting method. Default set to 0
        :return: True if element xpath enabled, else return False
        """
        try:
            time.sleep(sleep)
            webelement = self.web_driver_global.find_element_by_xpath(xpath)
            if webelement.is_enabled():
                logging.info("ELement with xpath {} is enabled".format(xpath))
                return True
            else:
                err = "Element with xpath {} is not enabled".format(xpath)
                logging.error(err)
                return False
        except ElementNotVisibleException:
            err = "Element {} is not Visble or found".format(xpath)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def GetXpathCssValue(self, xpath, cssvalue, timeout=10):
        """
        This method is to fetch the css value of the provided element xpath
        :param xpath: xpath of the element
        :param cssvalue: css value
        :param timeout: timeout in seconds
        :return: css property value if found, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = self.web_driver_global.find_element_by_xpath(xpath)
            logging.info(
                "ELement with xpath {} has following css value {}".format(xpath, elem.value_of_css_property(cssvalue)))
            return elem.value_of_css_property(cssvalue)
        except Exception as err:
            logging.error(err)
            return False

    def isXpathClickable(self, xpath, timeout=10):
        """
        This method is to check if the provided element xpath is clickable
        :param xpath: xpath of the element
        :param timeout: timeout in seconds
        :return: True if successful, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            logging.info("Element with xpath {} Exists".format(xpath))
            return True
        except TimeoutException:
            err = "Element with xpath {} Doesn't Exists".format(xpath)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def CheckIfXpathExist(self, xpath, timeout=10):
        """
        This method is to check if the provided element xpath exists
        :param xpath: xpath of the element
        :param timeout: timeout in seconds
        :return: True if xpath exists, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = self.web_driver_global.find_element_by_xpath(xpath)
            logging.info("xpath {} exists".format(xpath))
            return True
        except NoSuchElementException:
            err = "xpath {} doesn't exists".format(xpath)
            logging.error(err)
            return False
        except TimeoutException:
            err = "Time out error while waiting for xpath {}".format(xpath)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def isLinkEnabledAndDisplayed(self, link_txt, timeout=10):
        """
        This method is to check if the provided link text is enabled and displayed
        :param link_txt: Link Text
        :param timeout: timeout in seconds
        :return: True if link text is enabled and displayed, else return False
        """
        try:
            elem = WebDriverWait(self.web_driver_global, timeout).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_txt)))
            # class_name = elem.get_attribute("class")
            if elem.is_enabled() and elem.is_displayed():  # and class_name.find("disabledBtn") < 0:
                logging.info("link {} is enabled and clickable".format(link_txt))
                return True
            else:
                logging.error("link {} is disabled/ cannot be clicked".format(link_txt))
                return False
        except NoSuchElementException:
            err = "link with text {} does not exist".format(link_txt)
            logging.error(err)
            return False
        except TimeoutException:
            err = "Timeout error while waiting for link {}".format(link_txt)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def CheckIfLinkExists(self, link_txt, timeout=10):
        """
        This method is to check if the provided link text exists
        :param txt: Link Text
        :param timeout: timeout in seconds
        :return: True if link text exists, else return False
        """
        try:
            self.WaitForLink(link_txt, timeout)
            logging.info("link with text '" + link_txt + "' Exists")
            return True
        except NoSuchElementException:
            err = "link with text {} does not exist".format(link_txt)
            logging.error(err)
            return False
        except TimeoutException:
            err = "Timeout error while clicking on" + link_txt
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def CheckElementWithIdExists(self, id_text, timeout=10):
        """
        This method is to check if the element with ID provided exists
        :param id_text: ID to be checked for
        :param timeout: timeout in seconds
        :return: True if ID exists, else return False
        """
        try:
            elem = WebDriverWait(self.web_driver_global, timeout).until(EC.element_to_be_clickable((By.ID, id_text)))
            logging.info("Element with id " + id_text + " Exist")
            return True
        except TimeoutException:
            err = "time out error while waiting for element with id {}".format(id_text)
            logging.error(err)
            return False
        except NoSuchElementException:
            err = "Element with id {} does not exist".format(id_text)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def EnterTextInXpathReact(self, xpath, txt, clearText=True, timeout=10):
        """
        This method is to enter text in the mentioned React element xpath
        :param xpath: xpath when text has to be entered
        :param txt: Text to be entered in the mentioned xpath
        :param clearText: Default to True,
        :param timeout: timeout in seconds
        :return: True if text is entered, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = self.web_driver_global.find_element_by_xpath(xpath)
            if clearText == True:
                logging.info("Clearing text in xpath {}".format(xpath))
                # self.web_driver_global.implicitly_wait(10)
                # ActionChains(driver).move_to_element(button).click(button).perform()
                elem.send_keys(Keys.CONTROL + "a")
                elem.send_keys(Keys.DELETE)
            elem.send_keys(txt)

            act_text_by_attributevalue = self.GetAttributeTextValueInXpath(xpath)
            act_text_by_text = self.getText_In_Xpath(xpath)

            if act_text_by_attributevalue == txt or act_text_by_text == txt:
                logging.info("Entered {} in xpath {}".format(txt, xpath))
                return True
            else:
                logging.error("Couldn't Enter {} in xpath {}".format(txt, xpath))
                logging.error("Actual Value in xpath attribute value is {}".format(act_text_by_attributevalue))
                logging.error("Actual Value in xpath text value is {}".format(act_text_by_text))
                return False
        except TimeoutException:
            err = 'TIMED OUT: Given element is not displayed: {}'.format(xpath)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def EnterTextInXpath(self, xpath, txt, clearText=True, timeout=10):
        """
        This method is to enter text in the mentioned element xpath
        :param xpath: xpath when text has to be entered
        :param txt: Text to be entered in the mentioned xpath
        :param clearText: Default to True,
        :param timeout: timeout in seconds
        :return: True if text is entered, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = self.web_driver_global.find_element_by_xpath(xpath)
            self.web_driver_global.implicitly_wait(10)
            if clearText == True:
                logging.info("Clearing text in xpath {}".format(xpath))
                elem.clear()
            elem.send_keys(txt)

            act_text_by_attributevalue = self.GetAttributeTextValueInXpath(xpath)
            act_text_by_text = self.getText_In_Xpath(xpath)
            if act_text_by_attributevalue == txt or act_text_by_text == txt:
                logging.info("Entered {} in xpath {}".format(txt, xpath))
                return True
            else:
                logging.error("Couldn't Enter {} in xpath {}".format(txt, xpath))
                logging.error("Actual Value in xpath attribute value is {}".format(act_text_by_attributevalue))
                logging.error("Actual Value in xpath text value is {}".format(act_text_by_text))
                return False
        except TimeoutException:
            err = 'TIMED OUT: Given element is not displayed: {}'.format(xpath)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def ClearTextInXpath(self, xpath, timeout=10):
        """
        This method is to Clear the text in the mentioned element xpath
        :param xpath: xpath when text has to be cleared
        :param timeout: timeout in seconds
        :return: True if text is cleared, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = self.web_driver_global.find_element_by_xpath(xpath)
            elem.clear()
            act_text = self.GetAttributeTextValueInXpath(xpath)
            if act_text == "":
                logging.info("Cleared text in xpath {}".format(xpath))
                return True
            else:
                logging.error("Couldn't Clear text in xpath {}".format(xpath))
                logging.error("Actual Value in xpath is {}".format(act_text))
                return False
        except TimeoutException:
            err = 'TIMED OUT: Given element is not displayed: {}'.format(xpath)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def ClickLinkWithText(self, text, timeout=10):
        """
        This method is to Click on link with mentioned text
        :param text: text of the link
        :param timeout: timeout in seconds
        :return: True if clicked on link text, else return False
        """
        try:
            self.WaitForLink(text, timeout)
            elem = self.web_driver_global.find_element_by_link_text(text)
            # self.web_driver_global.execute_script('arguments[0].click()', elem)
            elem.click()
            logging.info("Clicked on Link with text {}".format(text))
            return True
        except Exception as err:
            logging.error(err)
            return False

    def ClickLinkWithPartialText(self, partail_text, timeout=10):
        """
        This method is to Click on link with partial link text provided
        :param partail_text: text of the link
        :param timeout: timeout in seconds
        :return: True if clicked on link with partial text provided, else return False
        """
        try:
            elem = WebDriverWait(self.web_driver_global, timeout).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, partail_text)))
            elem = self.web_driver_global.find_element_by_partial_link_text(partail_text)
            # self.web_driver_global.execute_script('arguments[0].click()', elem)
            elem.click()
            logging.info("Clicked on Link with partial text {}".format(partail_text))
            return True
        except Exception as err:
            logging.error(err)
            return False

    def left_click_element_by_xpath(self, xpath, timeout=10):
        """
        This method is to Click on element xpath
        :param xpath: xpath of the element
        :param timeout: timeout in seconds
        :return: True if clicked on xpath, else return False
        """
        try:
            time.sleep(1)  ##Added implicitly to ensure mouse click
            self.WaitForXpath(xpath, timeout)
            element = self.web_driver_global.find_element_by_xpath(xpath)
            self.web_driver_global.execute_script('arguments[0].click()', element)
            # element.click()
            logging.info("Clicked on xpath {}".format(xpath))
            return True
        except TimeoutException:
            err = 'TIMEOUT: Given element is not displayed: {}'.format(xpath)
            logging.error(err)
            return False
        except ElementNotVisibleException:
            err = "Element is not visible.. check the xpath {}".format(xpath)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def click_element_by_xpath(self, xpath, timeout=10):
        """
        This method is to Click on element xpath
        :param xpath: xpath of the element
        :param timeout: timeout in seconds
        :return: True if clicked on xpath, else return False
        """
        try:
            time.sleep(1)  ##Added implicitly to ensure mouse click
            self.WaitForXpath(xpath, timeout)
            element = self.web_driver_global.find_element_by_xpath(xpath)
            # self.web_driver_global.execute_script('arguments[0].click()', element)
            element.click()
            logging.info("Clicked on xpath {}".format(xpath))
            return True
        except TimeoutException:
            err = 'TIMEOUT: Given element is not displayed: {}'.format(xpath)
            logging.error(err)
            return False
        except ElementNotVisibleException:
            err = "Element is not visible.. check the xpath {}".format(xpath)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def click_element_by_cssSelector(self, cssselector, timeout=10):
        """
        This method is to Click on element with provided css selector
        :param cssselector: cssselector of the element
        :param timeout: timeout in seconds
        :return: True if clicked on cssselector, else return False
        """
        try:
            element = WebDriverWait(self.web_driver_global, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, cssselector)))
            element = self.web_driver_global.find_element_by_css_selector(cssselector)
            # self.web_driver_global.execute_script('arguments[0].click()', element)
            element.click()
            logging.info("Clicked on CSS Selector {}".format(cssselector))
            return True
        except TimeoutException:
            err = 'TIMEOUT: Given element is not displayed: {}'.format(cssselector)
            logging.error(err)
            return False
        except ElementNotVisibleException:
            err = "Element is not visible.. check the css selector {}".format(cssselector)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def click_element_by_id(self, id_text, timeout=10):
        """
        This method is to Click on element with provided ID
        :param id_text: id_text of the element
        :param timeout: timeout in seconds
        :return: True if clicked on id_text mentioned, else return False
        """
        try:
            element = WebDriverWait(self.web_driver_global, timeout).until(EC.element_to_be_clickable((By.ID, id_text)))
            element = self.web_driver_global.find_element_by_id(id_text)
            # self.web_driver_global.execute_script('arguments[0].click()', element)
            element.click()
            logging.info("Clicked on Element with ID {}".format(id_text))
            return True
        except TimeoutException:
            err = 'TIMEOUT: Given ID element is not displayed: {}'.format(id_text)
            logging.error(err)
            return False
        except ElementNotVisibleException:
            err = "ID Element is not visible.. check the ID {}".format(id_text)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def click_element_by_name(self, name, timeout=10):
        """
        This method is to Click on element by name
        :param name: name of the element
        :param timeout: timeout in seconds
        :return: True if clicked on name mentioned, else return False
        """
        try:
            element = WebDriverWait(self.web_driver_global, timeout).until(EC.element_to_be_clickable((By.NAME, name)))
            element = self.web_driver_global.find_element_by_name(name)
            # self.web_driver_global.execute_script('arguments[0].click()', element)
            element.click()
            logging.info("Clicked on Element with Name {}".format(name))
            return True
        except TimeoutException:
            err = 'TIMEOUT: Given Name element is not displayed: {}'.format(name)
            logging.error(err)
            return False
        except ElementNotVisibleException:
            err = "Name Element is not visible.. check the ID {}".format(name)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def click_element_by_classname(self, class_name, timeout=10):
        """
        This method is to Click on element by Class name
        :param class_name: class_name of the element
        :param timeout: timeout in seconds
        :return: True if clicked on class_name mentioned, else return False
        """
        try:
            element = WebDriverWait(self.web_driver_global, timeout).until(
                EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
            element = self.web_driver_global.find_element_by_class_name(class_name)
            # self.web_driver_global.execute_script('arguments[0].click()', element)
            element.click()
            logging.info("Clicked on Element with Class Name {}".format(class_name))
            return True
        except TimeoutException:
            err = 'TIMEOUT: Given Name element is not displayed: {}'.format(class_name)
            logging.error(err)
            return False
        except ElementNotVisibleException:
            err = "Element is not visible.. check the Class Name {}".format(class_name)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def SelectElementWithVisibleText(self, xpath, txt, timeout=10):
        """
        This method is to Select the element with mentioned text in the Options available in xpath
        :param xpath: xpath of the element
        :param txt: txt element which needs to be selected in provided xpath
        :param timeout: timeout in seconds
        :return: True if selected sucssfully, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            select_box = self.web_driver_global.find_element_by_xpath(xpath)
            selectelem = Select(self.web_driver_global.find_element_by_xpath(xpath))
            options = [x for x in select_box.find_elements_by_tag_name("option")]
            for elem in options:
                if (elem.text).find(txt) > -1:
                    selectelem.select_by_visible_text(elem.text)
                    logging.info("selected {} from {}".format(elem.text, xpath))
                    return True
        except NoSuchElementException:
            err = "element with xpath {} not found".format(xpath)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def GetElementOptions(self, xpath, timeout=10):  ##admin policy tool
        """
        This method is to Get the element options in xpath
        :param xpath: xpath of the element
        :param timeout: timeout in seconds
        :return: List of element options in provided xpath, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            selectelem = Select(self.web_driver_global.find_element_by_xpath(xpath))
            return [x.text for x in selectelem.options]
        except NoSuchElementException:
            err = "element with xpath {} not found".format(xpath)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def SelectElementInXpath(self, xpath, txt, timeout=10):  ##admin
        """
        This method is to select the text element in the xpath mentioned
        :param xpath: xpath of the element
        :param txt: Text to be selected in xpath
        :param timeout: timeout in seconds
        :return: True if element selected in xpath, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = Select(self.web_driver_global.find_element_by_xpath(xpath))
            elem.select_by_visible_text(txt)
            logging.info("selected {} from {}".format(txt, xpath))
            return True
        except NoSuchElementException:
            err = "element with xpath {} not found".format(xpath)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def SelectElementfromClass(self, className, txt, timeout=10):
        """
        This method is to select the text element in the class name mentioned
        :param className: className of the element
        :param txt: Text to be selected
        :param timeout: timeout in seconds
        :return: True if element selected in className, else return False
        """
        try:
            element = WebDriverWait(self.web_driver_global, timeout).until(
                EC.element_to_be_clickable((By.CLASS_NAME, className)))
            element = Select(self.web_driver_global.find_element_by_class_name(className))
            element.select_by_visible_text(txt)
            logging.info("select {} from {} is selected".format(txt, className))
        except NoSuchElementException:
            err = "element with class name {} not found".format(className)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def select_element_with_index(self, xpath, index, timeout=10):
        """
        This method is to select the text element in the xpath at the specified index
        :param xpath: xpath of the element
        :param index: index to be selected
        :param timeout: timeout in seconds
        :return: True if element selected in index, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = Select(self.web_driver_global.find_element_by_xpath(xpath))
            elem.select_by_index(index)
            logging.info("selected {} from {}".format(str(index), xpath))
        except NoSuchElementException:
            err = "element with xpath {} not found".format(xpath)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def is_element_xpath_selected(self, xpath, timeout=10):
        """
        This method is verify if the checkbox/ togle button element  is selected
        :param xpath: xpath of the element
        :param timeout: timeout in seconds
        :return: True if checkbox is selected , else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = self.web_driver_global.find_element_by_xpath(xpath)
            if elem.is_selected():
                logging.info("{} is checked/ selected".format(xpath))
                return True
            else:
                logging.info("{} is Unchecked/ unselected".format(xpath))
                return False
        except Exception as err:
            logging.error(err)
            return str(err)

    def Select_Checkbox_With_Xpath(self, xpath, timeout=10):
        """
        This method is Select/Check the checkbox
        :param xpath: xpath of the element
        :param timeout: timeout in seconds
        :return: True if checkbox is selected , else return False if unchecked
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = self.web_driver_global.find_element_by_xpath(xpath)
            if elem.is_selected():
                logging.info("{} is already checked".format(xpath))
                return True
            else:
                logging.info("{} is Unchecked".format(xpath))
                self.web_driver_global.execute_script('arguments[0].click()', elem)
                # elem.click()
                elem = self.web_driver_global.find_element_by_xpath(xpath)
                if elem.is_selected():
                    logging.info("{} is checked".format(xpath))
                    return True
                else:
                    logging.error("{} is not checked after select operation".format(xpath))
                    return False
        except Exception as err:
            logging.error(err)
            return False

    def Unselect_Checkbox_With_Xpath(self, xpath, timeout=10):
        """
        This method is to Unselect/ uncheck the checkbox
        :param xpath: xpath of the element
        :param timeout: timeout in seconds
        :return: True if checkbox is unselected/ unchecked , else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            elem = self.web_driver_global.find_element_by_xpath(xpath)
            if elem.is_selected():
                logging.info("{} is checked".format(xpath))
                self.web_driver_global.execute_script('arguments[0].click()', elem)
                # elem.click()
                if self.web_driver_global.find_element_by_xpath(xpath).is_selected():
                    logging.error("{} is still checked after unselect operation".format(xpath))
                    return False
                else:
                    logging.info("{} is  unchecked".format(xpath))
                    return True
            else:
                logging.info("{} is already unchecked".format(xpath))
                return True
        except Exception as err:
            logging.error(err)
            return False

    def switch_to_alert(self):
        """
        This method is to switch to Alert box
        :return: True if switched to alert box , else return False
        """
        try:
            logging.info("Inside alert")
            self.web_driver_global.switch_to.alert.accept()
            return True
        except TimeoutException:
            err = 'Given element is not displayed: '
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False

    def getText_ById(self, element_id, timeout=10):
        """
        This method is to get the text in the provided ID
        :param element_id: Element ID
        :param timeout: timeout in seconds
        :return: text value in the ID provided , else return False
        """
        try:
            myElem = WebDriverWait(self.web_driver_global, timeout).until(
                EC.presence_of_element_located((By.ID, element_id)))
            element = self.web_driver_global.find_element_by_id(element_id)
            logging.info("found text {} in ID {}".format(element.text, element_id))
            return element.text
        except Exception as err:
            logging.error(err)
            return False

    def keys_action(self, element, key):  ##add more logics to continuous key press and keyboard scenarios
        """
        This method uses key_down method to send a key press, without releasing it
        :param element: Element to be pressed without releasing. Example: Keys.CONTROL for control key press
        :param key: Key to be pressed after holding element
        :return: True if successful, else return False
        Example –
        One can use key_down method as an Action chain as below. This example clicks Ctrl+C after opening the webpage
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
        """
        try:
            actions = ActionChains(self.web_driver_global)
            actions.key_down(element).send_keys(key).key_up(element).perform()
            return True
        except Exception as err:
            logging.error(err)
            return False

    def hot_keys_action(self, element):  ##add more logics to continuous key press and keyboard scenarios
        """
        This method uses key_down , Key_up and send_keys method to send a key press, with or without releasing it
        :param element: Element to be pressed
        Example: Keys.CONTROL+c , Keys.CONTROL+Keys.ALT+Keys.DELETE, Keys.CONTROL+Keys.ESCAPE
        :return: True if successful, else return False
        Example –
        One can use key_down method as an Action chain as below. This example clicks Ctrl+C after opening the webpage
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
        """
        try:
            actions = ActionChains(self.web_driver_global)
            element = element.split('+')
            if len(element) == 1:
                actions.key_down(eval(element[0])).key_up(eval(element[0])).perform()
            elif len(element) == 2:
                actions.key_down(eval(element[0])).send_keys(eval(element[1])).key_up(eval(element[0])).perform()
            elif len(element) == 3:
                actions.key_down(eval(element[0])).key_down(eval(element[1])).send_keys(eval(element[2])) \
                    .key_up(eval(element[0])).key_up(eval(element[1])).perform()
            else:
                return False
            return True
        except Exception as err:
            logging.error(err)
            str_err = err
            if "no such window" or "No Such Window" in str_err:
                return True
            return False

    def double_click_xpath(self, xpath_element, timeout=10):
        """
        This method is used to double click on provided xpath
        :param xpath_element: xpath Element to be be double clicked
        :param timeout: timeout in seconds
        :return: True if successful, else return False
        """
        try:
            self.WaitForXpath(xpath_element, timeout)
            actionChains = ActionChains(self.web_driver_global)
            webelement = self.web_driver_global.find_element_by_xpath(xpath_element)
            logging.info("Double CLicking on element with xpath {}".format(xpath_element))
            actionChains.double_click(webelement).perform()
            return True
        except Exception as err:
            logging.error(err)
            return False

    def mouse_hover_on_xpath(self, xpath, timeout=10):
        """
        This method is used to Hover the mouse on mentioned element
        :param xpath: Element xpath to be be mouse hovered
        :param timeout: timeout in seconds
        :return: True if successful, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            logging.info("Hovering on element {}".format(xpath))
            action = ActionChains(self.web_driver_global)
            item = self.web_driver_global.find_element_by_xpath(xpath)
            hover = action.move_to_element(item)
            hover.perform()
            return True
        except Exception as err:
            logging.error(err)
            return False

    def set_attribute_on_xpath(self, xpath, attribute, timeout=10):
        """
        This method is used to Hover the mouse on mentioned element
        :param xpath: Element xpath to be be mouse hovered
        :param timeout: timeout in seconds
        :return: True if successful, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            logging.info("Setting Attribute on element {}".format(xpath))

            item = self.web_driver_global.find_element_by_xpath(xpath)
            self.web_driver_global.execute_script("arguments[0].setAttribute('style', arguments[1]);", item, attribute)
            return True
        except Exception as err:
            logging.error(err)
            return False

    def right_click_on_xpath(self, element_xpath, timeout=10):
        """
        This method is used to right click on mentioned element
        :param element_xpath: Element to be be right clicked
        :param timeout: timeout in seconds
        :return: True if successful, else return False
        """
        try:
            self.WaitForXpath(element_xpath, timeout)
            actionChains = ActionChains(self.web_driver_global)
            element = self.web_driver_global.find_element_by_xpath(element_xpath)
            actionChains.context_click(element).perform()

            return True
        except Exception as err:
            logging.error(err)
            return False

    def isWindowWithXpathClosed(self, xpath, timeout=10):
        """
        This method is used to check if the window is closed with mentioned xpath
        :param xpath: xpath element
        :param timeout: timeout in seconds
        :return: True if window closed, else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            self.web_driver_global.execute_script('arguments[0].click()', xpath)
            err = 'Window is not closed'
            logging.error(err)
            return err
        except Exception as err:
            logging.info("Window is closed")
            return True

    def maximize_browser_window(self):
        """
        This method is used to maximize the window
        :return:
        """
        try:
            self.web_driver_global.maximize_window()
            logging.info("Maximized the browser in control")
            return True
        except Exception as err:
            logging.error(err)
            return False

    def minimize_browser_window(self):
        """
        This method is used to minimize the  window
        :return:
        """
        try:
            self.web_driver_global.minimize_window()
            logging.info("Minimized the browser in control")
            return True
        except Exception as err:
            logging.error(err)
            return False

    def close_driver(self):
        """
        Thi method can be used to close the browser window that is active
        TBD: Add logic to make it more specific
        :return: True if successful , else return Error
        """
        try:
            self.web_driver_global.close()
            logging.info("Closed the browser in control")
            return True
        except Exception as err:
            logging.error(err)
            return False

    def close_window_with_xpath(self, xpath, timeout=10):
        """
        Thi method can be used to close the window based on xpath of window that is in control
        :param xpath: Element xpath
        :param timeout: timeout in seconds
        :return: True if window closed , else return False
        """
        try:
            status, window_handle = self.find_window_handle_by_xpath(xpath)
            if status == True:
                self.web_driver_global.close()
                logging.info("Closed the window with handle {} with xpath {}".format(window_handle, xpath))
                return True
            else:
                logging.info("Looks like window is already closed as window with xpath {} not found".format(xpath))
                return True
        except Exception as err:
            logging.error(err)
            return False

    def quitDriver(self):
        """
        This method could be used to empty the driver instance by quitting.
        Note: Need to recreate the driver instance if this method is used by calling the class
        :return:  true if successful, else return error
        """
        try:
            # global web_driver_global
            logging.info("Quit/ Cleared the  browser instance in control: '{}'".format(self.web_driver_global))
            self.web_driver_global.quit()
            # web_driver_global = None
            return True
        except Exception as err:
            logging.error(err)
            return False

    def getText_ByName(self, name, timeout=10):
        """
        This method is to get the text by element name
        :param name: Element name
        :param timeout: timeout in seconds
        :return: text value in the name provided , else return False
        """
        try:
            myElem = WebDriverWait(self.web_driver_global, timeout).until(
                EC.presence_of_element_located((By.NAME, name)))
            element = self.web_driver_global.find_element_by_name(name)
            logging.info("found text {} in name {}".format(element.text, name))
            return element.text
        except Exception as err:
            logging.error(err)
            return False

    def click_and_hold_handle(self, element):
        """
        This method is used to click and hold the mentioned element in xpath
        :param element: element to be clicked and holded
        :return: True if success, else return False
        """
        try:
            print("Element is located by xpath")
            slider = self.web_driver_global.find_element_by_xpath(element)
            actions = ActionChains(self.web_driver_global)
            actions.click_and_hold(slider).move_by_offset(10, 0).release().perform()
            return True
        except Exception as err:
            logging.error(err)
            return False

    def getTitle(self):
        """
        This method is used to get the title of the driver window active
        :return: Title , else False
        """
        try:
            logging.info("Driver Title is {}".format(self.web_driver_global.title))
            return self.web_driver_global.title
        except Exception as err:
            logging.error(err)
            return False

    def isDisplayed_By_XPath(self, xpath, timeout=10):
        """
        This method is used to verify if mentioned xpath element is displayed
        :param xpath: element xpath
        :param timeout: timeout in seconds
        :return: True if element displayed , else returns False
        """

        try:
            self.WaitForXpath(xpath, timeout)
            boolean = False
            ele = self.web_driver_global.find_element_by_xpath(xpath)
            if ele.is_displayed():
                logging.info("xpath Element {} is displayed".format(xpath))
                return True
            else:
                logging.info("xpath Element {} is not displayed".format(xpath))
                return False
        except Exception as err:
            logging.error(err)
            return False

    def isDisplayed_By_LinkText(self, link_text, timeout=10):
        """
        This method is used to verify if mentioned link text element is displayed
        :param link_text: element link_text
        :param timeout: timeout in seconds
        :return: True if element displayed , else returns False
        """
        try:
            self.WaitForLink(link_text, timeout)
            boolean = False
            ele = self.web_driver_global.find_element_by_link_text(link_text)
            if ele.is_displayed():
                logging.info("Link Text Element {} is displayed".format(link_text))
                return True
            else:
                logging.info("Link Text Element {} is not displayed".format(link_text))
                return False
        except Exception as err:
            logging.error(err)
            return False

    def find_window_handle_by_xpath(self, ele_xpath_to_find, timeout=10):
        """
            This method can be used to find correct window handle by xpath provided in a set of electron window handles
            :param ele_xpath_to_find: xpath element to find in available windows
            :param timeout: timeout in seconds
            return: Boolean True and window handle if success, else False with None Handle
        """
        logging.info("All Window Handles --> {}".format(self.web_driver_global.window_handles))
        for each_handle in self.web_driver_global.window_handles:
            self.web_driver_global.switch_to.window(each_handle)
            status = self.isDisplayed_By_XPath(ele_xpath_to_find, timeout)
            if status != True:
                # logging.error("Invalid handle {} as cannot find".format(each_handle))
                continue
            else:
                logging.info("Working handle is {} having xpath {}".format(each_handle, ele_xpath_to_find))
                logging.info("Driver Title --> {}".format(self.web_driver_global.title))
                return True, each_handle
        logging.error("No valid Window Handle found which has element with xpath--> {} ".format(ele_xpath_to_find))
        return False, None

    def switch_window_by_handle(self, window_handle):
        """
            This method can be used to switch to particular UI window by providing window handle
            :param window_handle: Window handle to switch for
            return: Boolean True if success, else False
        """
        logging.info("Input Window Handle is {}".format(window_handle))
        self.web_driver_global.switch_to.window(window_handle)
        return True

    def switch_window_by_handle_and_find_xpath(self, window_handle, ele_xpath_to_find, timeout=10):
        """
            This method can be used to switch to particular UI window by providing window handle and xpath to find
            :param window_handle: Window handle to switch for
            :param ele_xpath_to_find: element xpath to find after switching window handle
            :param timeout: timeout in seconds
            return: Boolean True if success, else False
        """
        logging.info("Input Window Handle is {}".format(window_handle))
        self.web_driver_global.switch_to.window(window_handle)
        status = self.isDisplayed_By_XPath(ele_xpath_to_find, timeout)
        if status != True:
            logging.error("Invalid window handle {} as cannot find xpath {}".format(window_handle, ele_xpath_to_find))
            return False
        else:
            logging.info("{} is a Valid handle. Found xpath {} in handle".format(window_handle, ele_xpath_to_find))
            logging.info("Driver Title --> {}".format(self.web_driver_global.title))
            return True

    def scroll_and_select_option_in_dropdown(self, ele_xpath, search_text, timeout=10):
        """
            This method is to select drop down by first clicking to the drop down and then select the option by text
            :param ele_xpath: ## xpath value to click on the drop down field
            :param search_text: ## provide the value to search text in the drop down list to click
            :param timeout: timeout in seconds
            return: Boolean True if success, else False
        """
        try:
            logging.info("Clicking on the drop down for given {}:{} element".format(search_text, ele_xpath))
            self.WaitForXpath(ele_xpath, timeout)
            self.click_element_by_xpath(ele_xpath)
            status = self.isDisplayed_By_XPath('//*[contains(text(),"' + search_text + '")]')
            if status:
                logging.info("{} option is visible in drop down".format(search_text))
                self.click_element_by_xpath('//*[contains(text(),"' + search_text + '")]')
                logging.info("{} value selected successfully from the dropdown".format(search_text))
                return True
            else:
                logging.error("{} option is not found in the visible drop down list".format(search_text))
                logging.info("Will be scrolling the list by pressing Down arrow key to bring text in drop down list")
                for i in range(0, 20):
                    self.EnterTextInXpath(ele_xpath, Keys.DOWN, clearText=False)
                    status = self.isDisplayed_By_XPath('//*[contains(text(),"' + search_text + '")]', timeout)
                    if status:
                        logging.info("{} option is visible in drop down".format(search_text))
                        self.click_element_by_xpath('//*[contains(text(),"' + search_text + '")]')
                        logging.info("{} value selected successfully from the dropdown".format(search_text))
                        return True
                    else:
                        logging.error(
                            "{} option is not found in the drop down list will be continuing for {}/20 iteration".format(
                                search_text, i))
                        continue
                return False
        except Exception as err:
            logging.error(err)
            return False

    def search_and_select_option_in_dropdown(self, ele_xpath, search_text, timeout=10):
        """
            This method is to select drop by first clicking to the drop down send key and the select the option by text
            :param ele_xpath: ## xpath value to click on the drop down field
            :param search_text: ## provide the value to search text in the drop down list to click
            :param timeout: timeout in seconds
            return: Boolean True if success, else False
        """
        try:
            logging.info("Clicking on the drop down for given {}:{} element".format(search_text, ele_xpath))
            self.WaitForXpath(ele_xpath, timeout)
            self.click_element_by_xpath(ele_xpath)
            self.EnterTextInXpath(ele_xpath, search_text, clearText=False)
            status = self.isDisplayed_By_XPath('//span[contains(text(),"' + search_text + '")]')
            if status:
                logging.info("{} option is visible in drop down".format(search_text))
                self.click_element_by_xpath('//span[contains(text(),"' + search_text + '")]')
                logging.info("{} value selected successfully from the dropdown".format(search_text))
                return True
            else:
                logging.error("{} option is not found in the drop down list".format(search_text))
                return False
        except Exception as err:
            logging.error(err)
            return False

    def navigate_to_back(self):
        """
            This method is only specific to back page
            return: Boolean True if success, else False
        """
        try:
            self.web_driver_global.back()
            logging.info("navigate to back page")
            return True
        except Exception as err:
            logging.error(err)
            return False

    def scroll_elem_into_view(self, element):  # Added by aaditya
        """
        This method scrolls till element appears into view
        params:
          element: xpath of element to be visible after scrolling
        """
        try:
            logging.info(f"Scrolling till element {element}")
            status = self.isDisplayed_By_XPath(element)
            if status:
                logging.info(f"{element} is displayed on web page")
                logging.info("Scrolling")
                my_element = self.web_driver_global.find_element_by_xpath(element)
                actions = ActionChains(self.web_driver_global)
                actions.move_to_element(my_element).perform()
                return True
            else:
                logging.error("{} element is not found ".format(element))
        except Exception as err:
            logging.error(err)
            return False

    def getcssvalue(self, xpath, timeout=5):
        """
        This method is to get color of the field in hexa decimal value
        :param name: Element name
        :param timeout: timeout in seconds
        :return: text value of color , else return False
        """
        try:
            self.WaitForXpath(xpath, timeout)
            element = self.web_driver_global.find_element_by_xpath(xpath)
            if element:
                logging.info("found text {} in xpath {}".format(element.text, xpath))
                element_color = self.GetXpathCssValue(xpath, 'border', timeout)
                logging.info("Color of the text is {} for element xpath {}".format(element_color, xpath))
                element_color = element_color.split("rgb")
                get_colorcode = "rgb" + element_color[1]
                element_color = Color.from_string(get_colorcode).hex
                return element_color
            else:
                return False
        except Exception as err:
            logging.error(err)
            return False

    def UploadfileInXpath(self, xpath, file):
        """
        This method is to enter text in the mentioned element xpath
        :param xpath: xpath when text has to be entered
        :param file: File details
        :return: True if text is entered, else return False
        """
        try:
            elem = self.web_driver_global.find_element_by_xpath(xpath)
            elem.send_keys(file)
            return True
        except TimeoutException:
            err = 'TIMED OUT: Given element is not displayed: {}'.format(xpath)
            logging.error(err)
            return False
        except Exception as err:
            logging.error(err)
            return False


if __name__ == "__main__":
    pass
