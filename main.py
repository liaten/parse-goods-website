# https://www.tomtop.com/p-pz0061b-eu-6-64.html
# IMPORTS
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from sys import argv
from sys import exit
from itertools import product # размещения
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from requests import get
from urllib.parse import urlparse
# import os
from os.path import basename
from shutil import copy2
#####################################


def element_init_by_xpath(driver, xpath):
    try:
        elem = driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        # print("ELEMENT NOT FOUND BY XPATH: " + xpath)
        return None
    return elem


def elements_init_by_xpath(driver, xpath):
    try:
        elem = driver.find_elements(By.XPATH, xpath)
    except NoSuchElementException:
        # print("ELEMENTS NOT FOUND BY XPATH: " + xpath)
        return None
    return elem

def click(driver, xpath_o):
    WebDriverWait(driver=driver, timeout=1000000).until(EC.element_to_be_clickable((By.XPATH,xpath_o))).click()


if(len(argv)>2 or len(argv)==1 or argv[1]=="--help" or argv[1]=='-h'):
    if(len(argv)>2):
        print("WRONG USAGE. MORE THAN 1 ARGUMENT\n")
    print("SCRIPT USAGE\npython ./main.py [URL] [element] [\nEXAMPLE:\npython ./main.py \"https://ya.ru\"")
    exit(0)


# MAIN SCRIPT

# get the args from command line
url = argv[1]
# url = "https://www.tomtop.com/ru/p-h11111.html"
# url = "https://www.tomtop.com/p-pz0270b-eu.html"

# buttons bind to set locale settings, all single
xpath_country_button_main = "//div[@class='m_chose_country']"
xpath_language_option = "//div[@class='lang_part']/div[@class='bm_option']"
xpath_language_option_ru = "//div[@class='lang_part']/div[@class='bm_option']/div[@class='option_list']/a[@title='Русский']"
xpath_language_option_en = "//div[@class='lang_part']/div[@class='bm_option']/div[@class='option_list']/a[@title='English']"
xpath_pulldown_country = "//div[@class='bm_dialog m_shipto_wrap_dialog hide dialog_show']//div[@class='m_pullDown_country']"
xpath_pulldown_country_ru = "//div[@class='bm_dialog m_shipto_wrap_dialog hide dialog_show']//div[@class='m_pullDown_country openD']/div[@class='m_more_country']/ul/li[@class='RU']"
xpath_pulldown_country_us = "//div[@class='bm_dialog m_shipto_wrap_dialog hide dialog_show']//div[@class='m_pullDown_country openD']/div[@class='m_more_country']/ul/li[@class='US']"
xpath_currency = "//div[@class='bm_dialog m_shipto_wrap_dialog hide dialog_show']//div[@class='currency_part']//div[@class='result']"
xpath_currency_rub = "//div[@class='bm_dialog m_shipto_wrap_dialog hide dialog_show']//div[@class='currency_part']//div[@class='option_list']/a[@data-currency='RUB']"
xpath_currency_usd = "//div[@class='bm_dialog m_shipto_wrap_dialog hide dialog_show']//div[@class='currency_part']//div[@class='option_list']/a[@data-currency='USD']"
xpath_button_save = "//div[@class='bm_dialog m_shipto_wrap_dialog hide dialog_show']//div[@class='m_shipto_wrap']//div[@class='btn_wrap']//div[@class='btn_save']/a"
xpath_button_cookies = "//input[@class='bm_btn_A minor']"

