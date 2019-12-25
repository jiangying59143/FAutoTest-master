# coding=utf-8
'''
Tencent is pleased to support the open source community by making FAutoTest available.
Copyright (C) 2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

'''
import copy

from pip._vendor.pep517.dirtools import mkdir_p

from fastAutoTest.core.h5.h5Engine import H5Driver
import time
import os
import pymysql

# http://h5.baike.qq.com/mobile/enter.html 从微信进入此链接，首屏加载完后执行脚本
from sample.Person import Person


def picker(h5Driver, seletXpath, singleHeight, closeXpath, *itemxpaths):
    h5Driver.clickElementByXpath(seletXpath)
    time.sleep(1)
    for itemxpath in itemxpaths:
        h5Driver.scrollPickerByXpath(itemxpath, singleHeight)
    time.sleep(1)
    h5Driver.clickElementByXpath(closeXpath)


def selector(h5Driver, seletXpath, itemxpath):
    h5Driver.clickElementByXpath(seletXpath)
    time.sleep(1)
    h5Driver.clickElementByXpath(itemxpath)
    time.sleep(1)


def textor(h5Driver, xpath, text):
    if not h5Driver.isElementExist(xpath + '[@value="' + text + '"]'):
        h5Driver.clearInputTextByXpath(xpath)
        h5Driver.textElementByXpath(xpath, text)
        time.sleep(1)


def personPage(h5Driver, person):
    # 个人信息页面
    while not h5Driver.isElementExist('//h1[@class="demos-title"][text()="个人信息"]'):
        time.sleep(1)
    if not h5Driver.isElementExist('//input[@name="examinee.gbnameLevel4"][@value="' + person.areas[2] + '"]'):
        picker(h5Driver, '//*[@id="gbcode"]', 32, '*//a[text()="完成"]',
               '//div[@class="picker-item"][text()="' + person.areas[0] + '"]',
               '//div[@class="picker-item"][text()="' + person.areas[1] + '"]',
               '//div[@class="picker-item"][text()="' + person.areas[2] + '"]')
    # 姓名
    textor(h5Driver, '//*[@id="name"]', person.name)
    if not h5Driver.isElementExist('//input[@name="examinee.age"][@value="' + person.age + '"]'):
        selector(h5Driver, '//*[@id="age"]', '//p[text()="' + person.age + '"]')
    if not h5Driver.isElementExist('//input[@name="examinee.sex"][@value="' + person.sex + '"]'):
        selector(h5Driver, '//*[@id="sex"]', '//p[text()="' + person.sex + '"]')
    if not h5Driver.isElementExist('//input[@name="examinee.education"][@value="' + person.edu + '"]'):
        selector(h5Driver, '//*[@id="education"]', '//p[text()="' + person.edu + '"]')
    if not h5Driver.isElementExist('//input[@name="examinee.metier"][@value="' + person.metier + '"]'):
        selector(h5Driver, '//*[@id="metier"]', '//p[text()="' + person.metier + '"]')
    textor(h5Driver, '//*[@id="organ"]', person.organ)
    h5Driver.clickElementByXpath('//div[@class="submit_btn"]')


def exam(h5Driver):
    i = 1
    while h5Driver.isElementExist('//div[@id="exam_div"]/div[@index="' + str(i) + '"]'):
        h5Driver.clickElementByXpath('//div[@id="exam_div"]/div[@index="' + str(i) + '"]/div[2]/div[1]')
        h5Driver.clickElementByXpath('//div[@id="exam_div"]/div[@index="' + str(i) + '"]/div[3]/a[1]')
        i = i + 1
    h5Driver.clickElementByXpath('//a[text()="提交试卷"]')
    h5Driver.clickElementByXpath('//a[text()="确定"]')


def screenshot(h5Driver, appname, name, pic):
    dirPath = os.path.split(os.path.realpath(__file__))[0] + "/" + appname
    mkdir_p(dirPath)
    dirPath = dirPath + "/" + name
    mkdir_p(dirPath)
    PIC_SRC = os.path.join(dirPath, pic + '.png')
    h5Driver.logger.info('PIC_SRC ---> ' + PIC_SRC)
    h5Driver.d.screenshot(PIC_SRC)


if __name__ == '__main__':
    h5Driver = H5Driver()
    h5Driver.initDriver()
    # 点击素养学习
    h5Driver.clickElementByXpath("/html/body/div[1]/img[1]")

    person1 = Person(["宿迁市", "沭阳县", "东小店乡"], "jiangyin", "蒋英", "35～40岁以下", "男", "小学", "工人", "东小店乡谢圩村")
    person2 = copy.deepcopy(person1)
    person2.ename = "wanghui"
    person2.name = "王辉"
    persons = [person1, person2]

    for person in persons:
        loop_times = 1
        for i in range(loop_times):
            personPage(h5Driver, person)
            exam(h5Driver)
            while not h5Driver.isElementExist('//img[@src="we_resources/images/btn_study.png"]'):
                time.sleep(1)
            screenshot(h5Driver, "health", person.ename, "pic" + str(i+1))
            h5Driver.clickElementByXpath('//img[@src="we_resources/images/btn_study.png"]')

