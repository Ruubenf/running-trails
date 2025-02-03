from requests import get
from time import sleep
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

PAGES = 1

ids = ['1165636', '1164742']
"""
for i in range(PAGES):
    url = f"https://www.plotaroute.com/routes/running/popular/{i+1}?Locality=Lisboa&CCode=PT"

    file = get(url)

    # Get table with id RoutesTab
    soup = bs(file.content, 'html.parser')

    table = soup.find(id='RoutesTab')

    # For each tr without class, get the content of its first td
    for tr in table.find_all('tr', class_=False):
        try:
            ids.append(tr.find('td').text)
        except:
            pass
"""
print(ids)


# Create selenium driver
options = Options()
options.add_experimental_option("prefs", {
  "download.default_directory": r"./files",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})
driver = webdriver.Chrome(options=options)
ac = ActionChains(driver)

# Full screen
driver.maximize_window()

first_run = True


for id in ids:
    url = f"https://www.plotaroute.com/route/{id}"

    # Get the page
    driver.get(url)

    # Wait for a couple of seconds
    sleep(2)

    if first_run:
        # Accept cookies with button /html/body/div[1]/div/div/div/div[2]/div/button[2]
        driver.find_element('xpath', '/html/body/div[1]/div/div/div/div[2]/div/button[2]').click()
        first_run = False

    # Press the download button $("#DownloadBut").trigger("click")
    driver.execute_script('$("#DL_Format_KML").trigger("click")')

    # Wait for a couple of seconds
    sleep(2)

    # Press the other download button with doc
    elem = driver.find_element('xpath', '//*[@id="RatingStats"]')
    #show the text of the span inside the element
    #print(elem.find_element('xpath', './/span').text)

    # Target coords x: 582.171875, y: 259
    # Elem coords x: 681.921875, y: 536.59375

    ac.move_to_element(elem).move_by_offset(-100, -277).click().perform() 


    #download_button = driver.find_element('xpath', '//*[@id="DownloadBut"]')
    #download_button.click()
    #driver.execute_script('$("#DownloadBut").trigger("click")')
    #driver.execute_script('$document.getElementsByClassName("button highbut right margin-t10")[0].click()')

    # Wait for a couple of seconds
    sleep(1)    

# Close the driver

driver.close()

