from selenium import webdriver
from selenium.webdriver.chrome.service import Service

chrome_opt = webdriver.ChromeOptions()
chrome_opt.add_argument("--incognito")
chrome_opt.add_argument("--ignore-certificate-errors")
ser = Service("F:\\chromdriver\\chromedriver.exe")
driver = webdriver.Chrome(service=ser, options=chrome_opt)
url = "https://he.airbnb.com/s/Israel/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=april&flexible_trip_dates%5B%5D=march&flexible_trip_lengths%5B%5D=weekend_trip&date_picker_type=calendar&query=Israel&place_id=ChIJi8mnMiRJABURuiw1EyBCa2o&source=structured_search_input_header&search_type=autocomplete_click"
driver.get(url)
apartments_ele = driver.find_elements(by='css selector', value="div[class='_1e9w8hic']")
id_list = []
for ii in apartments_ele:
    apartment = ii.find_element(by='tag name', value="a")
    temp = apartment.get_attribute("aria-labelledby")
    print(temp)


driver.quit()
