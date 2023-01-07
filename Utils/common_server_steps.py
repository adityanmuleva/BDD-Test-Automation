import json
import os, sys

sys.path.append(os.path.join((os.path.realpath(__file__).split("TestCases")[0])))
import time
import logging
from re import match
from Configurations import *
from behave import step, register_type
from TestCases.features.steps.environment_steps import *
from Configurations.webconfig import *
from Xpaths.operable_xpaths import *
import parse
from faker import Faker
import calendar
import time
import random


##Below logic helps the user to pass empty value in feature file
##https://stackoverflow.com/a/58947425

@parse.with_pattern(r'.*')
def parse_nullable_string(text):
    return text


register_type(NullableString=parse_nullable_string)


def ExceptionFunction(err, exc_type, exc_obj, exc_tb):
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    sys.stderr.write("ERRORED DESC\t::%s:\n" % str(err))
    sys.stderr.write("ERRORED MODULE\t::%s:\n" % str(exc_type))
    sys.stderr.write("ERRORED FILE\t::%s:\n" % str(fname))
    sys.stderr.write("ERRORED LINE\t::%s:\n" % str(exc_tb.tb_lineno))
    logging.error("ERRORED DESC\t::%s:\n" % str(err))
    logging.error("ERRORED MODULE\t::%s:\n" % str(exc_type))
    logging.error("ERRORED FILE\t::%s:\n" % str(fname))
    logging.error("ERRORED LINE\t::%s:\n" % str(exc_tb.tb_lineno))


@step(u'I open operable web Page')
def open_web_ui(context):
    """
    This Method opens the web ui in configured browser
    :param context: context of the run
    :param xpath:  Server URL xpath to validate after  server URL opens in browser
    :return True if pass, else Assert false
    """
    try:
        server_url = DOCTOR_CONFIG["SERVER_URL"]
        xpath = login_xpath["username_textbox"]
        logging.info("Input params for step: '{}'".format(xpath))
        context.server_selen_obj.maximize_browser_window()
        status = context.server_selen_obj.OpenURLAndVerifyXpathPresent(server_url, xpath)
        context.test_execution_data['"{}"  Server open status with xpath "{}" '.format(server_url, xpath)] = status
        if status == True:
            logging.info(" Server UI opened successfully with URL '{}'".format(server_url))
            print(" Server UI opened successfully with URL '{}'".format(server_url))
            return True
        else:
            assert False, " Server UI with URL '{}' couldn't be opened".format(server_url)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred".format(exc_type, exc_obj, exc_tb)


@step(u'I login to operable with username "{username}", password "{password}"')
def LoginServerUI(context, username, password):
    """
    This Method is to log in with username and password
    :param context: context of the run
    :return True if pass, else Assert false
    """
    try:
        logging.info("Input params for step: '{}', '{}'".format(username, password))
        status_1 = context.server_selen_obj.isDisplayed_By_XPath(login_xpath["username_textbox"])
        if status_1:
            context.server_selen_obj.EnterTextInXpath(login_xpath["username_textbox"], username)
            context.server_selen_obj.EnterTextInXpath(login_xpath["password_textbox"], password)
            context.server_selen_obj.click_element_by_xpath(login_xpath['signin_button'])
            context.server_selen_obj.CheckIfXpathExist(patient_list['patients_list_div'], 10)

        status = context.server_selen_obj.WaitForXpath(patient_list['patients_list_div'], 10)
        context.test_execution_data[
            " Server login status with username '{}', password '{}'".format(username, password)] = status
        if status == True:
            logging.info("Successfully logged into  Server UI with username '{}', password '{}'".format(username,
                                                                                                        password))
            print("Successfully logged into  Server UI with username '{}', password '{}'".format(username,
                                                                                                 password))
            return True

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred".format(exc_type, exc_obj, exc_tb)


@step(u'I Create Patient')
def LoginServerUI(context):
    """
    This Method is to log in with username and password
    :param context: context of the run
    :return True if pass, else Assert false
    """
    try:
        gmt = time.gmtime()
        ts = calendar.timegm(gmt)
        fake = Faker()
        username = fake.unique.first_name() + '_' + str(ts)
        lastname = fake.unique.last_name()
        gender = ["Male", "Female"]
        random.choice(gender)
        zip_code = random.randrange(10000, 99999)
        phone_number = random.randrange(900000000, 999999999)
        address = fake.address()

        status = context.server_selen_obj.CheckIfXpathExist(patient_list['patients_list_div'], 10)
        if status == True:
            context.server_selen_obj.WaitForXpath(patient_list['add_patient_button'], 10)
            context.server_selen_obj.click_element_by_xpath(patient_list['add_patient_button'])
            context.server_selen_obj.WaitForXpath(add_patient['firstname_textbox'], 10)
            context.server_selen_obj.EnterTextInXpath(add_patient["firstname_textbox"], username)
            context.server_selen_obj.EnterTextInXpath(add_patient["lastname_textbox"], lastname)
            # TODO :Date
            context.server_selen_obj.click_element_by_xpath(add_patient['gender_dropdown'])
            context.server_selen_obj.click_element_by_xpath(
                add_patient['gender_option'].replace('~', random.choice(gender)))
            context.server_selen_obj.EnterTextInXpath(add_patient["zipcode_textbox"], zip_code)
            context.server_selen_obj.EnterTextInXpath(add_patient["mobile_number_textbox"], phone_number)
            context.server_selen_obj.EnterTextInXpath(add_patient["address_textbox"], address)
            # context.server_selen_obj.click_element_by_xpath(add_patient['submit_button'])
            return True

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred".format(exc_type, exc_obj, exc_tb)


@step(u'I Navigate to "{tab_name}" tab with xpath "{tab_xpath}"')
def navigate_to_tab(context, tab_name, tab_xpath):
    """
    This Method is to navigate to a particular tab
    :param context: context of the run
    :param tab_name: tab  name that must be clicked or navigated
    :param tab_xpath: tab xpath
    :return True if pass, else Assert false
    """
    try:
        logging.info("Input params for step: '{}', '{}'".format(tab_name, tab_xpath))
        if ('context' in tab_xpath) or ("[" and "]" in tab_xpath):
            tab_xpath = eval(tab_xpath)
        result = context.server_selen_obj.click_element_by_xpath(tab_xpath)
        context.test_execution_data['Tab "{}" with xpath "{}" Navigation status'.format(tab_name,
                                                                                        tab_xpath)] = result
        if result:
            logging.info("Successfully Navigated to Tab '{}' with xpath {}".format(tab_name, tab_xpath))
            print("Successfully Navigated to Tab '{}' with xpath '{}'".format(tab_name, tab_xpath))
            return True
        else:
            assert False, "'{}' tab with xpath '{}' could not be located and clicked ".format(tab_name, tab_xpath)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I Click on "{element_name}" element with xpath "{element_xpath}"')
def ClickOnElement(context, element_name, element_xpath):
    """
    This Method is to click on any particular element in UI
    :param context: context of the run
    :param element_name: element name
    :param element_xpath: element xpath to be clicked
    :return True if pass, else Assert false
    """
    try:
        logging.info("Input params for step: '{}', '{}'".format(element_name, element_xpath))
        if (('context' in element_xpath) or ("[" and "]" in element_xpath)) and (not element_xpath.startswith('/')):
            element_xpath = eval(element_xpath)
        result = context.server_selen_obj.click_element_by_xpath(element_xpath)
        context.test_execution_data['Element "{}" with xpath "{}" Click status'.format(element_name,
                                                                                       element_xpath)] = result
        if result is True:
            logging.info("Successfully Clicked element '{}' with xpath '{}'".format(element_name, element_xpath))
            print("Successfully Clicked element '{}' with xpath '{}'".format(element_name, element_xpath))
            return True
        else:
            assert False, "'{}' element with xpath '{}' could not be located and clicked ".format(element_name,
                                                                                                  element_xpath)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I verify if "{field_name}" field with xpath "{field_xpath}" has "{exp_field_value:NullableString}" value')
