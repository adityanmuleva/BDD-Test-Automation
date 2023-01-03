from time import sleep
import os, pprint, json, sys
sys.path.append(os.path.join((os.path.realpath(__file__).split("Reporter")[0])))

import random
import sys
import time
import xml.etree.ElementTree as ET

import os, sys, time, pprint

Base_Dir = os.path.join((os.path.realpath(__file__)).split("AutomationFW")[0])
Base_Dir = os.path.join(Base_Dir, "AutomationFW", "Reporter")


if len(sys.argv) > 1:
    print("Parameters")
    Project = sys.argv[1]
    XML_FOLDER = sys.argv[2]
    ResultHTML = sys.argv[3]
    RESULT_FOLD = sys.argv[4]
else:
    print("Default")
    Project = "ABC"
    RESULT_FOLD = "2021-04-28 23-29-15"
    XML_FOLDER = os.path.join(Base_Dir, "TestCases", "Results", "XML", RESULT_FOLD)
    RES_FOLDER_ex = os.path.join(Base_Dir, "TestCases", "Results", "HTML", RESULT_FOLD)
    ResultHTML = os.path.join(RES_FOLDER_ex, RESULT_FOLD + ".html")

print("Generating Report for XML Path: " + str(XML_FOLDER))
print("Generating Report In HTML : " + str(ResultHTML))

TemplateFile = os.path.join(Base_Dir, "Template.html")

global Total_PASS, Total_FAIL, Total_Script_issue, Total, Total_Skipped, Total_Module, Total_Time_Taken, Total_Not_Executed

template1 = '<button type="button" class="accordion STATS">DESC</button>'
html_arr = []

Total_PASS = 0
Total_FAIL = 0
Total_Script_issue = 0
Total_Skipped = 0
Total_Not_Executed = 0


def get_data_formatted():
    all_execution_files = os.listdir(XML_FOLDER)
    Stat_dic = {}

    for eachxmlfile in all_execution_files:
        xml_file = os.path.join(XML_FOLDER, eachxmlfile)
        Module_Name_grp = "-".join(eachxmlfile.split(".")[0:-1])
        tree = ET.parse(xml_file)
        root = tree.getroot()
        mod_dic = {}
        root_data = root.attrib
        Total_TC = int(root_data["tests"])
        Total_F = 0
        Total_S = 0
        Total_P = 0
        Total_NE = 0

        Total_Time = root_data["time"]
        index = 0
        for eactestdata in root:
            index = index + 1
            data = eactestdata.attrib
            Module_Name = data["classname"].split(".")[0]
            base_desc = data["name"].split("--")
            if "--" in data["name"]:
                DESCRIPTION = base_desc[0]
                TestCaseName = base_desc[0]
            else:
                DESCRIPTION = data["name"]
                TestCaseName = Project + "_" + Module_Name + "_TC_" + str(index)

            Result_Status = str(data["status"]).upper()
            if "PASS" in Result_Status:
                Total_P = Total_P + 1
                Log_details = str(eactestdata[0].text).split("\n")
                while ("" in Log_details):
                    Log_details.remove("")
            elif "FAIL" in Result_Status:
                Total_F = Total_F + 1
                Log_details = str(eactestdata[0].text).split("\n")
                while ("" in Log_details):
                    Log_details.remove("")
            else:
                for j in eactestdata:
                    if j.text:
                        execution_logs = str(j.text).split('\n')
                        while ("" in execution_logs):
                            execution_logs.remove("")
                        if '@scenario.begin' in execution_logs:
                            if '@skip' in execution_logs[1] or 'SKIP' in execution_logs[1] or 'IGNORE' in \
                                    execution_logs[1]:
                                Total_S = Total_S + 1
                            else:
                                Total_NE = Total_NE + 1
                            Log_details = execution_logs

            TimeTaken = data["time"]
            Status_Description = "PASSED SUC"
            mod_dic.update(
                {TestCaseName: {"Module_Name": Module_Name, "DESCRIPTION": DESCRIPTION, "Result_Status": Result_Status,
                                "Status_Description": Status_Description, "Log_details": Log_details}})

        module_tc_data = {"TOTAL_MODULE_TC": Total_TC, "TOTAL_FAILED": Total_F, "TOTAL_SKIPPED": Total_S,
                          "TOTAL_PASSED": Total_P, "Total_Not_Executed": Total_NE,
                          "TOTAL_TIME": Total_Time}
        Stat_dic.update({Module_Name_grp:
                             {"TESTCASES": mod_dic,
                              "MOD_DETAILS": module_tc_data}})
    return Stat_dic