# имя
xpath_name_main = "//div[@class='lineBlock showInformation']/h1/span" # single
# продолжение имени
xpath_name_sub = "//div[@class='lineBlock showInformation']/h2[@class='sub_title']" # single
# цена распродажи
xpath_sale_price = "//div[@class='lineBlock showInformation']//p[@id='detailPrice']" # single
# обычная цена
xpath_regular_price = "//div[@class='lineBlock showInformation']//div[@class='saleWarp']//span[@id='d_origprice']" # single
# кол-во продаж
xpath_product_sold = "//div[@class='lineBlock showInformation']//div[@class='m_sales_promotion']//span[@class='pro_sell']" # single
# кол-во на складе
xpath_product_count = "//div[@class='lineBlock showInformation']//div[@class='m_sales_promotion']//span[@class='pro_count']" # single
# описание
xpath_description = "//section[@class='contentInside proInfWarp lbBox']//div[@id='description']" # single
# рейтинг
xpath_rating_value = "//div[@class='lineBlock showInformation']//div[@class='productReviews lineBlock']//span[@itemprop='ratingValue']" # single
# кол-во отзывов
xpath_review_count = "//div[@class='lineBlock showInformation']//span[@itemprop='reviewCount']" # single
# опции товара
xpath_options = "//div[@class='m_item_wrap color']" # multi
# название опции
xpath_option_name = ".//p[@class='item_line proColor']//span" # single
# названия опций опций
xpath_options_of_options_name = ".//div[@class='item_box']/ul/li" # multi, получать data-attr-value
# доставка
xpath_logistics = "//span[@class='logistics_b']" # single
# div со складами (может быть несколько)
xpath_shipping_from = "//div[@class='m_item_wrap shippingFrom']" # single
# итемы ul/li в диве со складами
xpath_warehouses = ".//div[@class='item_box']/ul/li[contains(@class,'lineBlock') and not(contains (@class,'invalids'))]" # multi
# итемы tr в методах отправки
xpath_shipping_methods = "//tr[contains(@class,'sel_b')]"
# кнопка закрытия диалогового окна с методами отправки
xpath_close_shipping = "//div[@class='dialogs logistics_c dialogs_show']//span[@class='dialogs_c']//i[@class='close_dialogs']"
# Name of option
xpath_name_of_option = "./td[2]/a"
# Estimated shipping time
xpath_shipping_time = "./td[3]/a"
# Tracking number
xpath_tracking_number = "./td[4]"
# Shipping cost
xpath_shipping_cost = "./td[5]"
# Main image
xpath_main_image = "//li[contains(@class,'cpActive')]/a"

opts = Options()
opts.headless = True
opts.set_preference('intl.accept_languages', 'ru-RU')
opts.add_argument("--width=1800")
opts.add_argument("--height=900")
opts.set_preference("network.cookie.cookieBehavior", 0)
opts.set_preference("media.navigator.enabled", False)
opts.set_preference("privacy.firstparty.isolate", True)
opts.set_preference("browser.cache.offline.enable", False)
opts.set_preference("browser.send_pings", False)
opts.set_preference("browser.sessionstore.max_tabs_undo", 0)
opts.set_preference("browser.urlbar.speculativeConnect.enabled", False)
opts.set_preference("dom.battery.enabled", False)
opts.set_preference("dom.event.clipboardevents.enabled", False)
opts.set_preference("geo.enabled", False)
opts.set_preference("media.navigator.enabled", False)
opts.set_preference("network.cookie.lifetimePolicy", 2)
opts.set_preference("network.http.referer.trimmingPolicy", 2)
opts.set_preference("network.http.referer.XOriginPolicy", 2)
opts.set_preference("network.http.referer.XOriginTrimmingPolicy", 2)
opts.set_preference("webgl.disabled", True)
opts.set_preference("general.useragent.override","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0")
opts.binary_location = "C:/Program Files/Firefox Developer Edition/firefox.exe"


driver = Firefox(options=opts,service=Service("./geckodriver.exe"))

ublock_path = "./ublock.xpi"
driver.install_addon(path=ublock_path,temporary=True)
driver.get(url)

# соглашаемся с политикой получения печенек
# element_init_by_xpath(driver=driver,xpath=xpath_button_cookies).click()
click(driver=driver,xpath_o=xpath_button_cookies)

# устанавливаем локаль
click(driver=driver,xpath_o=xpath_country_button_main)
# print("Нажали на кнопку выбора языка № 1")
click(driver=driver,xpath_o=xpath_language_option)
# print("Нажали на кнопку выбора языка № 2")
click(driver=driver,xpath_o=xpath_language_option_en)
# print("Нажали на кнопку выбора языка № 3")
click(driver=driver,xpath_o=xpath_pulldown_country)
# print("Нажали на кнопку выбора страны № 1")
click(driver=driver,xpath_o=xpath_pulldown_country_us)
# print("Нажали на кнопку выбора страны № 2")
click(driver=driver,xpath_o=xpath_currency)
# print("Нажали на кнопку выбора валюты № 1")
click(driver=driver,xpath_o=xpath_currency_usd)
# print("Нажали на кнопку выбора валюты № 2")
click(driver=driver,xpath_o=xpath_button_save)


