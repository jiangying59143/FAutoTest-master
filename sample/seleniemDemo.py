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
    PIC_SRC = os.path.join(dirPath, name + '_' + pic + '.png')
    logging.info('PIC_SRC ---> ' + PIC_SRC)
    driver.save_screenshot(PIC_SRC)


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


def yinyangWeb(list, name, age, sex, edu, metier):
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
    while isElementExistByXpath(driver, '//div[@name="text' + str(index+1) + '"]'):
        try:
            multipleflag = u"多选题" in driver.find_elements_by_xpath('//div[@name="text' + str(index+1) + '"]/div[1]/strong[1]')[0].text.strip();
            ids = []
            thisTitle = driver.find_elements_by_xpath('//div[@name="text' + str(index+1) + '"]/div[2]')[0].get_attribute('textContent').strip()
            for q in list:
                if q["title"] in thisTitle:
                    for a in q["answers"]:
                        ss = driver.find_elements_by_xpath('//div[@name="text' + str(index+1) + '"]/div')
                        for sl in ss:
                            for tl in sl.find_elements_by_xpath('div[@onclick="checkNew(this)"]'):
                                if a in tl.text:
                                    ll = tl.find_elements_by_xpath('../input[1]');
                                    if multipleflag:
                                        llid = ll[0].get_attribute("value")
                                    else:
                                        llid = ll[0].get_attribute("id")
                                    ids.append(llid)
            if len(ids) == 0:
                if multipleflag:
                    driver.find_elements_by_xpath('//input[@type="checkbox"][@value="A' + str(index) + '"]')[0].click()
                    driver.find_elements_by_xpath('//img[@id="Key_Next"][@onclick="down(' + str(index + 1) + ')"]')[0].click()
                else:
                    driver.find_element_by_id("A" + str(index)).click()
            else:
                print ids
                if multipleflag:
                    for id in ids:
                        driver.find_elements_by_xpath('//input[@type="checkbox"][@value="' + id + '"]')[0].click()
                    driver.find_elements_by_xpath('//img[@id="Key_Next"][@onclick="down(' + str(index + 1) + ')"]')[0].click()
                else:
                    driver.find_element_by_id(ids[0]).click()
            index = index + 1
        except Exception, e:
            logging.error("页面操作：" + str(e))
            break

    driver.find_element_by_id("Submit").click()
    confirm = driver.switch_to.alert
    time.sleep(1)
    confirm.accept()  # 接受
    alert = driver.switch_to.alert
    time.sleep(1)
    alert.accept()  # 确认
    time.sleep(1)
    screenshot(driver, "yinyang", name, "pic")
    # 查看成绩
    driver.find_element_by_id("BtnOk").click()
    screenshot(driver, "yinyang", name, "pic-chengji")
    questionlist = driver.find_elements_by_tag_name("table");
    for question in questionlist:
        try:
            d = {}
            questionAndSelections = question.find_elements_by_tag_name("tr");
            questionTitleAndAnswer = questionAndSelections[0].find_elements_by_tag_name("td");
            title = questionTitleAndAnswer[0].get_attribute('textContent').strip().split(".", 1)[1]

            answers = questionTitleAndAnswer[1].get_attribute('textContent')
            answers = answers.split(u"正确答案:")[1].split(u"回答答案:")[0].strip()

            cse = []
            for i in range(1, len(questionAndSelections)):
                selectionContent = questionAndSelections[i].get_attribute('textContent')
                selectionContent = selectionContent.strip()
                if selectionContent != "":
                    for c in answers:
                        if selectionContent.startswith(c):
                            cse.append(selectionContent[2:len(selectionContent)])
            d.update(title=title, answers=answers, selections=cse)
            quetions.append(d)
        except Exception, e:
            logging.error("收集题目答案：" + str(e))
            pass
    # driver.quit()



if __name__ == '__main__':
    conn = pymysql.connect(host="xxxxxx", user="xxxxx", password="xxxx", database="questionnaire", charset="utf8")
    # 获取游标
    cur = conn.cursor()
    selectSql = "select title, answers from health"
    cur.execute(selectSql)
    results = cur.fetchall()
    list = []
    for row in results:
        answers = row[1][2:(len(row[1])-2)]
        answerss = answers.split('", "')
        print json.dumps(answerss).decode('unicode-escape')
        dic = {"title": row[0][1:(len(row[0])-1)], "answers": answerss}
        list.append(dic)
    print "-----------------------------------------------------------"
    threads = []
    t1 = threading.Thread(target=yinyangWeb, args=(list, u'蒋英', "35～40岁以下", "男", "小学", "工人"))
    threads.append(t1)
    t2 = threading.Thread(target=yinyangWeb, args=(list, u'赵武', "35～40岁以下", "男", "小学", "工人"))
    threads.append(t2)
    t3 = threading.Thread(target=yinyangWeb, args=(list, u'王柳', "35～40岁以下", "男", "小学", "工人"))
    threads.append(t3)
    t4 = threading.Thread(target=yinyangWeb, args=(list, u'詹三', "35～40岁以下", "男", "小学", "工人"))
    threads.append(t4)
    t5 = threading.Thread(target=yinyangWeb, args=(list, u'朱天', "35～40岁以下", "男", "小学", "工人"))
    threads.append(t5)
    # 启动线程
    for t in threads:
        t.start()
    # 守护线程
    for t in threads:
        t.join()

    # sql语句
    sql = "insert into quetion (title, answers) values (%s,%s)"

    for question in quetions:
        result = json.dumps(question).decode('unicode-escape')
        # print result
        # 参数化方式传参
        try:
            row_count = cur.execute(sql, [json.dumps(question['title']).decode('unicode-escape'),
                                          json.dumps(question["selections"]).decode('unicode-escape')])
        except Exception, e:
            logging.error("数据库插入：" + str(e))
    try:
        conn.commit()
    except Exception, e:
        logging.error("数据库提交：" + str(e))
        conn.rollback()
    cur.close()
    conn.close()
    print('all end:', time.ctime())
