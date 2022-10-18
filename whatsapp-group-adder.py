from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import csv

group_name=""
file_location=""

chrome_options = Options()
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://web.whatsapp.com/')

#wait 60 secs to allow for the user to manually scan the Whatsapp Web QR code to log on
el_side = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "side")))

#locate the search box
el_search = el_side.find_element(By.XPATH, "//div[contains(@title, 'Search')]")
print("Logged in and located search box:", el_search)


#define a helper function
def click_modal_button(button_text):    
    modal_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']//div[@role='button']//div[text() = '%s']" % (button_text))))
    modal_button.click()     


def add_contact_to_group(group_name, contact_to_add):        
    #click on the Add Participant button
    el_add_participant = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='drawer-right']//div[text() = 'Add participant']")))
    el_add_participant.click()    
    
    #click on the Search
    el_modal_popup = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']")))    
    el_modal_popup.find_element(By.XPATH, "//div[contains(@title, 'Search')]").send_keys(contact_to_add.rstrip())
    
    #click on the Contact
    el_contact_to_add = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']//span[@title='%s']" % (contact_to_add.rstrip()))))
    el_contact_to_add.click()    
    
    #check whether already added
    if len(el_modal_popup.find_elements(By.XPATH, "//div[text() = 'Already added to group']")) > 0:
        print(contact_to_add + ' was already an existing participant of ' + group_name)
        el_modal_popup.find_element(By.XPATH, "//header//button[@aria-label='Close']").click()
    else:    
        #click on the Green Check Mark
        el_green_check = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-animate-modal-body='true']//div[@role='button']//span[@data-testid='checkmark-medium']")))
        el_green_check.click()        

        #click on the Add Participant
        click_modal_button('Add participant')
        print(contact_to_add + ' added to ' + group_name)


with open(file_location, 'r') as fp:
    reader = csv.reader(fp)

    el_search.find_element(By.XPATH, "//div[contains(@title, 'Search')]").send_keys(group_name)
    time.sleep(5)
    #find chat with the correct title

    el_target_chat = driver.find_element(By.XPATH, "//div[@id='pane-side']").find_element(By.XPATH, "//span[@title='%s']" % (group_name))
    # el_target_chat = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@title='%s']" % (group_name))))
    el_target_chat.click()
    #wait for it to load by detecting that the header changed with the new title
    el_header_title = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//header//span[@title='%s']" % (group_name))))

    #click on the menu button
    el_menu_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main']//div[@data-testid='conversation-menu-button']")))
    el_menu_button.click()

    #click on the Group Info button
    el_group_info = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='app']//li//div[@aria-label='Group info']")))
    el_group_info.click()
    for row in reader:
        try:
            add_contact_to_group(group_name, row[0])
        except:
            continue