def IsValueExistsInField(context, field_name, field_xpath, exp_field_value):
    """
    This method is to verify if the provided value exists in the mentioned field
    :param field_name: field name to verify
    :param field_xpath: xpath of the element
    :param exp_field_value: expected value to find in the provided xpath. Note: provide empty space to check empty value
    :return: True if successful, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}', '{}'".format(field_name, field_xpath, exp_field_value))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        if ('context' in exp_field_value) or ("[" and "]" in exp_field_value):
            exp_field_value = eval(exp_field_value)

        status = context.server_selen_obj.IsTextExistsInXpath(field_xpath, exp_field_value)
        context.test_execution_data['Field "{}" with xpath "{}" value found with text "{}"'.format(field_name,
                                                                                                   field_xpath,
                                                                                                   exp_field_value)] = status
        if status is True:
            logging.info("Expected Value '{}' found in field '{}' having xpath '{}'".format(exp_field_value, field_name,
                                                                                            field_xpath))
            print("Expected Value '{}' found in field '{}' having xpath '{}'".format(exp_field_value, field_name,
                                                                                     field_xpath))
            return True
        else:
            assert False, "Expected Value '{}' could not be found in field '{}' having xpath '{}'".format(
                exp_field_value,
                field_name, field_xpath)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I get value of field "{field_name}" with xpath "{field_xpath}" by "{ByTextOrValueOrAttribute}"')
def GetValueInField(context, field_name: str, field_xpath: str, ByTextOrValueOrAttribute: str):
    """
    This Method can be used to get value af any field with provided xpath
    :param context: context of the run
    :param field_name: field name whose value needs to be retrieved
    :param field_xpath: field xpath whose value needs to be fetched
    :param ByTextOrValueOrAttribute:
                        Mention 'text' for fetching value by elem.text
                        Mention 'value' for fetching by get_attribute('value')
                        Mention correct 'attribute:attribute_name' for fetching by get_attribute(attribute)
    :return: Element text found if successful, else return err/ exception
    """
    try:
        logging.info(
            "Input params for step: '{}', '{}', '{}'".format(field_name, field_xpath, ByTextOrValueOrAttribute))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        if ByTextOrValueOrAttribute.casefold() == "text":
            field_text = context.server_selen_obj.getText_In_Xpath(field_xpath)
        elif ByTextOrValueOrAttribute.casefold() == "value":
            field_text = context.server_selen_obj.GetAttributeTextValueInXpath(field_xpath)
        elif "attribute:" in ByTextOrValueOrAttribute.casefold():
            field_text = context.server_selen_obj.GetValueofAttributeInXpath(field_xpath,
                                                                             ByTextOrValueOrAttribute.split(":")[-1])
        else:
            assert False, "Incorrect ByTextOrValueAttribute '{}' value provided. Mention 'text' for fetching value by " \
                          "elem.text or Mention 'value' for fetching by get_attribute('value') or Mention correct " \
                          "'attribute:attribute_name' for fetching by get_attribute(attribute)".format(
                ByTextOrValueOrAttribute)
        context.field_text = field_text
        context.test_execution_data['"{}" field name with xpath "{}" value by "{}"'.format(field_name, field_xpath,
                                                                                           ByTextOrValueOrAttribute)] = field_text
        if field_text is not False:
            logging.info(
                "Value '{}' found by '{}' in field '{}' having xpath '{}'".format(field_text, ByTextOrValueOrAttribute,
                                                                                  field_name, field_xpath))
            print(
                "Value '{}' found by '{}' in field '{}' having xpath '{}'".format(field_text, ByTextOrValueOrAttribute,
                                                                                  field_name, field_xpath))
            return field_text
        else:
            assert False, "Value could not be found by '{}' in field '{}' having xpath '{}'. FOund : '{}'".format(
                ByTextOrValueOrAttribute, field_name, field_xpath, field_text)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(
    u' I get value of field "{field_name}" with xpath "{field_xpath}" by "{ByTextOrValueOrAttribute}" and verify "{exp_field_value:NullableString}" presence')
def GetValueInFieldAndVerifyValue(context, field_name: str, field_xpath: str, ByTextOrValueOrAttribute: str,
                                  exp_field_value: str):
    """
    This Method can be used to get value af any field with provided xpath and verify if it is the same expected value
    :param context: context of the run
    :param field_name: field name whose value needs to be retrieved
    :param field_xpath: field xpath whose value needs to be fetched
    :param ByTextOrValueOrAttribute:
                        Mention 'text' for fetching value by elem.text
                        Mention 'value' for fetching by get_attribute('value')
                        Mention correct 'attribute:attribute_name' for fetching by get_attribute(attribute)
    :param exp_field_value: Value expected in the mentioned attribute
    :return: True if found same value as expected, else return err/ exception
    """
    try:
        logging.info(
            "Input params for step: '{}', '{}', '{}', '{}'".format(field_name, field_xpath, ByTextOrValueOrAttribute,
                                                                   exp_field_value))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        if ('context' in exp_field_value) or ("[" and "]" in exp_field_value):
            exp_field_value = eval(exp_field_value)

        if ByTextOrValueOrAttribute.casefold() == "text":
            field_text = context.server_selen_obj.getText_In_Xpath(field_xpath)
        elif ByTextOrValueOrAttribute.casefold() == "value":
            field_text = context.server_selen_obj.GetAttributeTextValueInXpath(field_xpath)
        elif "attribute:" in ByTextOrValueOrAttribute.casefold():
            field_text = context.server_selen_obj.GetValueofAttributeInXpath(field_xpath,
                                                                             ByTextOrValueOrAttribute.split(":")[-1])
        else:
            assert False, "Incorrect ByTextOrValueAttribute '{}' value provided. Mention 'text' for fetching value by " \
                          "elem.text or Mention 'value' for fetching by get_attribute('value') or Mention correct " \
                          "'attribute:attribute_name' for fetching by get_attribute(attribute)".format(
                ByTextOrValueOrAttribute)
        context.field_text = field_text
        context.test_execution_data['"{}" field name with xpath "{}" value by "{}"'.format(field_name, field_xpath,
                                                                                           ByTextOrValueOrAttribute)] = field_text
        if field_text is not False:
            logging.info(
                "Value '{}' found by '{}' in field '{}' having xpath '{}'".format(field_text, ByTextOrValueOrAttribute,
                                                                                  field_name, field_xpath))
            print(
                "Value '{}' found by '{}' in field '{}' having xpath '{}'".format(field_text, ByTextOrValueOrAttribute,
                                                                                  field_name, field_xpath))
            if field_text == exp_field_value:
                logging.info(
                    "Expected Value '{}' found in field '{}' having xpath '{}' found by '{}'".format(exp_field_value,
                                                                                                     field_name,
                                                                                                     field_xpath,
                                                                                                     ByTextOrValueOrAttribute))
                print("Expected Value '{}' found in field '{}' having xpath '{}' found by '{}'".format(exp_field_value,
                                                                                                       field_name,
                                                                                                       field_xpath,
                                                                                                       ByTextOrValueOrAttribute))
                return True
            else:
                assert False, "Expected Value '{}' could not be found in field '{}' having xpath '{}' found by '{}'. Actual found '{}'".format(
                    exp_field_value, field_name, field_xpath, ByTextOrValueOrAttribute, field_text)

        else:
            assert False, "Value could not be found by '{}' in field '{}' having xpath '{}'. Found : '{}'".format(
                ByTextOrValueOrAttribute, field_name, field_xpath, field_text)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I check if field "{field_name}" with xpath "{field_xpath}" is "{Exists_NotExists}"')
def VerifyifGivenFieldExistsOrNot(context, field_name, field_xpath, Exists_NotExists):
    """
    This Method can be used to verify if mentioned field exists or doesnt exists based on input expectation
    :param context: context of the run
    :param field_name: field name
    :param field_xpath: field xpath
    :param Exists_NotExists: value could be "Exists" or "NotExists"
    :return: True if successful, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}', '{}'".format(field_name, field_xpath, Exists_NotExists))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        status = context.server_selen_obj.CheckIfXpathExist(field_xpath)
        context.test_execution_data['"{}" field name with xpath "{}" Existance'.format(field_name,
                                                                                       field_xpath)] = status
        if Exists_NotExists.casefold() == "Exists".casefold():
            if status is True:
                logging.info("Field '{}' having xpath '{}' found as expected".format(field_name, field_xpath))
                print("Field '{}' having xpath '{}' found as expected".format(field_name, field_xpath))
                return True
            else:
                assert False, "Field '{}' having xpath '{}' not found. Expected to be found".format(field_name,
                                                                                                    field_xpath)
        elif Exists_NotExists.casefold() == "NotExists".casefold():
            if status is False:
                logging.info("Field '{}' having xpath '{}' not found as expected".format(field_name, field_xpath))
                print("Field '{}' having xpath '{}' not found as expected".format(field_name, field_xpath))
                return True
            else:
                assert False, "Field '{}' having xpath '{}' is found.Expected to be not found".format(field_name,
                                                                                                      field_xpath)
        else:
            assert False, "Incorrect ExistsNotExists '{}' value provided. Provide 'Exists' or 'NotExists' as the " \
                          "value".format(Exists_NotExists)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I verify if field "{field_name}" with xpath "{field_xpath}" is "{enabled_disabled}"')
