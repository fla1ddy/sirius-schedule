from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import sys, time, threading

import json
from collections import defaultdict

from config import GROUP, SEARCH_SELECTOR, TABLE_SELECTOR

def parsing():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://schedule.siriusuniversity.ru/list")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, SEARCH_SELECTOR))).click()
    driver.find_element(By.XPATH, '//*[@id="searchListInput"]').send_keys(GROUP)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchList"]/li'))).click()

    table = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, TABLE_SELECTOR)))
    days = table.find_elements(By.TAG_NAME, "tr")

    schedule = defaultdict(list)
    for day in days:
        date = day.find_element(By.CLASS_NAME, 'rasp-list-date').text
        schedule[date].append(
            {
                "start" : day.find_element(By.CLASS_NAME, 'rasp-list-start').text,
                "end" : day.find_element(By.CLASS_NAME, 'rasp-list-end').text,
                "discp" : day.find_element(By.CLASS_NAME, 'rasp-list-discp').text,
                "room" : day.find_element(By.CLASS_NAME, 'rasp-list-room').text,
                "teachers" : day.find_element(By.CLASS_NAME, 'rasp-list-teachers').text
            })
        
    with open(("response.json"), "w") as outfile:
         outfile.write(json.dumps(schedule, indent=4))

def animated_loading():
    chars = (r"/—\|")
    for char in chars:
        sys.stdout.write('\r'+'loading...'+char)
        time.sleep(.1)
        sys.stdout.flush() 

def main():
    pars = threading.Thread(name='parsing', target=parsing)
    pars.start()
    while pars.is_alive():
        animated_loading()