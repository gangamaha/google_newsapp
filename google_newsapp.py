import webbrowser
import time
import sys
new = 2  # open in a new tab, if possible
keyword = "presedential election USA"


def download_links(url):
    version = (3,0)
    python_version = sys.version_info[0]
    if python_version >= version:
        import urllib.request
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req)
            page = response.read()
            return page
        except:  # If there is some problem in reaching the url
            print("Cannot reach google.com, please check your internet connection and try later!!")
            exit(0)  # Gracefully exit
    else:
        import urllib2
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except:  # If there is some problem in reaching the url
            print "Cannot reach google.com, please check your internet connection and try later!!"
            exit(0)  # Gracefully exit


def get_next_link(raw_html):
    start_line = raw_html.find("_rQb")
    if start_line == -1:
        end_content = 0
        link = "no_more_links"
        return link, end_content
    else:
        start_line = raw_html.find("class=\"_rQb\"")
        start_content = raw_html.find('href=', start_line+1)
        end_content = raw_html.find('\" target',start_content+1)
        link = str(raw_html[start_content+6:end_content])
        return link, end_content


def get_links(raw_html):
    items = []
    while True:
        item, end_string = get_next_link(raw_html)
        if item == "no_more_links":
            break
        else:
            items.append(item)
            raw_html = raw_html[end_string:]
    return items

# open a public URL, in this case, the webbrowser docs
if ' ' in keyword:
    keyword = keyword.replace(' ', "+")

url = "https://www.google.com/search?hl=en&gl=us&authuser=0&biw=1366&bih=667&tbm=nws&q="+keyword+"&oq="+keyword+"&gs_l=serp.3..0l10.6720.7574.0.7869.5.3.0.2.2.0.64.160.3.3.0....0...1c.1.64.serp..0.5.164.Mi05-kl1alI"
raw_html = download_links(url)  # this has the entire web page html
# print raw_html
links = []
links = get_links(raw_html)
# print links
limit_news = 10
for link in links:
        if limit_news != 0:
            webbrowser.open(link, new=new)
            time.sleep(2)  # sleep so that the news link requests are not fired at one to the browser
            limit_news -= 1
