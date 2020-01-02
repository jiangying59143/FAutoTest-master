# coding=utf-8
import json
import threading
import time

import pymysql
from selenium import webdriver
from selenium.webdriver.support.select import Select
import os
import logging
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

quetions = []

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def screenshot(driver, appname, name, pic):
    dirPath = os.path.split(os.path.realpath(__file__))[0] + "/" + appname
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    PIC_SRC = os.path.join(dirPath, name + '_' + pic + '.html')
    # logger.info('PIC_SRC ---> ' + PIC_SRC)
    # f = open(PIC_SRC,'wb')
    # f.write(driver.page_source)
    # f.close()
    PIC_SRC = PIC_SRC.replace(".html", ".png")
    driver.get_screenshot_as_file(PIC_SRC)


def screenshot_long(driver, app_name, name, pic):
    driver.maximize_window()
    js_height = "return document.body.clientHeight"
    height = driver.execute_script(js_height)
    k = 1
    while True:
        if k * 500 < height:
            js_move = "window.scrollTo(0,{})".format(k * 500)
            driver.execute_script(js_move)
            time.sleep(0.2)
            height = driver.execute_script(js_height)
            k += 1
        else:
            break
    scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(scroll_width, scroll_height)
    dir_path = os.path.split(os.path.realpath(__file__))[0] + "/" + app_name
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    pic_src = os.path.join(dir_path, name + '_' + pic + '.png')
    driver.get_screenshot_as_file(pic_src)


def isElementExistById(driver, elementId):
    flag = True
    try:
        if len(driver.find_element_by_id(elementId)) > 0:
            return flag
    except:
        flag = False
        return flag


def isElementExistByName(driver, name):
    flag = True
    try:
        if len(driver.find_element_by_name(name)) > 0:
            return flag
    except:
        flag = False
        return flag


def isElementExistByXpath(driver, xpath):
    flag = True
    try:
        if len(driver.find_elements_by_xpath(xpath)) > 0:
            return flag
    except:
        flag = False
        return flag


def getTitleAndAnswers(driver, index, isScore):
    title_and_answers = {}
    this_title_html = driver.find_elements_by_xpath(
        '//li[@id="E' + str(index) + '"][@style="display: block;"]/table[1]/tbody[1]/tr[1]/td[1]/div[@class="ECnt"]')[
        0].get_attribute('innerHTML')
    this_title_and_answers = this_title_html.split("<br>")
    this_title = this_title_and_answers[1].split("</b>")[1].replace('<b>' + str(index) + '.</br>', '').strip()
    title_and_answers["title"] = this_title;
    # logger.debug(str(index) + ':' + this_title)
    for i in range(2, len(this_title_and_answers)):
        try:
            if isScore:
                title_and_answers[this_title_and_answers[i].split(u"、", 1)[0]] = \
                this_title_and_answers[i].split(u"、", 1)[1]
            else:
                title_and_answers[this_title_and_answers[i].split(u"、", 1)[1]] = \
                this_title_and_answers[i].split(u"、", 1)[0]
        except Exception, ex:
            # print this_title_html
            if this_title_and_answers[i] != "" and u"、" in this_title_and_answers[i]:
                title_and_answers[this_title_and_answers[i].split(u"、", 1)[0]] = \
                this_title_and_answers[i].split(u"、", 1)[0]
    # logger.debug(title_and_answers)
    # logger.debug("\n-----------------")
    return title_and_answers


def yinyangWeb(list, name, age, sex, edu, metier, orgName):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path="../driver/chromedriver.exe", options=options)
    # driver = webdriver.Chrome(executable_path="../driver/chromedriver.exe")
    driver.get("http://www.jscdc.cn/KABP2011/business/index1.jsp")
    # http://npm.taobao.org/mirrors/chromedriver/78.0.3904.105/
    city = Select(driver.find_element_by_id("zone3"))
    city.select_by_visible_text("宿迁市")
    zone = Select(driver.find_element_by_id("zone4"))
    zone.select_by_visible_text("沭阳县")
    village = Select(driver.find_element_by_id("zone5"))
    village.select_by_visible_text("东小店乡")
    driver.find_element_by_id("name").send_keys(name)
    ageGroup = Select(driver.find_element_by_id("ageGroup"))
    ageGroup.select_by_visible_text(age)
    sexGroup = Select(driver.find_element_by_name("sex"))
    sexGroup.select_by_visible_text(sex)
    educationStatus = Select(driver.find_element_by_id("educationStatus"))
    educationStatus.select_by_visible_text(edu)
    metierGroup = Select(driver.find_element_by_id("metier"))
    metierGroup.select_by_visible_text(metier)
    driver.find_element_by_id("orgName").send_keys(orgName)
    driver.find_element_by_id("log_img").click()
    totalQuestionCount = int(driver.find_element_by_id("__subjectCount").text)
    for index in range(1, totalQuestionCount + 1):
        questionType = driver.find_elements_by_xpath('//li[@id="E' + str(
            index) + '"][@style="display: block;"]/table[1]/tbody[1]/tr[1]/td[1]/div[@class="ECnt"]/b[1]')[
            0].text.strip()
        multipleflag = u"多选题" in questionType

        selections = []

        this_title_and_answers = getTitleAndAnswers(driver, index, False)

        correctSelections = []

        for q in list:
            if q["title"] in this_title_and_answers["title"]:
                for a in q["answers"]:
                    if this_title_and_answers.has_key(a):
                        correctSelections.append(a)
                        selections.append(this_title_and_answers[a])
        if len(selections) == 0:
            if multipleflag:
                driver.find_elements_by_xpath('//input[@type="checkbox"][@value="A' + str(index) + '"]')[0].click()
                driver.find_elements_by_xpath('//img[@id="Key_Next"]')[0].click()
            else:
                driver.find_elements_by_xpath('//input[@type="radio"][@value="A' + str(index) + '"]')[0].click()
        else:
            # print "--------------------------------------"
            # for i in this_title_and_answers:
            #     print "dict[%s]=" % i,this_title_and_answers[i]
            # for x in correctSelections:
            #     print "正确答案：" + str(x)
            # print "选择了:" + str(selections)
            if multipleflag:
                for selection in selections:
                    driver.find_elements_by_xpath('//input[@type="checkbox"][@value="' + selection + str(index) + '"]')[
                        0].click()
                driver.find_elements_by_xpath('//img[@id="Key_Next"]')[0].click()
            else:
                driver.find_elements_by_xpath('//input[@type="radio"][@value="' + selections[0] + str(index) + '"]')[
                    0].click()

    driver.find_elements_by_xpath('//td[@id="btnAct' + str(totalQuestionCount) + '"]/div[1]/input[1]')[0].click()
    confirm = driver.switch_to.alert
    time.sleep(1)
    confirm.accept()  # 接受
    time.sleep(1)
    screenshot_long(driver, "healthComputer", name, "pic")

    correctCount = 0;
    for i in range(1, totalQuestionCount + 1):
        healthQuestion = {}

        this_title_and_answers = getTitleAndAnswers(driver, i, True)
        # print this_title_and_answers
        title = this_title_and_answers["title"]

        answers = driver.find_element_by_id("KWait" + str(i)).text
        if u"标准答案：" in answers:
            answers = answers.split(u"您的答案：")[1].split(u"标准答案：")[1].strip()
        else:
            correctCount += 1
            answers = answers.split(u"您的答案：")[1].strip()

        cse = []
        for c in answers:
            if this_title_and_answers.has_key(c):
                cse.append(this_title_and_answers[c])
        healthQuestion.update(title=title, answers=answers, selections=cse)
        quetions.append(healthQuestion)
    print name + "->总题数:" + str(totalQuestionCount) + " 答对题数：" + str(correctCount) + " 分数:" + driver.find_element_by_id(
        "df_fs").text


