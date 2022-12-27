import subprocess
import undetected_chromedriver as uc
import time  
import random
import pyautogui
import request_audio as rq
import audio_speech_to_text as sp
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def bot_pass(driver):
        #solving balloon bot test
        time.sleep(random.uniform(0.5, 1))
        #balloon=driver.find_element("xpath", "//button[contains(text(), 'לחץ כאן')]") #TEST
        balloon=driver.find_element("xpath", "//button[contains(text(), 'לחץ')]") #TEST
        loc=balloon.location #TEST
        x_loc=loc['x'] #TEST
        y_loc=loc['y'] #TEST
        pyautogui.moveTo(x_loc, y_loc, 0.4) #TEST 
        balloon.click() #TEST
        time.sleep(random.uniform(0.5, 1))
        press_again=True
        while press_again:
            try:     
              balloon=driver.find_element("xpath", "//button[contains(text(), 'לחץ')]")
              loc=balloon.location #TEST
              x_loc=loc['x'] #TEST
              y_loc=loc['y'] #TEST
              pyautogui.moveTo(x_loc, y_loc, 0.4) #TEST 
              balloon.click() #TEST
              time.sleep(random.uniform(0.5, 1))
            except:
              print('balloon test failed!')
              break


        #solving recapcha
        frame_0=WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//iframe[@title='reCAPTCHA']")))
        driver.switch_to.frame(frame_0)
        recapcha=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='recaptcha-checkbox-border']"))).click()
        driver.switch_to.default_content()
        frame=WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//iframe[@title='התוקף של אתגר reCAPTCHA יפוג בעוד שתי דקות']")))
        driver.switch_to.frame(frame)
        audio_solver=driver.find_element("xpath", "//button[@id='recaptcha-audio-button']").click()
        time.sleep(random.uniform(2, 2.5))
        download_audio=driver.find_element("xpath", "//a[@class='rc-audiochallenge-tdownload-link']").click()
        time.sleep(random.uniform(2, 2.5))
        driver.switch_to.window(driver.window_handles[1])
        rq.download_speech(driver.current_url)
        #time.sleep(random.uniform(2, 2.5))
        text=sp.speech_to_text('new.wav')
        #time.sleep(random.uniform(2, 2.5))
        print(text)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(random.uniform(2, 2.5))
        frame = driver.find_element("xpath", "//iframe[@title='התוקף של אתגר reCAPTCHA יפוג בעוד שתי דקות']")
        driver.switch_to.frame(frame)
        input_capcha=driver.find_element("xpath", "//input[@id='audio-response']")
        input_capcha.send_keys(text)
        time.sleep(random.uniform(2, 2.5))
        confirm_capcha=driver.find_element("xpath", "//button[@id='recaptcha-verify-button']").click()

        #continue after solving recapcha
        time.sleep(random.uniform(2, 2.5))
        driver.switch_to.default_content()
        continue_without_sign=driver.find_element("xpath", "//a[@data-i18n='ContinueWithoutSignIn']").click()
        time.sleep(random.uniform(2, 2.5))
        continue_anyway=driver.find_element("xpath", "//button[@data-i18n='ContinueAnyway']").click()



def queqe_appointment(driver):
        done=False
        #enter phone number
        phone_number=WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH,"//input[@data-ng-model='textAnswer']")))
        phone_number.send_keys('ENTER YOUR PHONE')
        time.sleep(random.uniform(3, 3.5))
        next=driver.find_element("xpath", "//button[@data-i18n='Continue']").click()
        

        #select dates and times
        number_of_tries_dates=2
        pos_date=0 #pos of date in the dates list
        for i in range(0,number_of_tries_dates):
            try:
                date_txt='No Date Available'
                time_txt='No Time Available'
                dates=WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"//li[@class='list-item picker-body']//ul/li")))
                dates[pos_date].click()
                date_txt=dates[pos_date].get_attribute("aria-label")
                time.sleep(random.uniform(4.5, 5))
                scrolling_div=driver.find_element("xpath", "//div[@class='mCustomScrollBox mCS-mv-minimal mCSB_vertical mCSB_inside']")
                scrolling_div.send_keys(Keys.PAGE_DOWN)
                times=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='picker-scroll-container no-scroll']//ul/li")))
                times[len(times)-1].click()
                time_txt=times[len(times)-1].text
                print('done!',date_txt+', '+time_txt)
                done=True
                break
            except:
                print('cannot make an appoinment with date: '+date_txt+", "+time_txt)
            pos_date+=1
            
            if date_txt=='No Date Available':
                break
        return done    
        #confirm queqe
        #confirm_appoinment=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='btn actionButton createApp  ng-binding']//ul/li"))).click()

URLS=["https://myvisit.com/#!/home/service/7237","https://myvisit.com/#!/home/service/8872"]
if __name__=='__main__': 
    browser_agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    options = uc.ChromeOptions()
    #options.add_argument(f'user-agent={browser_agent}')
    #options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36')
    options.add_argument("--no-sandbox")
    driver = uc.Chrome(options=options,service_creationflags=subprocess.CREATE_NO_WINDOW)
    driver.maximize_window()
    #print(driver.execute_script("return navigator.userAgent;"))
    first_url=True
    made_appt=False
    for url in URLS:    
        if made_appt:
            break
        driver.get(url)
        if first_url: #first url
            bot_pass(driver)
            first_url=False
                
        made_appt=queqe_appointment(driver)
        
            


        
