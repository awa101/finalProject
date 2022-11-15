from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from article.ditAPI import tools, modelPredictScore, pred # ㅇㅖ담님 짱 good
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
    result = str(modelPredictScore.articleScore(article)) # 예측 
    article = Article(title=temp["title"], reporter=temp["reporter"], press=temp["press"], link=inputUrl, publication_time=temp["time"], crawling_time=today, img=temp["img"], result=result, gubun='input')
    # title, contents, press, img, time, reporter
    # a.save() # 데이터 저장 실질적인 데이터 테스트 완료 후 주석 풀기
    return article

# 예측 
def modelPredict(article) :
    '''
    점수? binary ?  일관성이 있을 확률  ex)0.72
    '''
    return modelPredictScore.articleScore(article)

# datily Crawling 
def datilyCrawling():

    '''
    1. tools의 데일리크롤링한 함수 호출 (return값 딕셔너리 열개 담긴 리스트 하나로 옴)
    2. 리스트 loop moon
    3. 저 안에서 하나씩 예측하기 예측함수 호출
    4. DB에 담기
    5. 로그 쌓기 시작할 때 한 번 하고 하나씩 담길 때 하고 끝날 때 한번

    '''
    print('daily crawling start')
    today = timezone.now()
    tests = tools.daily_news_grab()

    for test in tests:
        print(test)
        model_result = pred.modelPredictFunc(test['title'], test['contents'])
        print(model_result)
        article = Article(title=test["title"], reporter=test["reporter"], press=test["press"], link=test["link"], publication_time=test["time"], crawling_time=today, img=test["img"], result=model_result, gubun='daily')
        print(article)
        article.save()



    print('datilyCrawling 함수 실행 : ', timezone.now())

def viewtest(request) :
    # 화면 가져가는 데이터
    # 화면에서 input 받은 데이터

    # temp = InputUrlCrawling("https://n.news.naver.com/article/028/0002614078?cds=news_media_pc")
    #json_val = json.dumps(temp, ensure_ascii=False)
    #json_val = serializers.serialize('json', temp)
   
    # result = pred.modelPredictFunc(temp.title, content)
    # print('modelPredictFunc result : ', result)
    # return HttpResponse(temp.title+temp.result)
    datilyCrawling()
    return HttpResponse('넴')

# ------- 아래부터 함수 추가하시면 됩니다. 
from django.template import loader
def main (request):
    news_info=tools.daily_news_grab()
    template = loader.get_template('/Users/coletda/mnt/c/venvs/wslFinal/finalProject/templates/mainpage.html')
    context={
        'news_info' : news_info,
    }
    return HttpResponse(template.render(context,request))
    