def VerifyifGivenFieldEnabledOrNot(context, field_name, field_xpath, enabled_disabled):
    """
    This Method can be used to verify if mentioned field is enabled or disabled
    :param context: context of the run
    :param field_name: field name
    :param field_xpath: field xpath
    :param enabled_disabled: value could be "Enabled" or "Disabled"
    :return: True if successful, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}', '{}'".format(field_name, field_xpath, enabled_disabled))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        status = context.server_selen_obj.isXpathEnabled(field_xpath)
        context.test_execution_data['"{}" field name with xpath "{}" Enabled'.format(field_name,
                                                                                     field_xpath)] = status
        if enabled_disabled.casefold() == "Enabled".casefold():
            if status is True:
                logging.info("Field '{}' having xpath '{}' is Enabled as Expected".format(field_name, field_xpath))
                print("Field '{}' having xpath '{}' is Enabled as Expected".format(field_name, field_xpath))
                return True
            else:
                assert False, "Field '{}' having xpath '{}' is not Enabled. Expected to be Enabled".format(field_name,
                                                                                                           field_xpath)
        elif enabled_disabled.casefold() == "Disabled".casefold():
            if status is False:
                logging.info("Field '{}' having xpath '{}' is Disabled as Expected".format(field_name, field_xpath))
                print("Field '{}' having xpath '{}' is Disabled as Expected".format(field_name, field_xpath))
                return True
            else:
                assert False, "Field '{}' having xpath '{}' is not Disabled. Expected to be Disabled".format(field_name,
                                                                                                             field_xpath)
        else:
            assert False, "Incorrect enabled_disabled '{}' value provided. Provide 'Enabled' or 'Disabled' as the " \
                          "value".format(enabled_disabled)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(
    u' I explicitly wait for "{seconds}" seconds for field "{field_name}" with xpath "{field_xpath}" to appear or clickable')
def WaitForFieldToAppearOrClickable(context, seconds, field_name, field_xpath):
    """
    This Method can be used to Wait for mentioned seconds for field to appear/ clickable
    :param context: context of the run
    :param seconds: seconds to wait for element xpath
    :param field_name: field name
    :param field_xpath: field xpath
    :return: True if successful, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}', '{}'".format(seconds, field_name, field_xpath))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        status = context.server_selen_obj.WaitForXpath(field_xpath, int(seconds))
        context.test_execution_data['"{}" field name with xpath "{}" Found within "{}" seconds'.format(field_name,
                                                                                                       field_xpath,
                                                                                                       seconds)] = status
        if status is True:
            logging.info(
                "Field '{}' having xpath '{}' is found within '{}' seconds".format(field_name, field_xpath, seconds))
            print("Field '{}' having xpath '{}' is found within '{}' seconds".format(field_name, field_xpath, seconds))
            return True
        else:
            assert False, "Field '{}' having xpath '{}' is not found in '{}' seconds".format(field_name, field_xpath,
                                                                                             seconds)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u' I explicitly wait for "{seconds}" seconds for field "{field_name}" with xpath "{field_xpath}" to disappear')
def WaitForFieldToDisappear(context, seconds, field_name, field_xpath):
    """
    This Method can be used to explicitly Wait for mentioned seconds for field to disappear
    :param context: context of the run
    :param seconds: seconds to wait for element xpath to dispappear
    :param field_name: field name
    :param field_xpath: field xpath
    :return: True if successful, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}', '{}'".format(seconds, field_name, field_xpath))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        status = context.server_selen_obj.WaitForXpathtoDisappear(field_xpath, int(seconds))
        context.test_execution_data['"{}" field name with xpath "{}" disappeared within "{}" seconds'.format(field_name,
                                                                                                             field_xpath,
                                                                                                             seconds)] = status
        if status is True:
            logging.info("Field '{}' having xpath '{}' is not found as expected within '{}' seconds".format(field_name,
                                                                                                            field_xpath,
                                                                                                            seconds))
            print("Field '{}' having xpath '{}' is not found as expected within '{}' seconds".format(field_name,
                                                                                                     field_xpath,
                                                                                                     seconds))
            return True
        else:
            assert False, "Field '{}' having xpath '{}' is found even after '{}' seconds. Expected to disappear".format(
                field_name, field_xpath, seconds)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I enter text "{text:NullableString}" in field "{field_name}" with xpath "{field_xpath}"')
def EnterTextInField(context, text, field_name, field_xpath):
    """
    This Method can be used to Enter Text in the field mentioned by xpath
    :param context: context of the run
    :param text: text to be entered in the mentioned xpath
    :param field_name: field name
    :param field_xpath: field xpath
    :return: True if successful, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}', '{}'".format(text, field_name, field_xpath))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        if ('context' in text) or ("[" and "]" in text):
            text = eval(text)
        status = context.server_selen_obj.EnterTextInXpath(field_xpath, text, clearText=True)
        context.test_execution_data['"{}" field name with xpath "{}" has "{}" text entered'.format(field_name,
                                                                                                   field_xpath,
                                                                                                   text)] = status
        if status is True:
            logging.info(
                "Successfully entered text '{}' in Field '{}' having xpath '{}'".format(text, field_name, field_xpath))
            print(
                "Successfully entered text '{}' in Field '{}' having xpath '{}'".format(text, field_name, field_xpath))
            return True
        else:
            assert False, "Couldn't enter text '{}' in Field '{}' having xpath '{}'".format(text, field_name,
                                                                                            field_xpath)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I clear text in field "{field_name}" with xpath "{field_xpath}"')
