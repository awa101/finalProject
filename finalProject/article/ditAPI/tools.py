from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs
from . import publisher as pb
from . import temp as temp
import requests


# 날짜 범위 계산
def date_range(start, end):
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    dates = [
        (start + timedelta(days=i)).strftime("%Y%m%d")
        for i in range((end - start).days + 1)
    ]
    return dates


# 페이지 수 계산
def soup_page(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    }
    req = requests.get(url, headers=headers)
    html = req.text
    soup = bs(html, "html.parser")
    return soup


# 제목, 본문 가져오기
def find_site(url):
    for i in range(len(pb.news)):
        if pb.news[i]["name"] in url:
            title = pb.news[i]["title"]
            contents = pb.news[i]["contents"]
            return [title, contents]


def get_title_contents(news_site):
    try:
        class_name = find_site(news_site)
        soup = soup_page(news_site)
        title_text = soup.select_one(class_name[0]).text
        contents_text = str(soup.select_one(class_name[1]))
        contents_text = [
            i
            for i in contents_text.split("<br/>")
            if len(i) > 1
            and "class=" not in i
            and "id=" not in i
            and "span" not in i
            and "strong" not in i
        ]
        temp = {'title': title_text,
                'contents': contents_text,
                'press': '언론사명',
                'img': 'https://img2.daumcdn.net/thumb/R658x0.q70/?fname=https://t1.daumcdn.net/news/202211/10/moneytoday/20221110094129395caim.jpg',
                'time': '입력 2022. 11. 10. 09:38',
                'reporter': '기자'}
    except AttributeError as err:
        return None
    else:
        return temp


# 매일 크롤링
def daily_news_grab():
    return


def check_page(url):
    try:
        soup = soup_page(url)
        news_lists = soup.find(class_="type06_headline").find_all("a") + soup.find(
            class_="type06"
        ).find_all("a")

    except AttributeError as err:
        return None
    else:
        page_length = len(soup.select(".paging > a"))
        for count in range(page_length):
            new_soup = soup_page(url + f"&page={count+1}")
            new_news_lists = new_soup.find(class_="type06_headline").find_all(
                "a"
            ) + soup.find(class_="type06").find_all("a")
            for i in grab_link(new_news_lists):
                temp.link.append(i)
        return

    # 페이지 수 확인


def grab_link(link):
    news_lists_links = list(set([link[i].get("href") for i in range(len(link))]))
    # 기사 리스트 유무
    return news_lists_links
