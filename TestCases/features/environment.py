import os, sys
import json

sys.path.append(os.path.join((os.path.realpath(__file__).split("TestCases")[0])))
import logging
from datetime import datetime
import collections
import time
import shutil
import sys
import subprocess
from behave.model import Scenario
from behave import use_fixture, configuration
import json5
# import Reporter.GenerateHTMLReport as GenerateHTMLReport
from TestCases.fixtures import *
from Utils.common_selenium_utils import *
from Utils.common_server_steps import *
from TestCases.features.steps.environment_steps import *

# Generic Log File Paths
TestSuite = "TestCases"
Program = "Aaditya"
USER = "DOCTOR"

TimeStamp = datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
TestCases_Folder = os.path.join((os.path.realpath(__file__)).split(TestSuite)[0], TestSuite)
logs_directory = os.path.join(TestCases_Folder, "Results", "LOGS", TimeStamp)
print(logs_directory)

xml_dir = os.path.join(TestCases_Folder, "Results", "XML")
xmlreport_dir = os.path.join(TestCases_Folder, "Results", "XML", TimeStamp)
jsonreport_dir = os.path.join(TestCases_Folder, "Results", "JSON", TimeStamp)
htmlreport_dir = os.path.join(TestCases_Folder, "Results", "HTML", TimeStamp)
current_log_directory = os.path.join(logs_directory, "this_run" + ".log")


root_fol = os.path.join((os.path.realpath(__file__)).split("AutomationFW")[0])
common_report_fol = os.path.join(root_fol, "AutomationFW", "Reporter")
report_py_file = os.path.join(common_report_fol, "GenerateHTMLReport.py")

if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)
if not os.path.exists(xmlreport_dir):
    os.makedirs(xmlreport_dir)
if not os.path.exists(jsonreport_dir):
    os.makedirs(jsonreport_dir)
if not os.path.exists(htmlreport_dir):
    os.makedirs(htmlreport_dir)

logfile_path = current_log_directory


def ExceptionFunction(err, exc_type, exc_obj, exc_tb):
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    sys.stderr.write("ERRORED DESC\t::{}:\n".format(str(err)))
    sys.stderr.write("ERRORED MODULE\t::{}}:\n".format(str(exc_type)))
    sys.stderr.write("ERRORED FILE\t::{}}:\n".format(str(fname)))
    sys.stderr.write("ERRORED LINE\t::{}}:\n".format(str(exc_tb.tb_lineno)))
    logging.error("ERRORED DESC\t::{}:\n".format(str(err)))
    logging.error("ERRORED MODULE\t::{}:\n".format(str(exc_type)))
    logging.error("ERRORED FILE\t::{}:\n".format(str(fname)))
    logging.error("ERRORED LINE\t::{}:\n".format(str(exc_tb.tb_lineno)))


def before_all(context):
    tags_thisRun = ""
    all_argvs = sys.argv[1:]
    l = len(all_argvs)
    for index, obj in enumerate(all_argvs):
        if obj == "--tags" or obj == "-t":
            if index < (l - 1):
                tags_thisRun = tags_thisRun + all_argvs[index + 1]
        elif "--tags=" in obj.lower():
            tags_thisRun = tags_thisRun + obj.split("=")[-1]
    context.tags_thisRun = tags_thisRun
    context.logfile_path = logfile_path

    print("Logfile_path={}".format(logfile_path))
    fh = logging.FileHandler(logfile_path, mode='w')
    logging.getLogger().addHandler(fh)  # To get the logger and add a handler of the log file
    fh_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(funcName)s() - %(message)s')
    fh.setFormatter(fh_formatter)
    logging.info("Logfile_path={}".format(logfile_path))
    logging.info("Current working directory is: {}".format(os.getcwd()))
    # https://behave.readthedocs.io/en/latest/new_and_noteworthy_v1.2.6.html
    # https://github.com/behave/behave/blob/master/features/runner.continue_after_failed_step.feature

