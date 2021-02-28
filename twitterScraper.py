"""
Autor : İsmail Can Tosun

"""

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time


class TwitterScraper:
    def __init__(self,search_term):
        self.__base_url = "https://twitter.com/search?q="
        self.__search_term = search_term 
        driver_path = "C:\chromedriver.exe"
        self.__browser = webdriver.Chrome(driver_path)
        
        #Opens the url
    def get_source(self):
        self.__browser.get(self.__base_url+self.__search_term)
        time.sleep(4)
        
    def get_tweets(self):
        self.get_source()
        data = list()
        scrollCount = 0 #Sets how many times the page will scroll.
        while scrollCount  < 2:
            
            #Takes the source of the page and finds the tweets.
            soup = BeautifulSoup(self.__browser.page_source, "html.parser")
            tweets = soup.find_all("div",attrs={"data-testid":"tweet"})
        
            for tw in tweets:
              
                try:
                    
                    tweet = tw.find("div",{"class":"css-901oao r-1fmj7o5 r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0"}).text
                    nickname = tw.find("div",attrs = {"class":"css-1dbjc4n r-18u37iz r-1wbh5a2 r-13hce6t"}).text
                    date = tw.find("time").text  
                    try :
                        comments =int(tw.find("div", attrs={"data-testid":"reply"}).text)
                    except:
                        comments = 0
                    
                    try :
                        likes = int(tw.find("div", attrs={"data-testid":"like"}).text)
    
                    except:
                        likes = 0
                        
                    try :
                        retweets= int(tw.find("div", attrs={"data-testid":"retweet"}).text)
                    except:
                        retweets = 0
                    data.append((nickname,date,tweet,likes,retweets,comments))
                    
                except:
                    continue
                    
                
            #Scroll operations
            lastHeight = self.__browser.execute_script("return document.body.scrollHeight")
            
            scroll=0
            while scroll<1:
                self.__browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                newHeight = self.__browser.execute_script("return document.body.scrollHeight")
        
                if newHeight == lastHeight:
                    break
                else:
                    lastHeight = newHeight
        
                scroll+=1
           
                
            scrollCount +=1
        self.close_browser()
        return data
            
    #Data list is written in Excel
    def write_excel(self,data,filename="tweets.xlsx"):
        df = pd.DataFrame(data)
        df.columns = ["Author","Date","Tweet","Likes","Retweets","Discussions"]
        df.to_excel(filename)
        
    #Browser is closing
    def close_browser(self):
        self.__browser.close()

if __name__ == "__main__":
    scraper = TwitterScraper("request for startup") #The search term is giving
    data = scraper.get_tweets()
    scraper.write_excel(data)
    