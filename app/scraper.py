from bs4 import BeautifulSoup   
import requests


def request_url(website):
    url = website
    response = requests.get(url)  
    if response.status_code == 200:
        soup = BeautifulSoup(response.text,"html.parser")
        return soup
    else:
        return "not responding"

class Scrape():
    def __init__(self,website):
        self.website=website
    
    def get_data(self):
        #ASYNC FONKSİYON KULLAN
        if self.website=="webtekno":
            if request_url("https://www.webtekno.com") != "not responding":
                content = request_url("https://www.webtekno.com").find_all('div',{'class':'content-timeline__item'})
                topics = {"group_title":"webtekno"}
                for i in content:
                    title = i.find('span',{'class':'content-timeline--underline'})
                    link = i.find('a',{'class':'content-timeline__link clearfix'}).get('href')
                    if title !=None: #title none ise araya video koymuşlar demektir. 
                        topics[link] = title.text
                return topics
    

        elif self.website=="shiftdelete":
            if request_url("https://shiftdelete.net/") != "not responding":
                content = request_url("https://shiftdelete.net/").find_all('div',{'class':'swiper-slide swiper-slide2'})
                topics = {"group_title":"shiftdelete"}
                for i in content:
                    title = i.find('div',{'class':'col-md-12'}).text
                    link = i.find('a').get('href')
                    topics[link] = title.split('\n')[1]
                return topics


        elif self.website=="donanimhaber":
            if request_url("https://www.donanimhaber.com/") != "not responding":
                content = request_url("https://www.donanimhaber.com/").find_all('div',{'class':'medya'})
                count = 0
                topics = {"group_title":"donanımhaber"}
                for i in content:
                    if count == 10:
                        break
                    title = i.find('a')["data-title"]
                    link = "https://www.donanimhaber.com" + i.find('a').get('href')
                    topics[link]=title
                    count +=1
                return topics
            

        elif self.website=="technopat":
            if request_url("https://www.technopat.net/") != "not responding":
                content = request_url("https://www.technopat.net/").find_all('h3',{'class':'jeg_post_title'})
                count = 0
                topics = {"group_title":"technopat"}
                for i in content:
                    if count==10:
                        break
                    title = i.find('a').text
                    link = i.find('a').get('href')
                    topics[link]=title
                    count += 1
                return topics

        elif self.website=="chiptr":
            if request_url("https://www.chip.com.tr/") != "not responding":
                content = request_url("https://www.chip.com.tr/").find_all('div',{'class':['akisPost sm','akisPost','akisPost sm right']})
                count = 0
                topics = {"group_title":"chiptr"}
                for i in content:
                    if count == 10:
                        break
                    text = i.find('div',{'class':'akisText'})
                    link = "https://www.chip.com.tr/" + text.find('a').get('href')
                    title = text.find('h3').text
                    topics[link]=title
                    count +=1
                return topics

    