def before_feature(context, feature):
    feature_logfile_path = os.path.join(logs_directory, feature.name + ".log")
    fh1 = logging.FileHandler(feature_logfile_path, mode='w')
    logging.getLogger().addHandler(fh1)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(funcName)s() - %(message)s')
    fh1.setFormatter(formatter)
    logging.info("Started feature.name='{}'".format(feature.name))
    context.test_suite_execution_data = {}
    context.fh1 = fh1

    start_server_selen_obj(context, "browser.chrome")

    for selen_try in range(3):
        try:
            start_server_selen_obj(context, feature.tags)
            break
        except Exception as err:
            print("Will Retry after 5 seconds")
            logging.info("Will Retry after 5 seconds")
            time.sleep(5)
        logging.error('Cannot start Web browser')
        return


def before_tag(context, tag):
    if tag == "fixture.dummy_tag":
        use_fixture(dummy_fixture, context)


def before_scenario(context, scenario):
    logging.info("Started scenario.name='{}'".format(scenario.name))
    context.test_execution_data = {}
    context.os_specific_logs = collections.defaultdict(str)


def before_step(context, step):
    logging.info("Started step.name='{}'".format(step.name))


def after_step(context, step):
    logging.info("Completed step.name='{}'".format(step.name))


def after_scenario(context, scenario):
    logging.info("Completed scenario.name='{}'".format(scenario.name))
    try:
        context.server_selen_obj.quitDriver()
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ExceptionFunction(err, exc_type, exc_obj, exc_tb)

    if len(context.test_execution_data):
        context.test_suite_execution_data[scenario.name] = context.test_execution_data


def after_feature(context, feature):
    logging.info("Completed feature.name='{}'".format(feature.name))
    logging.getLogger().removeHandler(context.fh1)
    if len(context.test_suite_execution_data):
        file_path = os.path.join(jsonreport_dir,os.path.splitext(feature.filename)[0].replace(os.path.sep, ".").replace("/", ".").partition(".")[2] + ".json")
        with open(file_path, "w") as fp:
            fp.write(json.dumps(context.test_suite_execution_data, indent=2))


def after_all(context):
    xml_files = os.listdir(xml_dir)
    for each_xml_file in xml_files:
        if each_xml_file.endswith(".xml"):
            shutil.move(os.path.join(xml_dir, each_xml_file), xmlreport_dir)

    xunit_html_logfile_name = "xunit_" + context.tags_thisRun + "_" + datetime.now().strftime('%Y-%m-%d %H-%M-%S')  # + ".log"
    GenerateHTMLReport = subprocess.getoutput('xunit-viewer -r "{}" -o "{}" -t "{}" --unhandled-rejections=strict'.format(xmlreport_dir, os.path.join(htmlreport_dir, xunit_html_logfile_name), TestSuite + " Results"))
    xunit_html_report_file_path = os.path.join(htmlreport_dir, xunit_html_logfile_name + ".html")
    html_logfile_name = context.tags_thisRun + "_" + datetime.now().strftime('%Y-%m-%d %H-%M-%S') + ".html"
    html_report_file_path = os.path.join(htmlreport_dir, html_logfile_name)
    testrail_resultfile_path = ""
    os.system('python {} {} "{}" "{}" "{}" "{}"'.format(report_py_file, Program, xmlreport_dir, html_report_file_path, TimeStamp, testrail_resultfile_path))

    logging.info("XUnit Viewer Output Path of generated HTML report for '{}' program run of '{}' suite--> {}".format(USER,TestSuite,xunit_html_report_file_path))
    logging.info("New Custom generated HTML report for '{}' program run of '{}' suite--> {}".format(USER, TestSuite,html_report_file_path))

    if os.path.exists(xunit_html_report_file_path):
        subprocess.Popen("{}".format(xunit_html_report_file_path), shell=True)
    time.sleep(2)
    if os.path.exists(html_report_file_path):
        subprocess.Popen("{}".format(html_report_file_path), shell=True)

    logging.info("Reached After All")