def ClearTextInField(context, field_name, field_xpath):
    """
    This Method can be used to Clear Text in the field mentioned by xpath
    :param context: context of the run
    :param field_name: field name
    :param field_xpath: field xpath
    :return: True if successful, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}'".format(field_name, field_xpath))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        status = context.server_selen_obj.ClearTextInXpath(field_xpath)
        context.test_execution_data['"{}" field name with xpath "{}" text cleared'.format(field_name,
                                                                                          field_xpath)] = status
        if status is True:
            logging.info("Successfully cleared text in Field '{}' having xpath '{}'".format(field_name, field_xpath))
            print("Successfully cleared text in Field '{}' having xpath '{}'".format(field_name, field_xpath))
            return True
        else:
            assert False, "Couldn't clear text in Field '{}' having xpath '{}'".format(field_name, field_xpath)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I verify if field "{field_name}" checkbox with xpath "{field_xpath}" is "{checked_unchecked}"')
def VerifyifGivenCheckboxSelectedOrNot(context, field_name, field_xpath, checked_unchecked):
    """
    This Method can be used to verify if mentioned checkbox is checked or unchecked
    :param context: context of the run
    :param field_name: field name
    :param field_xpath: field xpath
    :param checked_unchecked: value could be "Checked" or "Unchecked"
    :return: True if successful, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}', '{}'".format(field_name, field_xpath, checked_unchecked))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        status = context.server_selen_obj.is_element_xpath_selected(field_xpath)
        context.test_execution_data['"{}" field name with xpath "{}" Checked/ Selected'.format(field_name,
                                                                                               field_xpath)] = status
        if checked_unchecked.casefold() == "Checked".casefold():
            if status is True:
                logging.info(
                    "Checkbox Field '{}' having xpath '{}' is Checked as Expected".format(field_name, field_xpath))
                print("Checkbox Field '{}' having xpath '{}' is Checked as Expected".format(field_name, field_xpath))
                return True
            else:
                assert False, "Checkbox Field '{}' having xpath '{}' is not Enabled. Expected to be Enabled".format(
                    field_name,
                    field_xpath)
        elif checked_unchecked.casefold() == "Unchecked".casefold():
            if status is False:
                logging.info(
                    "Checkbox Field '{}' having xpath '{}' is Unchecked as Expected".format(field_name, field_xpath))
                print("Checkbox Field '{}' having xpath '{}' is Unchecked as Expected".format(field_name, field_xpath))
                return True
            else:
                assert False, "Checkbox Field '{}' having xpath '{}' is not Unchecked. Expected to be Unchecked".format(
                    field_name,
                    field_xpath)
        else:
            assert False, "Incorrect checked_unchecked '{}' value provided. Provide 'Checked' or 'Unchecked' as the " \
                          "value".format(checked_unchecked)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I "{select_unselect}" checkbox field "{field_name}" with xpath "{field_xpath}"')
def SelectOrUnselctCheckbox(context, select_unselect, field_name, field_xpath):
    """
    This Method can be used to select or unselect checkbox
    :param context: context of the run
    :param select_unselect: value could be "select" or "unselect"
    :param field_name: field name
    :param field_xpath: field xpath
    :return: True if successful, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}', '{}'".format(select_unselect, field_name, field_xpath))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        if select_unselect.casefold() == "Select".casefold():
            status = context.server_selen_obj.Select_Checkbox_With_Xpath(field_xpath)
            context.test_execution_data['"{}" field name with xpath "{}" Checked/ Selected'.format(field_name,
                                                                                                   field_xpath)] = status
            if status is True:
                logging.info("Checkbox Field '{}' having xpath '{}' is Checked".format(field_name, field_xpath))
                print("Checkbox Field '{}' having xpath '{}' is Checked".format(field_name, field_xpath))
                return True
            else:
                assert False, "Checkbox Field '{}' having xpath '{}' is not Checked.".format(field_name, field_xpath)
        elif select_unselect.casefold() == "Unselect".casefold():
            status = context.server_selen_obj.Unselect_Checkbox_With_Xpath(field_xpath)
            context.test_execution_data['"{}" field name with xpath "{}" is Unchecked/ UnSelected'.format(field_name,
                                                                                                          field_xpath)] = status
            if status is True:
                logging.info("Checkbox Field '{}' having xpath '{}' is Unchecked".format(field_name, field_xpath))
                print("Checkbox Field '{}' having xpath '{}' is Unchecked".format(field_name, field_xpath))
                return True
            else:
                assert False, "Checkbox Field '{}' having xpath '{}' is not Unchecked".format(field_name, field_xpath)
        else:
            assert False, "Incorrect select_unselect '{}' value provided. Provide 'Select' or 'Unselect' as the " \
                          "value".format(select_unselect)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I Double Click on "{element_name}" element with xpath "{element_xpath}"')
def DoubleClickOnElement(context, element_name, element_xpath):
    """
    This Method is to double click on any particular element in UI
    :param context: context of the run
    :param element_name: element name
    :param element_xpath: element xpath to be double clicked
    :return True if pass, else Assert false
    """
    try:
        logging.info("Input params for step: '{}', '{}'".format(element_name, element_xpath))
        if ('context' in element_xpath) or ("[" and "]" in element_xpath):
            element_xpath = eval(element_xpath)
        result = context.server_selen_obj.double_click_xpath(element_xpath)
        context.test_execution_data['Element "{}" with xpath "{}" Double Click status'.format(element_name,
                                                                                              element_xpath)] = result
        if result is True:
            logging.info("Successfully Double Clicked element '{}' with xpath '{}'".format(element_name, element_xpath))
            print("Successfully Double Clicked element '{}' with xpath '{}'".format(element_name, element_xpath))
            return True
        else:
            assert False, "'{}' element with xpath '{}' could not be located and Double clicked ".format(element_name,
                                                                                                         element_xpath)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I Hover Mouse on "{element_name}" element with xpath "{element_xpath}"')
def HoverMouseOnElement(context, element_name, element_xpath):
    """
    This Method is to Hover Mouse on any particular element in UI
    :param context: context of the run
    :param element_name: element name
    :param element_xpath: element xpath to be mouse hovered
    :return True if pass, else Assert false
    """
    try:
        logging.info("Input params for step: '{}', '{}'".format(element_name, element_xpath))
        if ('context' in element_xpath) or ("[" and "]" in element_xpath):
            element_xpath = eval(element_xpath)
        result = context.server_selen_obj.mouse_hover_on_xpath(element_xpath)
        context.test_execution_data['Element "{}" with xpath "{}" Mouse Hover status'.format(element_name,
                                                                                             element_xpath)] = result
        if result is True:
            logging.info(
                "Successfully Hovered mouse on element '{}' with xpath '{}'".format(element_name, element_xpath))
            print("Successfully Hovered mouse on element '{}' with xpath '{}'".format(element_name, element_xpath))
            return True
        else:
            assert False, "'{}' element with xpath '{}' could not be Hovered with mouse ".format(element_name,
                                                                                                 element_xpath)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I Right click on "{element_name}" element with xpath "{element_xpath}"')
def RightClickOnElement(context, element_name, element_xpath):
    """
    This Method is to Right Click on any particular element in UI
    :param context: context of the run
    :param element_name: element name
    :param element_xpath: element xpath to be right clicked
    :return True if pass, else Assert false
    """
    try:
        logging.info("Input params for step: '{}', '{}'".format(element_name, element_xpath))
        if ('context' in element_xpath) or ("[" and "]" in element_xpath):
            element_xpath = eval(element_xpath)
        result = context.server_selen_obj.right_click_on_xpath(element_xpath)
        context.test_execution_data['Element "{}" with xpath "{}" Right Click status'.format(element_name,
                                                                                             element_xpath)] = result
        if result is True:
            logging.info(
                "Successfully Right Clicked on element '{}' with xpath '{}'".format(element_name, element_xpath))
            print("Successfully Right Clicked on element '{}' with xpath '{}'".format(element_name, element_xpath))
            return True
        else:
            assert False, "'{}' element with xpath '{}' could not be Right Clicked".format(element_name,
                                                                                           element_xpath)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I Verify if "{field_name}" element with xpath "{field_xpath}" window is "{closed_open}"')
def VerifyWindowIsClosed(context, field_name, field_xpath, closed_open):
    """
    This Method can be used to verify if mentioned element window is closed or not closed
    :param context: context of the run
    :param field_name: Element field name
    :param field_xpath: field xpath
    :param closed_open: value could be "closed" or "open"
    :return: True if successful, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}', '{}'".format(field_name, field_xpath, closed_open))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        status = context.server_selen_obj.isWindowWithXpathClosed(field_xpath)
        context.test_execution_data['"{}" field name with xpath "{}" Window is Closed'.format(field_name,
                                                                                              field_xpath)] = status
        if closed_open.casefold() == "closed".casefold():
            if status is True:
                logging.info("Field '{}' having xpath '{}' is closed as Expected".format(field_name, field_xpath))
                print("Field '{}' having xpath '{}' is Closed as Expected".format(field_name, field_xpath))
                return True
            else:
                assert False, "Field '{}' having xpath '{}' is Open. Expected to be Closed".format(field_name,
                                                                                                   field_xpath)
        elif closed_open.casefold() == "open".casefold():
            if status is False:
                logging.info("Field '{}' having xpath '{}' is open as Expected".format(field_name, field_xpath))
                print("Field '{}' having xpath '{}' is open as Expected".format(field_name, field_xpath))
                return True
            else:
                assert False, "Field '{}' having xpath '{}' is closed. Expected to be Open".format(field_name,
                                                                                                   field_xpath)
        else:
            assert False, "Incorrect closed_open '{}' value provided. Provide 'closed' or 'open' as the " \
                          "value".format(closed_open)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I Close "{window_name}" window having xpath "{element_xpath}"')
