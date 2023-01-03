import sys
from behave import fixture
import logging
from Utils.common_selenium_utils import ServerWebSeleniumUtils
from Utils.common_server_steps import ExceptionFunction


def start_server_selen_obj(context, effective_tags):
    browser = context.config.userdata.get("browser", "chrome")
    if "browser.chrome" in effective_tags:
        try:
            server_selen_obj = ServerWebSeleniumUtils(working_browser="chrome")
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ExceptionFunction(err, exc_type, exc_obj, exc_tb)
            server_selen_obj = ServerWebSeleniumUtils(working_browser="chrome")
    else:
        try:
            server_selen_obj = ServerWebSeleniumUtils(working_browser=browser)
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ExceptionFunction(err, exc_type, exc_obj, exc_tb)
            server_selen_obj = ServerWebSeleniumUtils(working_browser=browser)
    context.server_selen_obj = server_selen_obj
