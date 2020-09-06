# by 1xcld

import json
from msedge.selenium_tools import Edge, EdgeOptions
import time
from down import downloadFile
from shutil import copy, rmtree
import os
from tqdm import tqdm

def chooseMenu():
    print("INSTAGRAM IMAGE DOWNLOADER by 1xcld®")
    print("version 1.0.0")
    print("1. Login")
    print("2. Choose account")
    print("3. Enter link of image")
    key = input()

key = 21
key = int(key)
path = './data.txt'
if (os.path.isfile(path)):
    key = 2
else:
    key = 1

def login():
    print("one time login and data is save to the database")
    print("username:")
    userName = input()
    print("password:")
    passWord = input()

    dataLogin = {'username': userName, 'password': passWord}
    with open('data.txt', 'w') as outfile:
        json.dump(dataLogin, outfile)

    chooseMenu()
    if (os.path.isfile(path)):
        key = 2
    else:
        key = 1
    menu(key)


def chooseAccount():
    with open('data.txt') as json_file:
        data = json.load(json_file)

    userInfo ='account: ' + data['username']
    print(userInfo) 
    
    userName = data['username']
    passWord = data['password']
    print("link:")
    link = input()
    print("number of photos: ")
    amount = input()

    # format text and amount
    amount = int(amount)

    # auto login
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument('headless')
    driver = Edge('msedgedriver', options = options)
    driver.get(link)
    time.sleep(2)
    userForm = driver.find_element_by_css_selector("input[name='username']")
    passForm = driver.find_element_by_css_selector("input[name='password']")
    userForm.send_keys(userName)
    passForm.send_keys(passWord)
    driver.find_element_by_css_selector("button[type='submit']").click()
    time.sleep(3)
    driver.execute_script("document.querySelector('.sqdOP.yWX7d.y3zKF').click()")

    # get link image to list
    time.sleep(2)
    if amount > 1: 
        spriteBtn = driver.find_element_by_css_selector(".coreSpriteRightChevron")
    list_link = []
    def get_url1():
        list_element = driver.find_elements_by_css_selector("img[style='object-fit: cover;']")
        for image in list_element[:1]:
            src = image.get_attribute("src")
            list_link.append(src)
    def get_url2():
        list_element = driver.find_elements_by_css_selector("img[style='object-fit: cover;']")
        list_element.pop(0)
        for image in list_element[:1]:
            src = image.get_attribute("src")
            list_link.append(src)

    for x in range(0, amount+1):
        if (len(list_link) > 0):
            get_url2()
        else:
            get_url1()
        if len(list_link) == amount:
            break
        elif spriteBtn:
            spriteBtn.click()
        else:
            break
        time.sleep(0.5)

    # check old image folder exist
    if (os.path.isdir("./image")): 
        rmtree("./image")

    # create new image folder
    folderPath = os.getcwd()
    folderPath += '\image'
    os.mkdir(folderPath)

    # clear screen
    clear = lambda: os.system('cls')
    clear()

    for i in tqdm(range(100)):
        pass

    print("\nnumber of photos:", len(list_link))

    pos = 0
    for href in list_link:
        print(pos+1, "DONE")
        imagePathResult = "./image/image_" + str(pos) + ".png"
        try:
            downloadFile(href)
            copy("./image/image.png", imagePathResult)
        except:
            print("error at %s" %pos+1)
        pos += 1
    os.remove("./image/image.png")

    resultPath = os.getcwd()
    resultPath = resultPath + '\image'
    os.startfile(resultPath)
    
    driver.close()
    chooseMenu()
    if (os.path.isfile(path)):
        key = 2
    else:
        key = 1
    menu(key)



def openLink():
    chooseMenu()
    if (os.path.isfile(path)):
        key = 2
    else:
        key = 1
    menu(key)


def menu(key):
    switcher = {
        1: login,
        2: chooseAccount,
        3: openLink
    }

    func = switcher.get(key)
    return func()

chooseMenu()
menu(key)

