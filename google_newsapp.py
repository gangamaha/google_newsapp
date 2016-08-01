import webbrowser
import time
import sys
new = 2  # open in a new tab, if possible
keyword = raw_input("What news are your currently interested!!").strip()

# Checking for user input. Exiting if there is no input as nothing to search for
if keyword is '':
    print("No topic entered by user. Please enter a valid topic name when prompted. Currently Exiting!!")
    exit(0)

version = 3
my_python_version = sys.version_info[0]  # My python version is 2.7 so my_python_version will be 2
if my_python_version < version:
    import urllib2 as py_url  # import urllib2 for Python 2.x
else:
    import urllib.request as py_url  # import urllib.request for Python 3.x


def download_links(url):
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = py_url.Request(url, headers=headers)
        response = py_url.urlopen(req)
        page = response.read()
        return page
    except Exception as e:  # If there is some problem in reaching the url
        print(str(e))
        print("Cannot reach google.com, please check your internet connection and try later!!")
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
        end_content = raw_html.find('\" target', start_content+1)
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

# if search keyword has multiple words, we need to replace the space by +
if ' ' in keyword:
    keyword = keyword.replace(' ', "+")

url = "https://www.google.com/search?hl=en&gl=us&authuser=0&biw=1366&bih=667&tbm=nws&q="+keyword+"&oq="+keyword+"&gs_l=serp.3..0l10.6720.7574.0.7869.5.3.0.2.2.0.64.160.3.3.0....0...1c.1.64.serp..0.5.164.Mi05-kl1alI"
raw_html = download_links(url)  # this has the entire web page html
# extract the web links
links = []
links = get_links(raw_html)
# open the links in new tabs of default browser, in my case Google chrome
limit_news = 10
print("Processing your news request. Please wait, each news will be opened as new tab in your default browser")
for link in links:
        if limit_news != 0:
            webbrowser.open(link, new=new)
            time.sleep(2)  # sleep so that the news link requests are not fired at one to the browser
            limit_news -= 1
