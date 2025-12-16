from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options=Options()
chrome_options.add_argument("--headless=new")
dr=webdriver.Chrome(options=chrome_options)
dr.implicitly_wait(5)

dr.get("https://www.sunbeaminfo.in/internship")
print("page title", dr.title)


table1=dr.find_element(By.CSS_SELECTOR,"table.table.table-bordered.table-striped")

body=table1.find_element(By.TAG_NAME,"tbody")
rows = body.find_elements(By.TAG_NAME,"tr")

for row in rows:
    cols = row.find_elements(By.TAG_NAME,"td")
    if len(cols)<7:
        continue
    info={
            "sr":cols[0].text,
            "batch":cols[1].text,
            "batch duration":cols[2].text,
            "start date":cols[3].text,
            "End date":cols[4].text,
            "time":cols[5].text,
            "fees":cols[6].text
        }
    print(info)
    
    


print("\n table2: \n")  
    
    
wait=WebDriverWait(dr,10)
# Scroll to the bottom (makes sure that dynamic contents load)
dr.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# wait for and click the "Available Internship Programs" toggle button
plus_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']")))
dr.execute_script("arguments[0].scrollIntoView(true);", plus_button)
plus_button.click()


table2=dr.find_element(By.ID,value="collapseSix")
tbody=table2.find_element(By.TAG_NAME,"tbody")
rows=tbody.find_elements(By.TAG_NAME,"tr")


for row in rows:
    cols=row.find_elements(By.TAG_NAME,"td")
    info={
        "Technology":cols[0].text,
        "Aim":cols[1].text,
        "Prerequisite":cols[2].text,
        "Learning":cols[3].text,
        "Location":cols[4].text,
       
    }
    print(info)

dr.quit()