def CloseWindowWithXPath(context, window_name, element_xpath):
    """
    This Method is to Close any UI window with mentioned xpath present in the window
    :param context: context of the run
    :param window_name: Window name that has to be closed
    :param element_xpath: element xpath to be searched in window
    :return True if pass, else Assert false
    """
    try:
        logging.info("Input params for step: '{}', '{}'".format(window_name, element_xpath))
        if ('context' in element_xpath) or ("[" and "]" in element_xpath):
            element_xpath = eval(element_xpath)
        result = context.server_selen_obj.close_window_with_xpath(element_xpath)
        context.test_execution_data['Window "{}" with xpath "{}" Closed status'.format(window_name,
                                                                                       element_xpath)] = result
        if result is True:
            logging.info("Successfully Closed Window '{}' with xpath '{}'".format(window_name, element_xpath))
            print("Successfully Closed Window '{}' with xpath '{}'".format(window_name, element_xpath))
            return True
        else:
            assert False, "'{}' window with xpath '{}' could not be closed".format(window_name, element_xpath)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I confirm if field "{field_name}" with xpath "{field_xpath}" is "{displayed_notdisplayed}"')
def VerifyifGivenFieldDisplayedOrNot(context, field_name, field_xpath, displayed_notdisplayed):
    """
    This Method can be used to verify if mentioned field is displayed or not displayed
    :param context: context of the run
    :param field_name: field name
    :param field_xpath: field xpath
    :param displayed_notdisplayed: value could be "displayed" or "not_displayed"
    :return: True if successful, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}', '{}'".format(field_name, field_xpath, displayed_notdisplayed))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        status = context.server_selen_obj.isDisplayed_By_XPath(field_xpath)
        context.test_execution_data['"{}" field name with xpath "{}" is Displayed'.format(field_name,
                                                                                          field_xpath)] = status
        if displayed_notdisplayed.casefold() == "displayed".casefold():
            if status is True:
                logging.info("Field '{}' having xpath '{}' is displayed as Expected".format(field_name, field_xpath))
                print("Field '{}' having xpath '{}' is displayed as Expected".format(field_name, field_xpath))
                return True
            else:
                assert False, "Field '{}' having xpath '{}' is not displayed. Expected to be displayed".format(
                    field_name,
                    field_xpath)
        elif displayed_notdisplayed.casefold() == "not_displayed".casefold():
            if status is False:
                logging.info(
                    "Field '{}' having xpath '{}' is not displayed as Expected".format(field_name, field_xpath))
                print("Field '{}' having xpath '{}' is not displayed as Expected".format(field_name, field_xpath))
                return True
            else:
                assert False, "Field '{}' having xpath '{}' is displayed. Expected to be not displayed".format(
                    field_name,
                    field_xpath)
        else:
            assert False, "Incorrect displayed_notdisplayed '{}' value provided. Provide 'displayed' or 'not_displayed' as the " \
                          "value".format(displayed_notdisplayed)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred".format(exc_type, exc_obj, exc_tb)


@step(u'I navigate to window "{window_name}" with xpath "{field_xpath}"')
def FindOpenWindowByXpath(context, window_name: str, field_xpath: str):
    """
    This Method can be used to find any open window with provided xpath
    :param context: context of the run
    :param window_name: window name which must be found
    :param field_xpath: field xpath whose value needs to be searched in window
    :return: Window Handle if successful, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}'".format(window_name, field_xpath))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        status, driver_window_handle = context.server_selen_obj.find_window_handle_by_xpath(field_xpath)
        context.driver_window_handle = driver_window_handle
        context.test_execution_data['{} window with xpath "{}" found'.format(window_name, field_xpath)] = status
        if status is True:
            logging.info("Window '{}' found having xpath '{}' with handle '{}'".format(window_name, field_xpath,
                                                                                       driver_window_handle))
            print("Window '{}' found having xpath '{}' with handle '{}'".format(window_name, field_xpath,
                                                                                driver_window_handle))
            return driver_window_handle
        else:
            assert False, "could not find value window '{}' having xpath '{}'. Window Handle: '{}'".format(window_name,
                                                                                                           field_xpath,
                                                                                                           driver_window_handle)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I select dropdown value with "{text}" option by scrolling in field "{field_name}" with xpath "{field_xpath}"')
def ScrollAnd_SelectOption_InDropdown(context, text, field_name, field_xpath):
    """
    This Method can be used to Scroll down a dropdown and search for mentioned option text and select
    :param context: context of the run
    :param text: text to be searched in the mentioned xpath by scrolling
    :param field_name: field name
    :param field_xpath: field xpath
    :return: True if successful, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}', '{}'".format(text, field_name, field_xpath))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        status = context.server_selen_obj.scroll_and_select_option_in_dropdown(field_xpath, text)
        context.test_execution_data['"{}" field name with xpath "{}" has "{}" option selected'.format(field_name,
                                                                                                      field_xpath,
                                                                                                      text)] = status
        if status is True:
            logging.info("Successfully selected '{}' option in Field '{}' having xpath '{}'".format(text, field_name,
                                                                                                    field_xpath))
            print("Successfully selected '{}' option in Field '{}' having xpath '{}'".format(text, field_name,
                                                                                             field_xpath))
            return True
        else:
            assert False, "Couldn't select/ find '{}' option in Field '{}' having xpath '{}'".format(text, field_name,
                                                                                                     field_xpath)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I select dropdown value by searching "{text}" option in field "{field_name}" with xpath "{field_xpath}"')
def Search_And_SelectOption_InDropdown(context, text, field_name, field_xpath):
    """
    This Method can be used to search for mentioned option text in the mentioned field
    :param context: context of the run
    :param text: text to be searched in the mentioned xpath by searching
    :param field_name: field name
    :param field_xpath: field xpath
    :return: True if successful, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}', '{}'".format(text, field_name, field_xpath))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        status = context.server_selen_obj.search_and_select_option_in_dropdown(field_xpath, text)
        context.test_execution_data['"{}" field name with xpath "{}" has "{}" option selected'.format(field_name,
                                                                                                      field_xpath,
                                                                                                      text)] = status
        if status is True:
            logging.info("Successfully selected '{}' option in Field '{}' having xpath '{}'".format(text, field_name,
                                                                                                    field_xpath))
            print("Successfully selected '{}' option in Field '{}' having xpath '{}'".format(text, field_name,
                                                                                             field_xpath))
            return True
        else:
            assert False, "Couldn't select/ find '{}' option in Field '{}' having xpath '{}'".format(text, field_name,
                                                                                                     field_xpath)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u" I read '{input_xpaths}' and validate with expected '{tooltips_values}' content")
