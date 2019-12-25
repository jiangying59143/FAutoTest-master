# coding=utf-8
import json
import threading
import time

import pymysql
from selenium import webdriver
from selenium.webdriver.support.select import Select
import os
import logging

quetions = []


def screenshot(driver, appname, name, pic):
    dirPath = os.path.split(os.path.realpath(__file__))[0] + "/" + appname
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    dirPath = dirPath + "/" + name
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    PIC_SRC = os.path.join(dirPath, pic + '.png')
    logging.info('PIC_SRC ---> ' + PIC_SRC)
    driver.get_screenshot_as_file(PIC_SRC)


def isElementExistById(driver, elementId):
    flag = True
    try:
        driver.find_element_by_id(elementId)
        return flag
    except:
        flag = False
        return flag


def isElementExistByXpath(driver, xpath):
    flag = True
    try:
        driver.find_elements_by_xpath(xpath)
        return flag
    except:
        flag = False
        return flag


def yinyangWeb(enname, name, age, sex, edu, metier):
    driver = webdriver.Chrome(executable_path="../driver/chromedriver.exe")
    driver.get("http://jscdc.cn/KABPWeb2011/paperTest1/createPagerForSafety.action")
    # http://npm.taobao.org/mirrors/chromedriver/78.0.3904.105/
    city = Select(driver.find_element_by_id("city"))
    city.select_by_visible_text("宿迁市")
    zone = Select(driver.find_element_by_id("zone"))
    zone.select_by_visible_text("沭阳县")
    village = Select(driver.find_element_by_id("village"))
    village.select_by_visible_text("东小店乡")
    driver.find_element_by_id("ename").send_keys(name)
    ageGroup = Select(driver.find_element_by_id("ageGroup"))
    ageGroup.select_by_visible_text(age)
    sexGroup = Select(driver.find_element_by_name("sex"))
    sexGroup.select_by_visible_text(sex)
    educationStatus = Select(driver.find_element_by_id("educationStatus"))
    educationStatus.select_by_visible_text(edu)
    metierGroup = Select(driver.find_element_by_id("metier"))
    metierGroup.select_by_visible_text(metier)
    driver.find_element_by_id("log_img").click()
    index = 0
    # 单选题
    while isElementExistById(driver, "A" + str(index)):
        driver.find_element_by_id("A" + str(index)).click()
        index = index + 1
    # 多选题
    while isElementExistByXpath(driver, '//input[@type="checkbox"][@value="A' + str(index) + '"]'):
        try:
            driver.find_elements_by_xpath('//input[@type="checkbox"][@value="A' + str(index) + '"]')[0].click()
            driver.find_elements_by_xpath('//img[@id="Key_Next"][@onclick="down(' + str(index + 1) + ')"]')[0].click()
            index = index + 1
        except Exception:
            logging.info("做题完成")
            break

    driver.find_element_by_id("Submit").click()
    confirm = driver.switch_to.alert
    time.sleep(1)
    confirm.accept()  # 接受
    alert = driver.switch_to.alert
    time.sleep(1)
    alert.accept()  # 确认
    time.sleep(1)
    screenshot(driver, "yinyang", enname, "pic")
    # 查看成绩
    driver.find_element_by_id("BtnOk").click()
    questionlist = driver.find_elements_by_tag_name("table");
    for question in questionlist:
        try:
            d = {}
            questionAndSelections = question.find_elements_by_tag_name("tr");
            questionTitleAndAnswer = questionAndSelections[0].find_elements_by_tag_name("td");
            title = questionTitleAndAnswer[0].get_attribute('textContent')
            d.update(title=title)
            print title
            answers = questionTitleAndAnswer[1].get_attribute('textContent')
            d.update(answers=answers)
            print answers
            selections = questionAndSelections[1].find_elements_by_tag_name("td");
            se = []
            for selection in selections:
                selectionContent = selection.get_attribute('textContent')
                se.append(selectionContent)
                print selectionContent
            d.update(title=title, answers=answers, selections=se)
            quetions.append(d)
        except:
            logging.info("out of range")
            pass
    # driver.quit()


threads = []
t1 = threading.Thread(target=yinyangWeb, args=("jiangyin", u'蒋英', "35～40岁以下", "男", "小学", "工人"))
threads.append(t1)
t2 = threading.Thread(target=yinyangWeb, args=("zhaowu", u'赵武', "35～40岁以下", "男", "小学", "工人"))
threads.append(t2)
t3 = threading.Thread(target=yinyangWeb, args=("wangliu", u'王柳', "35～40岁以下", "男", "小学", "工人"))
threads.append(t3)
t4 = threading.Thread(target=yinyangWeb, args=("zhansan", u'詹三', "35～40岁以下", "男", "小学", "工人"))
threads.append(t4)
t5 = threading.Thread(target=yinyangWeb, args=("zhutian", u'朱天', "35～40岁以下", "男", "小学", "工人"))
threads.append(t5)

if __name__ == '__main__':
    # 启动线程
    # for t in threads:
    #     t.start()
    # # 守护线程
    # for t in threads:
    #     t.join()
    #
    # conn = pymysql.connect(host="127.0.0.1", user="root", password="jiangying", database="test", charset="utf8")
    # # sql语句
    # sql = "insert into quetion (title, answers) values (%s,%s)"
    # # 获取游标
    # cur = conn.cursor()

    yinyangWeb("jiangyin", u'蒋英', "35～40岁以下", "男", "小学", "工人")

    for question in quetions:
        print question
        result = json.dumps(question).decode('unicode-escape')
        # 参数化方式传参
        # row_count = cur.execute(sql, [question['title'], question['answers']])
        # print "插入第" + str(row_count)
    # try:
    #     cur.commit()
    # except:
    #     cur.rollback()
    # cur.close()
    # conn.close()
    #
    # print('all end:', time.ctime())