def run():
    conn = pymysql.connect(host="xxx", user="xxxx", password="xxxx", database="questionnaire",
                           charset="utf8")
    # 获取游标
    cur = conn.cursor()
    selectSql = "select title, answers from health"
    cur.execute(selectSql)
    results = cur.fetchall()
    list = []
    for row in results:
        answers = row[1][2:(len(row[1]) - 2)]
        answerss = answers.split('", "')
        # print json.dumps(answerss).decode('unicode-escape')
        dic = {"title": row[0][1:(len(row[0]) - 1)], "answers": answerss}
        list.append(dic)

    # yinyangWeb(list, u'蒋英', "35～40岁以下", "男", "小学", "工人", u"东小店乡谢圩村")

    threads = []
    t1 = threading.Thread(target=yinyangWeb, args=(list, u'蒋英', "35～40岁以下", "男", "小学", "工人", u"东小店乡谢圩村"))
    threads.append(t1)
    t2 = threading.Thread(target=yinyangWeb, args=(list, u'赵武', "35～40岁以下", "男", "小学", "工人", u"东小店乡谢圩村"))
    threads.append(t2)
    t3 = threading.Thread(target=yinyangWeb, args=(list, u'王柳', "35～40岁以下", "男", "小学", "工人", u"东小店乡谢圩村"))
    threads.append(t3)
    t4 = threading.Thread(target=yinyangWeb, args=(list, u'詹三', "35～40岁以下", "男", "小学", "工人", u"东小店乡谢圩村"))
    threads.append(t4)
    t5 = threading.Thread(target=yinyangWeb, args=(list, u'朱天', "35～40岁以下", "男", "小学", "工人", u"东小店乡谢圩村"))
    threads.append(t5)
    # t6 = threading.Thread(target=yinyangWeb, args=(list, u'朱天1', "35～40岁以下", "男", "小学", "工人", u"东小店乡谢圩村"))
    # threads.append(t6)
    # t7 = threading.Thread(target=yinyangWeb, args=(list, u'朱天2', "35～40岁以下", "男", "小学", "工人", u"东小店乡谢圩村"))
    # threads.append(t7)
    # t8 = threading.Thread(target=yinyangWeb, args=(list, u'朱天3', "35～40岁以下", "男", "小学", "工人", u"东小店乡谢圩村"))
    # threads.append(t8)
    # t9 = threading.Thread(target=yinyangWeb, args=(list, u'朱天4', "35～40岁以下", "男", "小学", "工人", u"东小店乡谢圩村"))
    # threads.append(t9)
    # t10 = threading.Thread(target=yinyangWeb, args=(list, u'朱天5', "35～40岁以下", "男", "小学", "工人", u"东小店乡谢圩村"))
    # threads.append(t10)
    # 启动线程
    for t in threads:
        t.start()
    # 守护线程
    for t in threads:
        t.join()


    # sql语句
    sql = "insert into health (title, answers) values (%s,%s)"

    for question in quetions:
        result = json.dumps(question).decode('unicode-escape')
        # print result
        # 参数化方式传参
        try:
            row_count = cur.execute(sql, [json.dumps(question['title']).decode('unicode-escape'),
                                          json.dumps(question["selections"]).decode('unicode-escape')])
        except Exception, e:
            pass
            # logger.error("数据库插入：" + str(e))

    try:
        conn.commit()
    except Exception, e:
        logger.error("数据库提交：" + str(e))
        conn.rollback()
    cur.close()
    conn.close()
    del quetions[:]
    return True


if __name__ == '__main__':
    for i in range(1, 101):
        finished = run()
        while not finished:
            time.sleep(1)
        print "-------------------第" + str(i) + "遍完成--------------"
