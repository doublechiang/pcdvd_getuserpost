import requests
from bs4 import BeautifulSoup

class Article:
    def getArticleByUser(self, article, user, total):
        for page in range(1, total):
            url = "https://www.pcdvd.com.tw/showthread.php?t={}&page={}&pp=10".format(article, page)
            r = requests.get(url)
            r.encoding = 'big5'
            self.getPostByUser(r.text, user)


    def save(self):
        r = requests.get('https://www.pcdvd.com.tw/showthread.php?t=660757&page=22&pp=10') 
        r.encoding = 'big5'
        f = open('t.html', "w")
        f.write(r.text)
        f.close()

    def getLastPage(self, html):
        """ Get Last Page number by any pcdvd page
        """
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.html.body
        pagenav = body.find_all('div', attrs={'class':'pagenav'})
        for div in pagenav:
            # print(div.text)
            nav_bar = div.table.tr
            nav_item = nav_bar.find_all('a')
            # for i in nav_item:
            #     last_url = i.attrs.get('href')
            last_url = nav_item[-1].attrs.get('href')
            # last_url is our last index
            return self.__getFinalPage(last_url)
                

    def __getFinalPage(self, url):
        tokens  = url.split('&')
        for p in tokens:
            if 'page=' in p:
                page_no = int(p[5:])
                return page_no

    def getPostByUser(self, html, lookup_user):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.html.body
        tables = body.find_all('table', attrs={'class': 'tborder'})
        para = ""
        for t in tables:
            found = False
            user = t.find_all('a', attrs={'class': 'bigusername'})
            for u in user: 
                if lookup_user == u.text:
                    found = True
                    
            post = t.find_all('td', attrs={'style': 'border-bottom: 1px solid #3A6EA5;'})
            for p in post:
                para = p.text

            if found:
                print(t)


        

            



if __name__ == '__main__':
    f = open('t.html')
    html = f.read()
    f.close
    # Article().save()
    Article().getLastPage(html)
    # Article().parse()
    # Article().getArticleByUser('660757', 'ifeven', 1)
    # Article().getArticleByUser('485703', 'macrosstt', 261)