def Prepare_accordian_data(all_data_dic):
    global Total_PASS, Total_FAIL, Total_Script_issue, Total, Total_Skipped, Total_Module, Total_Time_Taken, Total_Not_Executed
    mod_des = '{0:70} | {1:10} | {2:10} | {3:10} | {4:10} | {5:10} | {6:10}'.format("MODULE ", "TOTAL", "PASSED",
                                                                                    "FAILED", "SKIPPED", "NOT-EXECUTED",
                                                                                    "TIME TAKEN")
    module_accord = '<button type="button" class="accordion headercol"><b><div class="pre1"> ' + str(
        mod_des) + ' </div></b></button>'
    html_arr.append(module_accord)
    html_arr.append('<div class="panel">')
    html_arr.append('</div>')
    Total_Module = 0
    Total_Time_Taken = 0

    for Module_grp_name, data_dic in all_data_dic.items():
        Total_Module = Total_Module + 1
        module_dic = data_dic["MOD_DETAILS"]
        Total_Time_Taken = Total_Time_Taken + int(float(module_dic["TOTAL_TIME"]))
        mod_des = '{0:70} | {1:3}        | {2:3}        | {3:3}        | {4:3}        | {5:3}        | {6:3}'.format(
            Module_grp_name, module_dic["TOTAL_MODULE_TC"], module_dic["TOTAL_PASSED"], module_dic["TOTAL_FAILED"],
            module_dic["TOTAL_SKIPPED"], module_dic["Total_Not_Executed"], module_dic["TOTAL_TIME"])
        module_accord = '<button type="button" class="accordion modulecol"><div class="pre1"> ' + str(
            mod_des) + ' </div></button>'
        html_arr.append(module_accord)
        html_arr.append('<div class="panel">')
        data_dic = data_dic["TESTCASES"]
        for TempTestCaseID, data in data_dic.items():
            # print(data)
            if "SCRIPT ISSUE" in str(data["Status_Description"]).upper():
                STATS = "nottested_01"
                Total_Script_issue = Total_Script_issue + 1
            else:
                if "PASS" in data["Result_Status"]:
                    STATS = "success_01"
                    Total_PASS = Total_PASS + 1
                    ID = "PASS"
                elif "FAIL" in data["Result_Status"]:
                    STATS = "fail_01"
                    Total_FAIL = Total_FAIL + 1
                    ID = "FAIL"
                elif "SKIPPED" in data["Result_Status"]:
                    if '@skip' in data["Log_details"][1] or 'SKIP' in data["Log_details"][1] or 'IGNORE' in \
                            data["Log_details"][1]:
                        STATS = "skip_01"
                        Total_Skipped = Total_Skipped + 1
                        ID = "SKIP"
                    else:
                        STATS = "nottested_01"
                        Total_Not_Executed = Total_Not_Executed + 1
                        ID = "NOTTESTED"
                else:
                    STATS = "nottested_01"
                    Total_Not_Executed = Total_Not_Executed + 1
                    ID = "NOTTESTED"

            DESC = data["DESCRIPTION"]
            Module_Name = data["Module_Name"]
            all_lines = data["Log_details"]

            DESCRIPTION = '{0:25} - {1:50}'.format(TempTestCaseID, DESC)
            html_arr.append('<div class="' + str(ID) + '">')
            template1 = '<button type="button" class="accordion ' + STATS + '"><div class="pre1"> ' + str(
                DESCRIPTION) + ' </div></button>'
            html_arr.append(template1)
            html_arr.append('<div class="panel">')
            html_arr.append('<pre">')

            for eachlogdata in all_lines:
                html_arr.append("<p>" + eachlogdata + "</p>")

            html_arr.append('</pre">')
            html_arr.append('</div>')
            html_arr.append('</div>')

        html_arr.append('</div>')
    return html_arr


