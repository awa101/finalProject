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
    article = Article(title=temp["title"], reporter=temp["reporter"], press=temp["press"], link=inputUrl, publication_time=today, publication_str=temp["time"], crawling_time=today, img=temp["img"], result='test')
    article.result = str(modelPredictScore.articleScore(article)) # 예측 
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
    print('datilyCrawling 함수 실행 : ', timezone.now())

def viewtest(request) :
    # 화면 가져가는 데이터
    # 화면에서 input 받은 데이터

    temp = InputUrlCrawling("https://n.news.naver.com/article/028/0002614078?cds=news_media_pc")
    #json_val = json.dumps(temp, ensure_ascii=False)
    #json_val = serializers.serialize('json', temp)
    print(temp.title)
    content = '''이태원 참사를 수사하는 경찰청 특별수사본부가 최성범 서울 용산소방서장에 대한 압수수색 영장에 ‘국민 안전 확보 업무상 의무 이행을 게을리했다’는 내용을 적시한 것으로 확인됐다. 소방당국과 일선 소방관들은 “가장 먼저 출동했던 최 서장의 현장 대응은 적절했다”며 경찰 수사가 행정안전부와 경찰 지휘부 등이 아닌 소방 쪽을 향하는 것에 반발하고 있다.

특수본은 최 서장의 압수수색 영장에 “국민의 생명·신체에 대한 안전을 확보하고 이에 대한 위험을 회피·제거할 업무상 주의의무 이행을 게을리 했다”며 업무상 과실치사상 혐의를 적용했다. “현장 도착 당시 소방 비상 대응 2단계 발령에 해당하는 상황임을 파악하고서도 2단계 발령을 하지 않았다” “현장 소방대에게 인명 구조·구급 등 소방에 필요한 활동을 적절하게 지시하지 못했다”는 것이다.

최 서장은 첫 119 신고 접수 13분 뒤인 밤 10시28분 참사 현장에 도착했다. 현장 지휘팀장이 밤 10시43분 대응 1단계를 발령했고, 최 서장은 현장 상황을 살핀 뒤 주변 소방서 인력과 장비를 동원하는 대응 2단계를 밤 11시13분 발령했다.

최 서장에게 적용된 혐의는 참사 당일 50분 뒤에야 현장에 나타난 이임재 전 용산경찰서장과 같다. 소방당국은 경찰 수사 방향에 불편함을 드러냈다. 이일 소방청 119대응국장은 9일 중앙재난안전대책본부 브리핑에서 “최 서장은 당시 현장 지휘뿐만 아니라 관리, 상황 파악 등에 직접적, 적극적으로 관여했다”고 밝혔다. 김주형 전국공무원노동조합 소방본부장은 이날 <문화방송> 라디오 ‘김종배의 시선집중’ 인터뷰에서 “최 서장은 (참사 당일) 근무가 아닌 휴일인데도 초저녁부터 현장에 나와 있었고, 출동 역시 먼저 했다. 그런데 (경찰이 피의자로) 입건하면 도대체 어디까지 해야 되는게 우리의 임무냐”고 했다. 전날 전국공무원노동조합 소방본부서울소방지부는 성명을 통해 “이번 참사의 진상 규명과 책임자 처벌이 제대로 되도록 지켜볼 것이다. 꼬리자르기식 희생양을 만든다면 강력히 투쟁할 것”이라고 밝힌 바 있다.

특수본은 이날 “수사를 위한 형식적 입건”이라고 했지만, 대응 1단계를 발령한 용산소방서 팀장도 업무상 과실치사상 혐의로 입건했다. 전문가들은 대응의 적절성 여부는 따져봐야 한다면서도 업무상 과실치사상 혐의 적용에는 부정적 입장이다. 이영주 서울시립대 교수(소방방재학과)는 “왜 더 강하게 대응 못했는지 형사상으로 추궁하기 시작하면 앞으로 현장에서는 경중을 떠나 무조건 높은 단계의 대응을 걸어놓고 시작하는 수밖에 없다”고 했다. 수도권 검찰청의 한 부장검사는 “현장에서 다양한 조처를 했는데 ‘의무 이행에 게을러 사람을 숨지게 했다’는 내용을 입증하기 쉽지 않을 것이다. 2단계 발령을 더 빨리 했을 때 인명 피해를 훨씬 줄일 수 있었다고 경찰이 입증해야 하는 상황”이라고 했다. 2017년 충북 제천 스포츠시설에서 화재가 났을 때 소방 당국 대응이 미흡했다며 경찰이 당시 제천소방서장에게 업무상 과실치사 혐의를 적용해 검찰에 기소 의견으로 넘겼지만, 검찰은 2018년 “인명 구조 지연으로 인한 형사상 과실 인정이 어렵다”며 무혐의 처분한 바 있다.
    '''
    result = pred.modelPredictFunc(temp.title, content)
    print('modelPredictFunc result : ', result)
    return HttpResponse(temp.title+temp.result)

# ------- 아래부터 함수 추가하시면 됩니다. 

from django.template import loader
from django.http import JsonResponse
def main (request):
    articles=Article.objects.all()
    template=loader.get_template('article/mainpage.html')
    context={
        "articles":articles,
    }
    return HttpResponse(template.render(context,request))

def result(request):
    link=request.GET.get('inputLink')
    news=InputUrlCrawling(link)
    news= {
        'title':news.title,
        'reporter':news.reporter,
        'press': news.press,
        'result': news.result,
        'img':news.img,
        'time':news.publication_str
    }
    return JsonResponse(news)