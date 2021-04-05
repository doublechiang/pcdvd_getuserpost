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
                print('=' * 80)


        

            



if __name__ == '__main__':
    # Article().save()
    # Article().parse()
    # Article().getArticleByUser('660757', 'ifeven', 1)
    Article().getArticleByUser('485703', 'macrosstt', 2)
