#import sys
#from bs4 import BeautifulSoup
#import requests
#import json
print("hi")
exit()
print(sys.argv[1])
print(sys.argv[2])
exit()
ItemName=sys.argv[1]
maxitems=int(sys.argv[2])
url = "https://www.amazon.in"
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0"}
http_proxy  = "http://10.10.1.10:3128"
https_proxy = "https://10.10.1.11:1080"
ftp_proxy   = "ftp://10.10.1.10:3128"
proxyDict = { 
            "http"  : http_proxy, 
            "https" : https_proxy, 
            "ftp"   : ftp_proxy
            }

def getsoup(item, pagenum):
    url = "https://www.amazon.in/s?k="+item+"&page="+pagenum
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, "lxml")
    return soup

name = []
rating = []
price = []
image = []
review_num = []
product_link = []
stop = False
item_name = ItemName
web_page = getsoup(item_name, "1")
try:
    num_pages = int(web_page.find_all('ul', class_="a-pagination")[0].find_all('li', class_="a-disabled")[-1].text)
except:
    print("Nothing Found")
    sys.stdout.flush()
    exit()
page_num=1
#print(num_pages, "pages to be scraped")
for i in range(2,num_pages+1):
    if stop==True:
        break
    #print("Scraping page", page_num, "of", num_pages)
    web_page = getsoup(item_name, str(i))
    items = web_page.find_all('div', class_='s-result-item')
    #print(len(items), " items found\n")
    for item in items:
        if len(price)>maxitems:
            stop = True
            break
        try:
            info = (item.find('span', class_="a-text-normal").text,
                    item.find('span', class_="a-icon-alt").text,
                    "Rs. "+item.find_all("span", class_="a-price")[0].span.text[1:],
                    item.find('img', class_='s-image')['src'],
                    item.find("div", class_="a-size-small").find("span", class_="a-size-base").text,
                    url+items[10].find_all('a', class_='a-link-normal s-no-outline')[0]["href"])

            name.append(info[0])
            rating.append(info[1])
            price.append(info[2])
            image.append(info[3])
            review_num.append(info[4])
            product_link.append(info[5])
        except:
            pass
        #print("Exception found")
    page_num+=1

data = {'name':name, 'price':price, 'ratings':rating, 'image':image, 'review_num':review_num, 'product_link':product_link}
dataItems = json.dumps(data)
'''df = pd.DataFrame(data=data)
df.to_json(f"{item_name}_amazon.json", orient="split", compression="infer")'''
print(dataItems)
sys.stdout.flush()