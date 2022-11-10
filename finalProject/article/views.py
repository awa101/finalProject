from django.shortcuts import render
from django.http import HttpResponse
from article.ditAPI import tools # ㅇㅖ담님 짱 good
import json

from article.models import Article


def index(request):
    return HttpResponse("서버연결 극혐")

# url to Crawling
def InputUrlCrawling(inputUrl):
    temp = tools.get_title_contents(inputUrl)

    a = Article(title=temp["title"], reporter=temp["reporter"], press=temp["press"], link=inputUrl, publication_time=temp["time"], publication_str=temp["time"], result=temp["result"], crawling_time=temp["crawling_time"], img=temp["img"])
    # title, contents, press, img, time, reporter
    return temp


def viewtest(request) :
    # 화면 가져가는 데이터
    # 화면에서 input 받은 데이터

    temp = InputUrlCrawling("https://n.news.naver.com/article/028/0002614078?cds=news_media_pc")
    json_val = json.dumps(temp, ensure_ascii=False)
    return HttpResponse(json_val)


