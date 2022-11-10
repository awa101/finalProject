from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from article.ditAPI import tools # ㅇㅖ담님 짱 good
import json
from django.utils import timezone
from article.models import Article

# ------------------------- Don't touch Code

def index(request):
    return HttpResponse("서버연결 극혐2")

# url to Crawling
def InputUrlCrawling(inputUrl):
    temp = tools.get_title_contents(inputUrl)
    today = timezone.now()

    '''
    1. publication_time, publication_str 타입 및 format 정리 후 데이터 결정
    2. result 컬럼에 예측값 결과 넣기 
    '''
    a = Article(title=temp["title"], reporter=temp["reporter"], press=temp["press"], link=inputUrl, publication_time=today, publication_str=temp["time"], crawling_time=today, img=temp["img"], result='test')
    # title, contents, press, img, time, reporter
    # a.save() # 데이터 저장 실질적인 데이터 테스트 완료 후 주석 풀기
    return a

# 예측 
def modelPredict() :
    '''
    점수? binary ?  일관성이 있을 확률  ex)0.72
    '''
    score = 0.72
    result = score * 100
    return result

# datily Crawling 
def datilyCrawling():
    print('datilyCrawling 함수 실행')

def viewtest(request) :
    # 화면 가져가는 데이터
    # 화면에서 input 받은 데이터

    temp = InputUrlCrawling("https://n.news.naver.com/article/028/0002614078?cds=news_media_pc")
    #json_val = json.dumps(temp, ensure_ascii=False)
    #json_val = serializers.serialize('json', temp)
    print(temp.publication_time, temp.crawling_time)
    return HttpResponse(temp.title)

# ------- 아래부터 함수 추가하시면 됩니다. 

