from django.shortcuts import render
from django.http import HttpResponse
from article.ditAPI import tools


def index(request):
    return HttpResponse("서버연결 극혐")


def InputUrlCrawling(request):
    temp = tools.get_title_contents(
        "https://n.news.naver.com/article/028/0002614078?cds=news_media_pc"
    )
    result = {"test1": temp[0], "test2": temp[1]}
    return HttpResponse(temp[0])