def validate_tooltips(context, input_xpaths, tooltips_values):
    """
    This method is to validate the tooltips of any section by passing list of xpath and tooltips at the same time
    :param input_xpaths: <xpath> <list> list of xpaths for fetch the tool tip value
    :param tooltips_values: <list> list of expected tool tips values
    """
    try:
        if ('context' in input_xpaths) or ("[" and "]" in input_xpaths):
            input_xpaths = eval(input_xpaths)
        if ('context' in tooltips_values) or ("[" and "]" in tooltips_values):
            tooltips_values = eval(tooltips_values)

        logging.info("input xpaths list :{}".format(input_xpaths))
        logging.info("tooltips values list :{}".format(tooltips_values))
        actual_tooltip_values_list = []

        for ele_xpath in input_xpaths:
            logging.info("fetched xpath :{}".format(ele_xpath))
            context.server_selen_obj.mouse_hover_on_xpath(ele_xpath)  # mouse hover on //img tag
            logging.info(
                "actual value: {} ".format(context.server_selen_obj.getText_In_Xpath(ele_xpath + "//..//span")))
            actual_tooltip_values_list.append(
                context.server_selen_obj.getText_In_Xpath(ele_xpath + "//..//span"))  # text_tag
        mapper = zip(actual_tooltip_values_list, tooltips_values)
        mapper = list(mapper)
        logging.info("validate tooltips values :{}".format(mapper))
        for result in mapper:
            logging.info(f"{result} for mapper")
            if not result[0] == result[1]:  # compare tooltips values
                raise ValueError("Unable to match actual :{} expected: {}  ".format(result[0], result[1]))
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "{}:{}:{} occurred while performing the click action ".format(exc_type, exc_obj, exc_tb)


@step(u" I scroll down till element '{element_name}' having xpath '{ele_xpath}' is visible")
def scroll_till_element(context, element_name, ele_xpath):
    """
    This method is for scrolling till element
    params:
        element_name: target element name to scroll
        ele_xpath: target element xpath to scroll
    """
    try:
        logging.info("Input params for step: '{}', '{}'".format(element_name, ele_xpath))
        if ('context' in ele_xpath) or ("[" and "]" in ele_xpath):
            ele_xpath = eval(ele_xpath)
        logging.info("scrolling till element {} with xpath :{}".format(element_name, ele_xpath))
        status = context.server_selen_obj.scroll_elem_into_view(ele_xpath)
        context.test_execution_data[f"Scrolling {element_name} having xpath {ele_xpath}"] = status
        if status is True:
            logging.info("Successfully scrolled till '{}' having xpath '{}'".format(element_name, ele_xpath))
            print("Successfully scrolled till '{}' having xpath '{}'".format(element_name, ele_xpath))
            return True
        else:
            assert False, "Couldn't Successfully scroll till '{}' having xpath '{}'".format(element_name, ele_xpath)

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(
    u'I get value of field "{field_name}" with xpath "{field_xpath}" by "{ByTextOrValueOrAttribute}" and verify partial text "{exp_field_value:NullableString}" presence')
def GetPartialValueInFieldAndVerify(context, field_name: str, field_xpath: str, ByTextOrValueOrAttribute: str,
                                    exp_field_value: str):
    """
    This Method can be used to verify if given xpath contains partial text.
    :param context: context of the run
    :param field_name: field name whose value needs to be retrieved
    :param field_xpath: field xpath whose value needs to be fetched
    :param exp_field_text: Text the Xpath should contain
    :return: True if found text in xpath as expected, else return err/ exception
    """
    try:
        logging.info(
            "Input params for step: '{}', '{}', '{}', '{}'".format(field_name, field_xpath, ByTextOrValueOrAttribute,
                                                                   exp_field_value))
        # field_xpath = eval(field_xpath)
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        if ('context' in exp_field_value) or ("[" and "]" in exp_field_value):
            exp_field_value = eval(exp_field_value)

        if ByTextOrValueOrAttribute.casefold() == "text":
            field_text = context.server_selen_obj.getText_In_Xpath(field_xpath)
        elif ByTextOrValueOrAttribute.casefold() == "value":
            field_text = context.server_selen_obj.GetAttributeTextValueInXpath(field_xpath)
        elif "attribute:" in ByTextOrValueOrAttribute.casefold():
            field_text = context.server_selen_obj.GetValueofAttributeInXpath(field_xpath,
                                                                             ByTextOrValueOrAttribute.split(":")[-1])
        else:
            assert False, "Incorrect ByTextOrValueAttribute '{}' value provided. Mention 'text' for fetching value by " \
                          "elem.text or Mention 'value' for fetching by get_attribute('value') or Mention correct " \
                          "'attribute:attribute_name' for fetching by get_attribute(attribute)".format(
                ByTextOrValueOrAttribute)
        context.field_text = field_text
        context.test_execution_data['"{}" field name with xpath "{}" value by "{}"'.format(field_name, field_xpath,
                                                                                           ByTextOrValueOrAttribute)] = field_text
        if field_text is not False:
            logging.info(
                "Value '{}' found by '{}' in field '{}' having xpath '{}'".format(field_text, ByTextOrValueOrAttribute,
                                                                                  field_name, field_xpath))
            print(
                "Value '{}' found by '{}' in field '{}' having xpath '{}'".format(field_text, ByTextOrValueOrAttribute,
                                                                                  field_name, field_xpath))
            if exp_field_value in field_text:
                logging.info(
                    "Expected Partial Text '{}' found in field '{}' having xpath '{}' found by '{}'".format(
                        exp_field_value, field_name,
                        field_xpath, ByTextOrValueOrAttribute))
                print("Expected Partial Text '{}' found in field '{}' having xpath '{}' found by '{}'".format(
                    exp_field_value, field_name,
                    field_xpath, ByTextOrValueOrAttribute))
                return True
            else:
                assert False, "Expected Partial Text '{}' could not be found in field '{}' having xpath '{}' found by '{}'. Actual found '{}'".format(
                    exp_field_value, field_name, field_xpath, ByTextOrValueOrAttribute, field_text)

        else:
            assert False, "Partial Text could not be found by '{}' in field '{}' having xpath '{}'. Found : '{}'".format(
                ByTextOrValueOrAttribute, field_name, field_xpath, field_text)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u" Navigate to Back")
def Navigate_to_backPage(context):
    """
    Navigate to Back Page
    """
    try:
        context.server_selen_obj.navigate_to_back()
        logging.info("Successfully Navigated to back page")
        context.execute_steps(
            f'''
            Given  I explicitly wait for "15" seconds for field "Rotation Spinner" with xpath "GroupsAndConfig['ServerPage_GenericSpinner']" to disappear
            '''
        )
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "{}:{}:{} occurred while performing the click action ".format(exc_type, exc_obj, exc_tb)


@step(
    u'I verify if "{field_name}" field with xpath "{field_xpath}" has "{exp_tooltip:NullableString}" as tooltip value')