# print("Получаем атрибуты")

name = element_init_by_xpath(driver=driver,xpath=xpath_name_main).text + " " + element_init_by_xpath(driver=driver,xpath=xpath_name_sub).text
data = {}
data['name'] = name
# print("Название: " + name)

desctiption = element_init_by_xpath(driver=driver,xpath=xpath_description).text
data['desctiption'] = desctiption
# print("Описание: " + desctiption)

if(element_init_by_xpath(driver=driver,xpath=xpath_rating_value)!=None):
    rating = element_init_by_xpath(driver=driver,xpath=xpath_rating_value).get_attribute("textContent")
    review_count = element_init_by_xpath(driver=driver,xpath=xpath_review_count).text
    data['rating'] = str(rating + " (" + review_count + " отзывов)")
    # print("Рейтинг: " + rating + " (" + review_count + " отзывов)")
else:
    # print("Рейтинг не распознан")
    pass

if(element_init_by_xpath(driver=driver,xpath=xpath_product_count)!=None):
    product_count = element_init_by_xpath(driver=driver,xpath=xpath_product_count).text
    product_sold = element_init_by_xpath(driver=driver,xpath=xpath_product_sold).text
    # print("Продано стандартного товара: " + product_sold + "/" + product_count)
    data['product_sold'] = product_sold
    data['product_count'] = product_count
else:
    # print("Продажи не распознаны")
    pass

