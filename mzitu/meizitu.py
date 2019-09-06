import requests, os, random
from lxml import etree


meizi_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
]


save_path = 'E:\BeautifulPictures'

# 创建文件夹
def createFile(file_path):
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)


def get_html(url):
    response = requests.get(url, headers={'User-Agent': random.choice(meizi_headers)}).content.decode()
    html = etree.HTML(response)
    return html

def get_year(all_html):
    year_list = all_html.xpath('//div[@class="year"]/text()')
    print('year_list', len(year_list))
    year_all_list = all_html.xpath('//ul[@class="archives"]')
    print('year_all_list', len(year_all_list))
    year_dict = {year: year_all for year, year_all in zip(year_list, year_all_list)}
    return year_dict

def get_month(year_html):
    month_list = year_html.xpath('./li/p/em/text()')
    print('month_list', len(month_list))
    month_all_list = year_html.xpath('./li')
    print('month_all_list', len(month_all_list))
    month_dict = {month: month_all for month, month_all in zip(month_list, month_all_list)}
    return month_dict

def get_link(month_html):
    title = month_html.xpath('./p[2]/a[@target="_blank"]/text()')
    print('title', len(title))
    link = month_html.xpath('./p[2]/a[@target="_blank"]/@href')
    print('link', len(link))
    link_dict = {title: link for title, link in zip(title, link)}
    print(link_dict)
    return link_dict

def get_img(link_html):
    img_name = link_html.xpath('//h2/text()')[0]
    img_url = link_html.xpath('//div[@class="main-image"]//img/@src')[0]
    try:
        next_url = link_html.xpath('//div[@class="pagenavi"]/a/span[contains(text(), "下一页»")]/../@href')[0]
    except IndexError:
        next_url = None
    return img_name, img_url, next_url

def run():
    url = 'https://www.mzitu.com/all/'
    file = save_path
    createFile(file)
    html = get_html(url)
    year_dict = get_year(html)
    print(year_dict)
    for year, year_all in year_dict.items():
        year_file = file + '\\' + year
        createFile(year_file)
        month_dict = get_month(year_all)
        print(month_dict)
        for month, month_all in month_dict.items():
            month_file = year_file + '\\' + month
            createFile(month_file)
            link_dict = get_link(month_all)
            for title, link in link_dict.items():
                print(title,link)
                link_file = month_file + '\\' + title
                createFile(link_file)
                next_url = link
                while next_url:
                    link_html = get_html(next_url)
                    img_name, img_url, next_url = get_img(link_html)
                    # 防盗链加入Referer
                    headers = {'User-Agent': random.choice(meizi_headers), 'Referer': img_url}
                    img_res = requests.get(img_url, headers=headers)
                    img_name = img_name + '.' + img_url.split('.')[-1]
                    with open(link_file + '\\' + img_name, 'wb') as f:
                        f.write(img_res.content)


if __name__ == '__main__':
    run()