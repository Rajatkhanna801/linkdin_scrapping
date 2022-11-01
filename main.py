
# from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from chrome_driver import ChromeDriver
from selenium.webdriver.common.by import By


data = {
    "name": [],
    "date": [],
    "post": [],
    "likes": [],
    "count_posts":[]
}


class LinkedinSeleniumScraper:
    chromedriver = ChromeDriver()
    driver = chromedriver.drivers()
    def __init__(self):
        self.linkedin_creds = {
                'username': 'rajatkhanna801@gmail.com',
                'password': 'nokia5233'
        }
        self.login_url = "https://linkedin.com/uas/login"
        self.post_url = ["https://www.linkedin.com/company/blenheim-chalcot/posts/?feedView=all",]

    
    def perform_login(self):
        self.driver.get(self.login_url)
        self.driver.maximize_window()
        username = self.driver.find_element("id", "username")
        username_cred = self.linkedin_creds.get('username')
        username.send_keys(username_cred)
        pword = self.driver.find_element("id", "password")
        password_cred = self.linkedin_creds.get('password')
        pword.send_keys(password_cred) 
        sleep(2)
        self.driver.find_element("xpath","//button[@type='submit']").click()
        log_in_button = self.driver.find_element(By.CLASS_NAME,'from__button--floating')
        log_in_button.click()


    def scrap_post_details(self):
        self.perform_login()
        print("login done------------------------")
        self.driver.get(self.post_url)
        for i in range(max(0,50)): 
            ## here you will need to tune to see exactly how many scrolls you need
            self.driver.execute_script('window.scrollBy(0, 500)')
            sleep(1)
        
        src=self.driver.page_source
        soup=BeautifulSoup(src, 'html.parser')
        posts = self.driver.find_elements_by_xpath('//div[@class="ember-view  occludable-update "]')
        count_posts = len(posts) -1
        for names, dates, desc in zip(soup.find_all('div',{'class':'feed-shared-actor'}),
                                            soup.find_all('div',{"class":"feed-shared-actor--with-control-menu"}),
                                            soup.find_all('div',{'class':"feed-shared-update-v2__commentary"})):


            name = names.find('span',{'class':'feed-shared-actor__title'}).get_text().strip()
            date = dates.find('span',{'class':'visually-hidden'}).get_text().strip()
            if name and date:
                data["name"].append(name)                
                data["date"].append(date)              

            try:
                post = desc.find('span',{'dir':"ltr"}).get_text().strip()
                if post:               
                    data["post"].append(post)
            except Exception as e:
                    data["post"].append('')
            try:
                likes = "0"
                data["likes"].append(likes)                            
            except Exception as e:
                    print(str(e))
                    print('likes: ' +'0')        
                    data["likes"].append('')     

            data["count_posts"].append(count_posts)
            return data


    def create_csv(self):
        data = self.scrap_post_details()
        df = pd.DataFrame(data)
        df.to_csv("linked.csv", index=False)
        self.driver.close()


obj = LinkedinSeleniumScraper()
obj.create_csv()