if(elements_init_by_xpath(driver=driver,xpath=xpath_options)!=None):
    item_options = elements_init_by_xpath(driver=driver,xpath=xpath_options)
    options_lists = []
    # print("Опции товара:")
    data['options'] = {}
    options_counter = 0
    for option in item_options:
        options_counter+=1
        option_name = element_init_by_xpath(option,xpath_option_name).text
        data['options'][option_name] = {}
        # print(options_counter,option_name)
        if(elements_init_by_xpath(driver=option,xpath=xpath_options_of_options_name)!=None):
            options_of_option = elements_init_by_xpath(option,xpath_options_of_options_name)
            temp = []
            option_of_option_counter = 0
            for option_of_option in options_of_option:
                option_of_option_counter+=1
                option_of_option_name = option_of_option.get_attribute("data-attr-value")
                data['options'][option_name][option_of_option_counter] = option_of_option_name
                # print(str(options_counter)+"."+str(option_of_option_counter)+": "+option_of_option_name)
                temp.append(option_of_option)
            options_lists.append(temp)
    perestanovki = product(*options_lists)
    p_counter = 0
    data['perestanovki'] = {}
    for p in perestanovki:
        p_counter+=1
        data['perestanovki'][p_counter] = {}
        # print("Перестановка атрибутов товара № " + str(p_counter) + ":")
        web_element_counter = 0
        for web_element in p:
            web_element_counter+=1
            web_element.click()
            data['perestanovki'][p_counter][web_element_counter] = {}
            data['perestanovki'][p_counter][web_element_counter] = (web_element.get_attribute("data-attr-value"))
            # print(web_element.get_attribute("data-attr-value"))

        sale_price_rub = element_init_by_xpath(driver=driver,xpath=xpath_sale_price).text
        sale_price_usd = element_init_by_xpath(driver=driver,xpath=xpath_sale_price).get_attribute("usvalue")

        data['perestanovki'][p_counter]['price'] = {}
        if(element_init_by_xpath(driver=driver,xpath=xpath_regular_price)!=None):
            regular_price_rub = element_init_by_xpath(driver=driver,xpath=xpath_regular_price).text
            regular_price_usd = element_init_by_xpath(driver=driver,xpath=xpath_regular_price).get_attribute("usvalue")
            data['perestanovki'][p_counter]['price'] = ("Цена: " + regular_price_rub + " USD. (" + regular_price_usd + "$)" + "\nЦена распродажи: " + sale_price_rub + " USD. (" + sale_price_usd + "$)")
            # data['perestanovki'][p_counter].append("Цена: " + regular_price_rub + " USD. (" + regular_price_usd + "$)" + "\nЦена распродажи: " + sale_price_rub + " USD. (" + sale_price_usd + "$)")
            # print("Цена: " + regular_price_rub + " USD. (" + regular_price_usd + "$)")
            # print("Цена распродажи: " + sale_price_rub + " USD. (" + sale_price_usd + "$)")
        else:
            data['perestanovki'][p_counter]['price'] = ("Распродажа не проходит по данному товару\nОбычная цена: " + sale_price_rub + " USD. (" + sale_price_usd + "$)")
            # pass
            # data['perestanovki'][p_counter].append("Распродажа не проходит по данному товару\nОбычная цена: " + sale_price_rub + " USD. (" + sale_price_usd + "$)")
            # print("Распродажа не проходит по данному товару")
            # print("Обычная цена: " + sale_price_rub + " USD. (" + sale_price_usd + "$)")
        
        shipping_from = element_init_by_xpath(driver=driver,xpath=xpath_shipping_from)
        warehouses = elements_init_by_xpath(driver=shipping_from,xpath=xpath_warehouses)

        data['perestanovki'][p_counter]['warehouses'] = {}
        for warehouse in warehouses:
            warehouse.click()
            data['perestanovki'][p_counter]['warehouses'][warehouse.get_attribute("title")] = []
            # print(warehouse.get_attribute("title"))
            WebDriverWait(driver=driver, timeout=1000000).until(EC.element_to_be_clickable((By.XPATH,xpath_logistics))).click()
            shipping_methods = elements_init_by_xpath(driver=driver,xpath=xpath_shipping_methods)
            if(len(shipping_methods)==0):
                data['perestanovki'][p_counter]['warehouses'][warehouse.get_attribute("title")].append("Нет доставок из этого склада")
                # print("Нет доставок из этого склада")
            else:
                for single_shipping_method in shipping_methods:
                    name_of_option = element_init_by_xpath(driver=single_shipping_method,xpath=xpath_name_of_option).get_attribute("textContent")
                    estimated_shipping_time = element_init_by_xpath(driver=single_shipping_method,xpath=xpath_shipping_time).get_attribute("textContent")
                    tracking_number = element_init_by_xpath(driver=single_shipping_method,xpath=xpath_tracking_number).get_attribute("textContent")
                    shipping_cost = element_init_by_xpath(driver=single_shipping_method,xpath=xpath_shipping_cost).get_attribute("textContent")
                    data['perestanovki'][p_counter]['warehouses'][warehouse.get_attribute("title")].append("Название: " + name_of_option + "\nПриблизительное время доставки: " + estimated_shipping_time + "\nТрекинг: " + tracking_number + "\nСтоимость доставки: " + shipping_cost)
                    # print("Название: ",name_of_option, "Приблизительное время доставки: ",estimated_shipping_time, "Трекинг: ", tracking_number, "Стоимость доставки:",shipping_cost)
            WebDriverWait(driver=driver, timeout=1000000).until(EC.element_to_be_clickable((By.XPATH,xpath_close_shipping))).click()
        # print()
else:
    # print("Опции товара не распознаны")
    pass

# main_image_web_el = element_init_by_xpath(driver=driver,xpath=xpath_main_image)
# image_url = element_init_by_xpath(driver=driver,xpath=xpath_main_image).get_attribute("href")
data['image_url'] = element_init_by_xpath(driver=driver,xpath=xpath_main_image).get_attribute("href")
data['url'] = url


img_data = get(data['image_url']).content
img_name = basename(urlparse(data['image_url']).path)
data['image_name'] = img_name
with open(img_name,'wb') as handler:
    handler.write(img_data)


copy2('./'+img_name, r'C:\\nginx\\html\\wordpress\\img')

data['image_local_url'] = 'https://liaten.ru/img/' + img_name

json_data = json.dumps(data)
print(json_data)


driver.close()
