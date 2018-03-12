from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome('/chromedriver', options=options) #locate the webdriver in your file directory
username = "" #enter your FB email
password = "" #enter your FB password

def openTinder():
    driver.get("https://tinder.com/app/login")
    driver.implicitly_wait(10)
    driver.find_element_by_xpath("//*[@id='modal-manager']/div/div/div[2]/div[1]/div[2]/button[1]").click()
    
def fbLogin():
    driver.find_element_by_xpath("//*[@id='email']").send_keys(username)
    driver.find_element_by_xpath("//*[@id='pass']").send_keys(password)
    driver.find_element_by_xpath("//*[@id='u_0_0']").click()


def like():
    like = driver.find_element_by_xpath("//*[@id='content']/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[4]")
    while True:
        try:
            like.click()
        except NoSuchElementException:
            print("hello")
            

if __name__ == "__main__":
    openTinder()
    driver.switch_to_window(driver.window_handles[-1])
    fbLogin()
    driver.switch_to_window(driver.window_handles[0])
    like()
    

