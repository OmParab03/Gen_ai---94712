from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

search=input("Enter the song name to search on YouTube: ")
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get("https://www.youtube.com/")
search_box = driver.find_element(By.NAME, "search_query")
search_box.send_keys(search)
search_box.send_keys(Keys.RETURN)
driver.find_elements(By.ID, "video-title")[0].click()

for _ in range(15):  
        try:
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "ytp-skip-ad-button"))
            ).click()
            print("Skipped ad")
            
            break
        except:
            time.sleep(2)

duration=driver.find_element(By.CLASS_NAME,"ytp-time-duration").text
parts=duration.split(":")

sec=0
for part in parts:
    sec=sec*60+int(part)
print(sec)
time.sleep(sec)
driver.quit()
