from selenium import webdriver
from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import json


class Selem:

    def __init__(self, host, driver_name, driver_config_path="configuration_files/webdriver.json"):
        """
        Constructor initializes driver connection to host
        :param host: Web url to initialize
        :param driver_name: Preferred driver for use i.e. Chrome
        """

        self.host = host
        self.driver_config_path = driver_config_path
        self.driver = self.read_driver_config(driver_name, driver_config_path)

    def __enter__(self):
        """
        Enter method for with call, will execute web driver
        :return: host read object by web driver
        """
        try:
            self.browser = webdriver.Chrome(self.driver)
        except WebDriverException:
            raise Exception('Error initializing class, web driver path does not exist')
        self.browser.get(self.host)
        self.browser.maximize_window()
        return self

    def __exit__(self, sel_type, sel_value, sel_traceback):
        """
        Close method for with call
        :param sel_type:
        :param sel_value:
        :param sel_traceback:
        """
        self.browser.close()

    @staticmethod
    def read_driver_config(config_driver_name, driver_config_path):
        """
        Reads config for installed driver paths
        :param config_driver_name:
        :param driver_config_path:
        :return: path for driver .exe file
        """
        with open(driver_config_path, 'r') as df:
            driver_config = json.load(df)
        config_driver_path = driver_config['Drivers'][config_driver_name]
        return config_driver_path

    def login(self, username, password):
        self.browser.find_element_by_id("usuario").send_keys(username)
        self.browser.find_element_by_id("clave").send_keys(password)
        sleep(3)
        self.browser.find_element_by_name("submit1").click()
        sleep(5)

    def get_source(self):
        """
        Gets page source from page in browser
        :return: page source code
        """
        source = self.browser.page_source
        return source

    def get_xpath(self, xpath):
        """
        Search xpath
        :return: list of elements for xpath
        """
        element_xpath = self.browser.find_elements_by_xpath(xpath)
        return element_xpath

    def get_link_text(self, text):
        """
        Search xpath
        :return: list of elements for xpath
        """
        element_link_text = self.browser.find_element_by_link_text(text)
        return element_link_text
