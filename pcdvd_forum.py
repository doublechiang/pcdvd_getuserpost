import requests
import logging
import string
from io import BytesIO    
from urllib.parse import urlparse

from bs4 import BeautifulSoup

class PcdvdForum:

    def parseUrl(self, url):
        thread = None
        o = urlparse(url)
        q = o.query.split('&')
        for s in q:
            print(s)
            if s.startswith('t='):
                # Get the thread number string.
                thread = s[2:]

        # No matter what page index, we get first page only
        author = self.getAuthor(thread)
        return author, thread


    def getAuthor(self, thread):
        """ Get the first writer, this is the user
        """
        url = "https://www.pcdvd.com.tw/showthread.php?t={}".format(thread)
        r = requests.get(url)
        r.encoding = 'big5'
        soup = BeautifulSoup(r.text, 'html.parser')
        body = soup.html.body
        tables = body.find_all('table', attrs={'class': 'tborder'})
        for t in tables:
            user = t.find_all('a', attrs={'class': 'bigusername'})
            for u in user: 
                return u.text
        


    def getUserPostByThread(self, thread, user):
        """ use python generator to stream output, otherwise heroku will have timeout.
        """
        url = "https://www.pcdvd.com.tw/showthread.php?t={}".format(thread)
        r = requests.get(url)
        r.encoding = 'big5'
        lastpage = self.getLastPage(r.text)
        html_doc = []
        # html_doc.append('<meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=big5">')
        logging.info("Retrieveing pages from 1 to {}".format(lastpage))
        for page in range(1, lastpage):
            if page == 1:
                html_doc.extend(self.getUserPostByPage(r.text, user))

            url = "https://www.pcdvd.com.tw/showthread.php?t={}&page={}&pp=10".format(thread, page)
            r = requests.get(url)
            r.encoding = 'big5'
            # html_doc.extend(self.getUserPostByPage(r.text, user))
            yield self.getUserPostByPage(r.text, user)


    def save(self):
        r = requests.get('https://www.pcdvd.com.tw/showthread.php?t=660757&page=22&pp=10') 
        r.encoding = 'big5'
        f = open('t.html', "w")
        f.write(r.text)
        f.close()

    def getLastPage(self, html):
        """ Get Last Page number by any pcdvd page
            At PCDVD,
            if there is no pagenav, only one page.
            if there is less, page, there is no '最後' nav anchor
            then minus 1 is '下一頁' and the minus 2 is the last page.
        """
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.html.body
        pagenav = body.find_all('div', attrs={'class':'pagenav'})
        page =1
        for div in pagenav:
            # print(div.text)
            nav_bar = div.table.tr
            nav_item = nav_bar.find_all('a')
            if nav_item[-1].text == '下一頁':
                last_url = nav_item[-2].attrs.get('href')
            else:
                last_url = nav_item[-1].attrs.get('href')
            # last_url is our last index
            page=  self.__getFinalPageFromUrl(last_url)
        return page

    def __getFinalPageFromUrl(self, url):
        tokens  = url.split('&')
        for p in tokens:
            if 'page=' in p:
                page_no = int(p[5:])
                return page_no

    def getUserPostByPage(self, html, lookup_user):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.html.body
        tables = body.find_all('table', attrs={'class': 'tborder'})
        html_doc =[] 
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
                html_doc.append(str(t))
        # Contents in list
        # buf = BytesIO()
        # for p in html_doc:
        #     buf.write(p.encode('utf-8'))
        # print(buf.getvalue())
        # buf.seek(0)
        # print(html_doc)
        buf = "".join(html_doc)

        return buf



if __name__ == '__main__':
    # f = open('t.html')
    # html = f.read()
    # f.close
    # Article().save()
    # Article().getArticleByUser('660757', 'ifeven', 1)
    # Article().getArticleByUser('485703', 'macrosstt', 261)
    # Article().parse()
    p = PcdvdForum()
    # func = p.getUserPostByThread('991318', '慕凡')
    # for html in func:
    #     print(html)
    p.parseUrl('https://www.pcdvd.com.tw/showthread.php?t=1186121')
