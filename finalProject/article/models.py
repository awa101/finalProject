from django.db import models


class Article(models.Model):

    title = models.TextField()  # 기사제목
    reporter = models.CharField(max_length=50)  # 기자
    press = models.CharField(max_length=50)  # 언론사
    link = models.URLField()  # 기사링크
    publication_time = models.DateTimeField()  # 발행시간
    publication_str = models.TextField()  # 발행시간 문자열
    result = models.TextField()  # 낚시성인지 결과
    crawling_time = models.DateTimeField()  # 크롤링한 시간
    img = models.TextField() # 이미지
    gubun = models.TextField() # input, daily 구분
    '''
    # 기사내용
    # 로고 이미지
    # 썸네일 이미지    
    '''

    def __str__(self):
        return self.title
