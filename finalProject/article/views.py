from django.shortcuts import render
from django.http import HttpResponse
from article.ditAPI import tools


def index(request):
    return HttpResponse("서버연결 극혐")


def InputUrlCrawling(inputUrl):
    temp = tools.get_title_contents(inputUrl)
    result = {"test1": temp[0], "test2": temp[1]}
    return result


def viewtest(request) :
    # 화면 가져가는 데이터
    # 화면에서 input 받은 데이터

    temp = InputUrlCrawling("https://n.news.naver.com/article/028/0002614078?cds=news_media_pc")
    return HttpResponse(temp[0])
