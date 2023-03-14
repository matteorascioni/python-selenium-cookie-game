# Before to run this program, run this commands:
# python -m venv
# pip3 install selenium
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Selenium Driver setup
chrome_driver_path = "" # <-- Your chromedriver folder path
service = Service(executable_path=chrome_driver_path)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Get the endpoint to scrape
driver.get('http://orteil.dashnet.org/experiments/cookie/')

game_is_on = True
time_out = time.time() + 5
total_game_duration = time.time() + (60 * 5) # <-- You can change the duration of your game here
cookie = driver.find_element(By.ID, "cookie")


def buy_items():
    """ This function check if the money of the player are enough to buy the items on the right panel """
    # Get the items price on the right panel.
    item_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
    for item in reversed(item_prices):
        if item.text != "":
            # formatting the item string to get just the number inside of it.
            price = int(item.text.replace(",", "").split("-")[1].replace(" ", ""))
            # formatting the item string to get just the id of the html element.
            item_id = item.text.split("-")[0].replace(" -  ", "").rstrip()
            final_id = f"buy{item_id}"

            # if the money are more or equal of the price let's assign the final_id to the store item and makes the click.
            if money >= price:
                store_item = driver.find_element(By.ID, final_id)
                store_item.click()
                print(f"buying {item_id}")
                return

while game_is_on:
    # Get the cookie count element as money.
    money = int(driver.find_element(By.ID, "money").text.replace(",", ""))
    cookie.click()

    # Enter this block every 5 seconds
    if time.time() > time_out:
        buy_items()
        time_out = time.time() + 5
        # Ends the game if the time is more than 5 minutes (see total_game_duration)
        if time.time() > total_game_duration:
            game_is_on = False
            cookie_per_min = driver.find_element(By.ID, "cps")
            print(cookie_per_min)

driver.close()