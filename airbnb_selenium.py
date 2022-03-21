from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as EX
from datetime import datetime
import time


def save_full_sc(driver, id):
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    # driver.save_screenshot(path)  # has scrollbar
    driver.find_element_by_tag_name('body').screenshot("fail_"+id+".png")


def check_dates(date1, date2):
    date_format = "%d.%m.%Y"
    result = 1
    try:
        temp1 = datetime.strptime(date1, date_format)
        temp2 = datetime.strptime(date2, date_format)
    except ValueError:
        result = 0
    return result


def airBNB_price(apartment_id, date1, date2):

    # Check if dates are in correct format
    if check_dates(date1, date2) == 0:
        return "Dates not in correct format"

    # Selenium Set Up
    chrome_opt = webdriver.ChromeOptions()
    chrome_opt.add_argument("--incognito")
    chrome_opt.add_argument("--ignore-certificate-errors")
    chrome_opt.add_argument('--headless')
    chrome_opt.add_argument("--disable-gpu")
    ser = Service("F:\\chromdriver\\chromedriver.exe")
    driver = webdriver.Chrome(service=ser, options=chrome_opt)

    # input Set up
    apartment_id = str(apartment_id)
    date_in = date1
    date_out = date2
    base_url = 'https://he.airbnb.com/rooms/'

    new_url = base_url + apartment_id
    driver.get(new_url)
    driver.implicitly_wait(5)

    # Pop Up Handler due to incognito
    try:
        driver.find_element(by='css selector', value="button[class='_1gnjopp0']").click()
    except EC.NoSuchElementException:
        pass

    # Check if Dates Side Bar Element of dates present (if it's a correct page or not)
    try:
        driver.find_element(by='css selector', value="div[data-plugin-in-point-id='BOOK_IT_SIDEBAR']")
    except EC.NoSuchElementException:
        return 'Wrong Page'

    # Insert dates
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='change-dates-checkIn']")))
    driver.find_element(by='css selector', value="div[data-testid='change-dates-checkIn']").click()
    driver.find_element(by='id', value="checkIn-book_it").send_keys(date_in)
    driver.find_element(by='id', value="checkOut-book_it").click()
    driver.find_element(by='id', value="checkOut-book_it").send_keys(date_out)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkOut-book_it")))
    try:
        driver.find_element(by='id', value="book_it_dateInputsErrorId")
    except EC.NoSuchElementException:
        return 'Dates did not inserted well'

    driver.find_element(by='id', value="checkOut-book_it").send_keys("\n")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "_hdznyn")))

    # Check if dates inserted correctly
    temp_check_in = driver.find_element(by='css selector', value="div[data-testid='change-dates-checkIn']").text
    temp_check_out = driver.find_element(by='css selector', value="div[data-testid='change-dates-checkOut']").text
    if temp_check_in != date_in or temp_check_out != date_out:
        return 'Dates did not inserted well'

    # Price Check
    price = driver.find_element(by='css selector', value="div[class='_hdznyn'] span[class='_1k4xcdh']").text
    driver.quit()
    return price


def airBNB_multi_price(apartment_id_str, date1, date2):
    # Check if dates are in correct format
    if check_dates(date1, date2) == 0:
        return {"Error": "Dates not in correct format"}

    # Selenium Set Up
    chrome_opt = webdriver.ChromeOptions()
    chrome_opt.add_argument("--incognito")
    chrome_opt.add_argument("--ignore-certificate-errors")
    # chrome_opt.add_argument("--headless")
    chrome_opt.add_argument("--start-maximized")
    chrome_opt.add_argument("--disable-gpu")
    ser = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=ser, options=chrome_opt)
    date_in = date1
    date_out = date2
    base_url = 'https://he.airbnb.com/rooms/'
    final = {}
    apartment_id_list = apartment_id_str.split(",")
    for apartment in apartment_id_list:
        apartment_id = str(apartment)
        new_url = base_url + apartment_id
        driver.get(new_url)

        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[data-plugin-in-point-id='BOOK_IT_SIDEBAR']")))
        except EC.NoSuchElementException or EX.TimeoutException:
            final[apartment_id] = 'Wrong Page'
            continue

        # Insert dates
        try:
            temp = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='change-dates-checkIn']")))
            time.sleep(1)
            driver.execute_script("arguments[0].click()", temp)
            # temp.click()

            # temp = "document.getElementById('checkIn-book_it').value="+date_in
            # driver.execute_script(temp)

            temp = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "checkIn-book_it")))
            temp.send_keys(date_in)
            # driver.find_element(by='id', value="checkIn-book_it").send_keys(date_in)
            try:
                driver.find_element(by='id', value="book_it_dateInputsErrorId")
                final[apartment_id] = 'Dates did not inserted well'
                continue
            except EC.NoSuchElementException:
                pass
            driver.find_element(by='id', value="checkOut-book_it").click()
            check_out_ele = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkOut-book_it")))
            check_out_ele.send_keys(date_out)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkOut-book_it")))
            driver.find_element(by='id', value="checkOut-book_it").send_keys("\n")
            try:
                driver.find_element(by='id', value="book_it_dateInputsErrorId")
                final[apartment_id] = 'Dates did not inserted well'
                continue
            except EC.NoSuchElementException:
                pass
            final[apartment_id] = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='_hdznyn'] span[class='_1k4xcdh']"))).text

        except EX.ElementClickInterceptedException or EX.NoSuchElementException or EX.StaleElementReferenceException:
            final[apartment_id] = 'Server Fail, see screenshot'
            save_full_sc(driver, apartment_id)

        # Price Check
        # final[apartment_id] = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='_hdznyn'] span[class='_1k4xcdh']"))).text

    driver.quit()
    return final
