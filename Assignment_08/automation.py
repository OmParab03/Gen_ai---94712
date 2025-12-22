import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

COMMAND_FILE = "commands.txt"

def play_video(search):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    driver.get("https://www.youtube.com")

    
    search_box = wait.until(
        EC.presence_of_element_located((By.NAME, "search_query"))
    )
    search_box.send_keys(search)
    search_box.send_keys(Keys.RETURN)

    
    first_video = wait.until(
        EC.element_to_be_clickable((By.ID, "video-title"))
    )
    first_video.click()

    print(f"▶ Playing: {search}")

    
    end_time = time.time() + 30
    while time.time() < end_time:
        try:
            skip_btn = driver.find_element(By.CLASS_NAME, "ytp-skip-ad-button")
            skip_btn.click()
            print("⏭ Ad skipped")
            break
        except:
            time.sleep(2)
COMMAND_FILE = "commands.txt"

def chrome_search(search):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")
    box = driver.find_element(By.NAME, "q")
    box.send_keys(search)
    box.send_keys(Keys.RETURN)
    print(f"Searched🔍: {search}")

while True:
    time.sleep(2)

    with open(COMMAND_FILE, "r") as f:
        lines = f.readlines()

    if not lines:
        continue

    command = lines.pop(0).strip()

    with open(COMMAND_FILE, "w") as f:
        f.writelines(lines)
    if command.startswith("PLAY::"):
        search = command.replace("PLAY::", "").strip()
        play_video(search)
    elif command.startswith("SEARCH::"):
        search = command.replace("SEARCH::", "").strip()
        chrome_search(search)
