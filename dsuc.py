"""
checkdmarc是一个python语言开发的工具模块，用于收集目标域名的SPF记录和DMARC DNS记录，并同时验证两种记录的合理性。
   #此处记得空行
---
name: checkdmarc-SPF/DMARC 配置检测	#工具名称，可添加中文描述
category:	#工具分类
  - recon
"""

__modes__ = ["raw"]
import requests
import bs4
import argparse

external = []
unknown = []
fuzzables = []

def extractor(soup, host):
    all_links = list()
    for link in soup.find_all('a', href=True):
        #print(link['href'])
        if link['href'].startswith('/'):
       #     print("yes 0")
            if link['href'] not in all_links:
                all_links.append(host + link['href'])
        elif host in link['href']:
     #       print("yes 1")
            if link['href'] not in all_links:
                all_links.append(link['href'])
        elif 'http://' in link['href']:
        #    print("yes 2")
            if 'https://' + host.split('http://')[1] in link['href'] and link['href'] not in all_links:
                all_links.append(link['href'])
        elif 'http' not in link['href'] and 'www' not in link['href'] and len(link['href']) > 2 \
                and '#' not in link['href']:
            #print("yes 3")
            if link['href'] not in all_links:
                #print("yes 4")
                all_links.append(host + '/' + link['href'])
        elif len(link['href']) > 6:
      #      print("yes 4")
            external.append(link['href'])
        else:
     #       print("yes 5")
            unknown.append(link['href'])
    #print("all_links is")
    #print(all_links)
    return all_links


def fuzzable_extract(linklist):
    fuzzables = []
    for link in linklist:
        if "=" in link:
            fuzzables.append(link)
    return fuzzables


def xploit(link, host=None):
    if host is None:
        host = link
    res = requests.get(link, allow_redirects=True)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    return extractor(soup, host)


def level2(linklist, host):
    final_list = list()
    for link in linklist:
        for x in xploit(link, host):
            if x not in final_list:
                final_list.append(x)
                print("Appended", x)
        if link not in final_list:
            final_list.append(link)
    return final_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='root url', dest='url')
    #parser.add_argument('-d', '--deepcrawl', help='crawl deaply', dest='deepcrawl', action='store_true')
    #parser.add_argument('-f', '--fuzzable', help='extract fuzzable', dest='fuzzable', action='store_true')
    parser.add_argument('-e', '--external', help='extract external', dest='external', action='store_true')
    args = parser.parse_args()
    if args.url is None:
        quit()
    if 'http' not in args.url:
        args.url = 'http://' + args.url
    # if args.deepcrawl:
    #     links = level2(xploit(args.url), args.url)
    #     if len(links) >= 1:
    #         print('\nLINKS WITH DEEPCRAWL : \n')
    #         for link in links:
    #             print(link)
    #     else:
    #         print('\nNo Link Found\n')

    links = xploit(args.url)
    if len(links) >= 1:
        #print('\nLINKS :')
        for i in links:
            print(i)
    else:
        print('\nNo Link Found\n')


    # if args.fuzzable:
    #     if len(links) >= 1:
    #         if len(fuzzable_extract(links)) > 1:
    #             print('\nFUZZABLE LINKS :')
    #             for link in fuzzable_extract(links):
    #                 print(link)
    #         else:
    #             print('\nNo Fuzzable Link Found\n')

    if args.external:
        if len(external) >= 1:
            print('\nEXTERNAL LINKS :')
            for link in external:
                print(link)
        else:
            print('\nNo EXTERNAL Link Found\n')


if __name__ == "__main__":
    main()
