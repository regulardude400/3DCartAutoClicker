from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class AutoClicker:
    def __init__(self, url, transId, gatewayId, processorId):
        self.url = url
        self.transId = transId
        self.gatewayId = gatewayId
        self.processorId = processorId
        self.options = webdriver.ChromeOptions()
        self.prefs = {"profile.default_content_setting_values.notifications" : 2}
        self.options.add_experimental_option('prefs', self.prefs)
        self.driver = webdriver.Chrome('chromedriver', options=self.options)#locate the webdriver in your file directory
        self.username = "" 
        self.password = "" 
        
    def open3DCart(self):
        self.driver.get(self.url + "gem.asp?action=createSupportUser")
        self.driver.implicitly_wait(4)
        self.driver.find_element_by_partial_link_text("Login").click()
        className = "dropdown-toggle"
        dropdownExist = self.checkExistByClass(className)
        if(dropdownExist):
            self.new3DCartStore()
        else:
            self.old3DCartStore()
            
    def old3DCartStore(self):
        self.driver.get(self.url + "payment_options.asp?paymethod=online_payment")
        
    def new3DCartStore(self):
        self.driver.get(self.url + "payment_options.asp?paymethod=online_payment")
        
    def checkExistByClass(self, className):
        try:
            self.driver.find_element_by_class_name(className)
        except NoSuchElementException:
            return False
        return True
    
if __name__ == "__main__":
    a = AutoClicker("https://integrityinstuments-com.3dcartstores.com/admin/", 1, 2, 3)
    a.open3DCart()
    