def table_content():
    table_dic = {"Project": Project, "ExecutionDate": RESULT_FOLD, "Total_Module": Total_Module,
                 "Total_Time_Taken": str(Total_Time_Taken) + " seconds"}
    data = ""
    for name, value in table_dic.items():
        rowdata = "<tr><td>" + str(name) + "</td><td>" + str(value) + "</td></tr>"
        data = data + rowdata

    return data


def Build_the_HTML(html_arr, table_data):
    global Total_PASS, Total_FAIL, Total_Script_issue, Total, Total_Skipped, Total_Not_Executed

    template_obj = open(TemplateFile)
    template_all = template_obj.readlines()
    result_obj = open(ResultHTML, "w", encoding="utf-8")
    Total = Total_PASS + Total_FAIL + Total_Script_issue + Total_Skipped + Total_Not_Executed

    Status_Run = '<p>TOTAL EXECUTED : ' + str(Total) + ' | PASS : ' + str(Total_PASS) + ' | FAIL : ' + str(
        Total_FAIL) + ' | SCRIPT ISSUE : ' + str(Total_Script_issue) + ' | TOTAL SKIPPED : ' + str(
        Total_Skipped) + ' | TOTAL NOT EXECUTED : ' + str(Total_Not_Executed) + '</p>'
    # print(Status_Run)
    for eachtemplateline in template_all:
        if "<<STAT>>" in eachtemplateline:
            result_obj.writelines(Status_Run)

        if "<<DATE>>" in eachtemplateline:
            eachtemplateline = eachtemplateline.replace("<<DATE>>", str(RESULT_FOLD))

        if "<<PROJECT>>" in eachtemplateline:
            eachtemplateline = eachtemplateline.replace("<<PROJECT>>", str(Project))

        if "<<TOTAL>>" in eachtemplateline:
            eachtemplateline = eachtemplateline.replace("<<TOTAL>>", str(Total))

        if "<<PASSED>>" in eachtemplateline:
            eachtemplateline = eachtemplateline.replace("<<PASSED>>", str(Total_PASS))
        if "<<FAILED>>" in eachtemplateline:
            eachtemplateline = eachtemplateline.replace("<<FAILED>>", str(Total_FAIL))

        if "<<NOTTESTED>" in eachtemplateline:
            eachtemplateline = eachtemplateline.replace("<<NOTTESTED>>", str(Total_Not_Executed))

        if "<<SKIP>" in eachtemplateline:
            eachtemplateline = eachtemplateline.replace("<<SKIP>>", str(Total_Skipped))

        if "<<TABLEDATA>" in eachtemplateline:
            eachtemplateline = eachtemplateline.replace("<<TABLEDATA>>", str(table_data))

        if "<<DATA>>" in eachtemplateline:
            for eachline in html_arr:
                result_obj.writelines(eachline)
        else:
            result_obj.writelines(eachtemplateline)


data_dic = get_data_formatted()
html_arr = Prepare_accordian_data(data_dic)
table_data = table_content()
Build_the_HTML(html_arr, table_data)

print("Total_PASS : {}".format(Total_PASS))
print("Total_FAIL : {}".format(Total_FAIL))
print("Total_SKIPPED : {}".format(Total_Skipped))
print("Total_NOT-EXECUTED : {}".format(Total_Not_Executed))