def verify_tooltip_for_xpath(context, field_name, field_xpath, exp_tooltip):
    """
    This method is to verify if correct tooltip value is present in the mentioned field xpath
    :param field_name: field name to verify the tooltip
    :param field_xpath: xpath of the element
    :param exp_tooltip: expected tooltip value to find in the provided xpath.
    :return: True if successful, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}', '{}'".format(field_name, field_xpath, exp_tooltip))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        if ('context' in exp_tooltip) or ("[" and "]" in exp_tooltip):
            exp_tooltip = eval(exp_tooltip)
        status = context.server_selen_obj.mouse_hover_on_xpath(field_xpath)  # mouse hover on //img tag
        context.test_execution_data[
            'Mouse Hover status in Field "{}" with xpath "{}"'.format(field_name, field_xpath, )] = status
        if status is False:
            assert False, "Couldn't Hover the mouse in field '{}' having xpath '{}'".format(field_name, field_xpath)
        logging.info("Successfully Hovered the mouse in field '{}' having xpath '{}'".format(field_name, field_xpath))
        print("Successfully Hovered the mouse in field '{}' having xpath '{}'".format(field_name, field_xpath))

        status = context.server_selen_obj.IsTextExistsInXpath(field_xpath, exp_tooltip)
        context.test_execution_data['Field "{}" with xpath "{}" value found with tooltip "{}"'.format(field_name,
                                                                                                      field_xpath,
                                                                                                      exp_tooltip)] = status
        if status == True:
            logging.info(
                "Expected tooltip value '{}' found in field '{}' having xpath '{}'".format(exp_tooltip, field_name,
                                                                                           field_xpath))
            print("Expected tooltip value '{}' found in field '{}' having xpath '{}'".format(exp_tooltip, field_name,
                                                                                             field_xpath))
            return True
        else:
            assert False, "Expected tooltip value '{}' could not be found in field '{}' having xpath '{}'".format(
                exp_tooltip, field_name, field_xpath)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "{}:{}:{} occurred while performing the click action ".format(exc_type, exc_obj, exc_tb)


@step(
    u'I get value list of field "{field_name}" with xpath "{field_xpath}" by "{ByTextOrValueOrAttribute}" and verify "{exp_field_value_list}" presence')
def GetValueListInFieldAndVerifyValueList(context, field_name, field_xpath, ByTextOrValueOrAttribute,
                                          exp_field_value_list):
    """
    This Method can be used to get value af any field with provided xpath and verify if it is the same expected value
    :param context: context of the run
    :param field_name: field name whose value needs to be retrieved
    :param field_xpath: field xpath whose value needs to be fetched
    :param ByTextOrValueOrAttribute:
                        Mention 'text' for fetching value by elem.text
                        Mention 'value' for fetching by get_attribute('value')
                        Mention correct 'attribute:attribute_name' for fetching by get_attribute(attribute)
    :param exp_field_value_list: List Value expected in the mentioned attribute
    :return: True if found same value list as expected, else return err/ exception
    """
    try:
        logging.info(
            "Input params for step: '{}', '{}', '{}', '{}'".format(field_name, field_xpath, ByTextOrValueOrAttribute,
                                                                   exp_field_value_list))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        if ('context' in exp_field_value_list) or ("[" and "]" in exp_field_value_list):
            exp_field_value_list = eval(exp_field_value_list)

        if ByTextOrValueOrAttribute.casefold() == "text":
            field_text_list = context.server_selen_obj.GetMultipleElements_TextListInXpath(field_xpath)
        elif ByTextOrValueOrAttribute.casefold() == "value":
            field_text_list = context.server_selen_obj.GetMultipleElements_ListByValueInXpath(field_xpath)
        elif "attribute:" in ByTextOrValueOrAttribute.casefold():
            field_text_list = context.server_selen_obj.GetMultipleElements_ListByAttributeInXpath(field_xpath,
                                                                                                  ByTextOrValueOrAttribute.split(
                                                                                                      ":")[-1])
        else:
            assert False, "Incorrect ByTextOrValueAttribute '{}' value provided. Mention 'text' for fetching value by " \
                          "elem.text or Mention 'value' for fetching by get_attribute('value') or Mention correct " \
                          "'attribute:attribute_name' for fetching by get_attribute(attribute)".format(
                ByTextOrValueOrAttribute)
        context.field_text = field_text_list
        context.test_execution_data['"{}" field name with xpath "{}" value list by "{}"'.format(field_name, field_xpath,
                                                                                                ByTextOrValueOrAttribute)] = field_text_list
        if field_text_list is not False:
            logging.info(
                "Value list '{}' found by '{}' in field '{}' having xpath '{}'".format(field_text_list,
                                                                                       ByTextOrValueOrAttribute,
                                                                                       field_name, field_xpath))
            print(
                "Value list '{}' found by '{}' in field '{}' having xpath '{}'".format(field_text_list,
                                                                                       ByTextOrValueOrAttribute,

                                                                                       field_name, field_xpath))
            if len(field_text_list) == len(exp_field_value_list):
                fail_list = []
                for each_text in exp_field_value_list:

                    if each_text in field_text_list:
                        pass
                    else:
                        fail_list.append(each_text)

            else:
                assert False, "Actual text list length '{}' is not equal to expected text list length '{}' " \
                              "in field '{}' having xpath'{}'. \n Actual text list = '{}' \n" \
                              "Expected text list = '{}'".format(len(field_text_list), len(exp_field_value_list),

                                                                 field_name, field_xpath, field_text_list,
                                                                 exp_field_value_list)
            if len(fail_list) == 0:
                logging.info(
                    "Expected Value list '{}' found in field '{}' having xpath '{}' found by '{}'".format(
                        exp_field_value_list, field_name, field_xpath, ByTextOrValueOrAttribute))
                print("Expected Value list '{}' found in field '{}' having xpath '{}' found by '{}'".format(
                    exp_field_value_list, field_name, field_xpath, ByTextOrValueOrAttribute))
                return True

            else:
                assert False, "Could not find following expected list values '{}' in  field '{}' having xpath'{}'. \n Actual text list = '{}' \n" \
                              "Expected text list = '{}'".format(fail_list, field_name, field_xpath, field_text_list,
                                                                 exp_field_value_list)
        else:
            assert False, "Value could not be found by '{}' in field '{}' having xpath '{}'. Found : '{}'".format(
                ByTextOrValueOrAttribute, field_name, field_xpath, field_text_list)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(
    u'I get field "{field_name}" with xpath "{field_xpath}" by "{ByTextOrValueOrAttribute}" and verify length to be "{length}"')
def GetValueInFieldAndVerifyFieldLength(context, field_name: str, field_xpath: str, ByTextOrValueOrAttribute: str,
                                        length: str):
    """
    This Method can be used to verify length of a given field.
    :param context: context of the run
    :param field_name: field name whose value needs to be retrieved
    :param field_xpath: field xpath whose value needs to be fetched
    :param length: expected field length
    :return: True if found text in xpath as expected, else return err/ exception
    """
    try:
        logging.info(
            "Input params for step: '{}', '{}', '{}', '{}'".format(field_name, field_xpath, ByTextOrValueOrAttribute,
                                                                   length))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)

        if ByTextOrValueOrAttribute.casefold() == "text":
            field_text = context.server_selen_obj.getText_In_Xpath(field_xpath)
        elif ByTextOrValueOrAttribute.casefold() == "value":
            field_text = context.server_selen_obj.GetAttributeTextValueInXpath(field_xpath)
        elif "attribute:" in ByTextOrValueOrAttribute.casefold():
            field_text = context.server_selen_obj.GetValueofAttributeInXpath(field_xpath,
                                                                             ByTextOrValueOrAttribute.split(":")[-1])
        else:
            assert False, "Incorrect ByTextOrValueAttribute '{}' value provided. Mention 'text' for fetching value by " \
                          "elem.text or Mention 'value' for fetching by get_attribute('value') or Mention correct " \
                          "'attribute:attribute_name' for fetching by get_attribute(attribute)".format(
                ByTextOrValueOrAttribute)
        context.field_text = field_text
        context.test_execution_data['"{}" field name with xpath "{}" value by "{}"'.format(field_name, field_xpath,
                                                                                           ByTextOrValueOrAttribute)] = field_text
        if field_text is not False:
            logging.info(
                "Value '{}' found by '{}' in field '{}' having xpath '{}'".format(field_text, ByTextOrValueOrAttribute,
                                                                                  field_name, field_xpath))
            print("Value '{}' found by '{}' in field '{}' having xpath '{}' with length".format(field_text,
                                                                                                ByTextOrValueOrAttribute,
                                                                                                field_name, field_xpath,
                                                                                                len(field_text)))
            if len(field_text) == int(length):
                logging.info(
                    "Field length is equal to {}  for field {} with xpath {}".format(length, field_name, field_xpath))
                print("Field length is equal to {}  for field {} with xpath {}".format(length, field_name, field_xpath))
                return True
            else:
                assert False, "Field length is not equal to {} for field {} with xpath {}. Actual Length found to be {}".format(
                    length, field_name, field_xpath, str(len(field_xpath)))

        else:
            assert False, "Text could not be found by '{}' in field '{}' having xpath '{}'. Found : '{}'".format(
                ByTextOrValueOrAttribute, field_name, field_xpath, field_text)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(u'I get text color for the field name "{}" with xpath "{}" and verify color to be "{}"')
def GetTextColor(context, field_name: str, field_xpath: str, expected_color: str):
    """
    This Method can be used to get the text color in hexa code.
    :param context: context of the run
    :param field_name: field name whose value needs to be retrieved
    :param field_xpath: field xpath whose value needs to be fetched
    :param length: expected field length
    :return: True if found text in xpath as expected, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}', '{}'".format(field_name, field_xpath, expected_color))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        if ('context' in expected_color) or ("[" and "]" in expected_color):
            expected_color = eval(expected_color)
        text_color = context.server_selen_obj.getTextColor(field_xpath)
        context.field_text = text_color
        context.test_execution_data['"{}" field name with xpath "{}""'.format(field_name, field_xpath)] = text_color
        if text_color is not False:
            logging.info(
                "Text color '{}' is found field '{}' having xpath '{}'".format(text_color, field_name, field_xpath))
            print("Text color '{}' is found field '{}' having xpath '{}'".format(text_color, field_name, field_xpath))
            if text_color == expected_color:
                logging.info(
                    "Text color matched with expected color {} for field {} with xpath {}".format(expected_color,
                                                                                                  field_name,
                                                                                                  field_xpath))
                print("Text color matched with expected color {} for field {} with xpath {}".format(expected_color,
                                                                                                    field_name,
                                                                                                    field_xpath))
                return True
            else:
                assert False, "Text color doesnot match with expected color {} for field {} with xpath {}".format(
                    expected_color, field_name, field_xpath)
        else:
            assert False, "Text color could not be found for field '{}' having xpath '{}'. Found : '{}'".format(
                field_name, field_xpath, text_color)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(
    u'I refresh to verify "{content_area}" having "{xpath_list}" list of xpath to be displayed for given number of "{tries}" tries')
def get_last_check_in_time(context, content_area, xpath_list, tries):
    """
    This Method provided device last check-in time to  server
    :param content_area : content area whose value needs to be verified
    :param xpath_list : ## list of xpath to be verified
    :param tries : ## number of retry
    :return True if pass, else Assert false
    """
    try:
        logging.info("Input params for step: '{}','{}', '{}'".format(content_area, xpath_list, tries))
        if ('context' in xpath_list) or ("[" and "]" in xpath_list):
            xpath_list = eval(xpath_list)
        for each_try in range(int(tries)):
            result = []
            for each_xpath in xpath_list:
                if ('context' in each_xpath) or ("[" and "]" in each_xpath):
                    each_xpath = eval(each_xpath)
                status = context.server_selen_obj.WaitForXpath(each_xpath, 5)
                if status != True:
                    logging.info("Element with xpath '{}' not found".format(each_xpath))
                    result.append(each_xpath)
            if len(result) == 0:
                logging.info("All element for list of xpath '{}' found".format(xpath_list))
                context.test_execution_data["All element for list of xpath '{}' found".format(xpath_list)] = result
                return True
            logging.info(
                "Elements with xpath '{}' not found , Attempting to retry '{}'/'{}'".format(result, int(each_try) + 1,
                                                                                            tries))
            result.clear()
            time.sleep(10 * int(tries))
            context.server_selen_obj.refresh_page()

        assert False, "Element could not be found for field '{}' having xpath '{}' for a given number of tried'{}'".format(
            content_area, xpath_list, tries)

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "{}:{}:{} occurred".format(exc_type, exc_obj, exc_tb)


@step(u'I wait for "{seconds}" seconds')
def CloseWindowWithXPath(context, seconds):
    """
    This Method is to wait
    :param context: context of the run
    :param seconds: time to wait in seconds
    :return :
    """
    try:
        logging.info("Waiting for {} seconds".format(seconds))
        print("Waiting for {} seconds".format(seconds))
        return time.sleep(int(seconds))
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(
    u'I verify the color of the field name "{field_name}" with xpath "{field_xpath}" and the color is "{expected_color}"')
def GetFieldBorderColor(context, field_name: str, field_xpath: str, expected_color: str):
    """
    This Method can be used to get the field color in hexa code.
    :param context: context of the run
    :param field_name: field name whose value needs to be retrieved
    :param field_xpath: field xpath whose value needs to be fetched
    :param length: expected field length
    :return: True if found text in xpath as expected, else return err/ exception
    """
    try:
        logging.info("Input params for step: '{}', '{}', '{}'".format(field_name, field_xpath, expected_color))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        if ('context' in expected_color) or ("[" and "]" in expected_color):
            expected_color = eval(expected_color)
        text_color = context.server_selen_obj.getcssvalue(field_xpath)
        context.text_color = text_color
        context.test_execution_data['"{}" field name with xpath "{}""'.format(field_name, field_xpath)] = text_color
        if text_color is not False:
            logging.info(
                "Text color '{}' is found field '{}' having xpath '{}'".format(text_color, field_name, field_xpath))
            print("Text color '{}' is found field '{}' having xpath '{}'".format(text_color, field_name, field_xpath))
            if text_color == expected_color:
                logging.info(
                    "Text color matched with expected color {} for field {} with xpath {}".format(expected_color,
                                                                                                  field_name,
                                                                                                  field_xpath))
                print("Text color matched with expected color {} for field {} with xpath {}".format(expected_color,
                                                                                                    field_name,
                                                                                                    field_xpath))
                return True
            else:
                assert False, "Text color doesnot match with expected color {} for field {} with xpath {}".format(
                    expected_color, field_name, field_xpath)
        else:
            assert False, "Text color could not be found for field '{}' having xpath '{}'. Found : '{}'".format(
                field_name, field_xpath, text_color)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)


@step(
    u'I upload a file "{file_name}" from the file path "{file_path}" to the field "{field_name}" with xpath "{field_xpath}"')
def Uploadfilefromxpath(context, file_name, file_path, field_name, field_xpath):
    """
    This Method can be used to upload a file in the xpath provided
    :param context: context of the run
    :param file_name: name of the file
    :param file_path: path of the file
    :param field_name: field name
    :param field_xpath: field xpath
    :return: True if successful, else return err/ exception
    """
    try:
        global file_names
        file_names = []
        logging.info(
            "Input params for step: '{}', '{}', '{}', '{}'".format(file_name, file_path, field_name, field_xpath))
        if ('context' in field_xpath) or ("[" and "]" in field_xpath):
            field_xpath = eval(field_xpath)
        if ('context' in file_path) or ("[" and "]" in file_path):
            file_path = eval(file_path)
        if ('context' in file_name) or ("[" and "]" in file_name):
            file_name = eval(file_name)

        if type(file_name) == list:
            for file in file_name:
                file_names.append(file)
        else:
            file_names.append(file_name)
            logging.info("file added : '{}'".format(file_names))

        File_location = file_path + '\\' + file_names[0]
        if len(file_names) == 1:
            pass
        else:
            for i in range(1, len(file_names)):
                File_location = File_location + ' \n ' + file_path + '\\' + file_names[i]

        logging.info("These Files {} are going to upload".format(File_location))
        status = context.server_selen_obj.UploadfileInXpath(field_xpath, File_location)

        if status is True:
            logging.info(
                "Successfully uploaded file '{}' in Field '{}' having xpath '{}'".format(File_location, field_name,
                                                                                         field_xpath))
            print("Successfully uploaded file  '{}' in Field '{}' having xpath '{}'".format(File_location, field_name,
                                                                                            field_xpath))
            return True
        else:
            assert False, "Couldn't upload file '{}' in Field '{}' having xpath '{}'".format(File_location, field_name,
                                                                                             field_xpath)
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)
        assert False, "'{}':'{}':'{}' occurred ".format(exc_type, exc_obj, exc_tb)
