from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Okt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import urllib, base64
# from fontTools.ttLib import TTFont
import os
from pathlib import Path


def Wordcloud(context):
    BASE_DIR = Path(__file__).resolve().parent
    dirTmp = os.path.join(BASE_DIR, "BMDOHYEON_ttf.ttf")
    # font = TTFont(BASE_DIR, "BMDOHYEON_ttf.ttf")

    okt = Okt()
    nouns = okt.nouns(context) # 명사만 추출
    words = [n for n in nouns if len(n) > 1] # 단어의 길이가 1개인 것은 제외

    c = Counter(words) # 위에서 얻은 words를 처리하여 단어별 빈도수 형태의 딕셔너리 데이터를 구함
    wc = WordCloud(colormap='Set2', scale=2.0, max_font_size=250, font_path=dirTmp)
    gen = wc.generate_from_frequencies(c)
    plt.figure()
    plt.imshow(gen)
    plt.axis('off')
    plt.show()

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    args = {'image':uri}

    return args

# wc = WordCloud(width=400, height=400, scale=2.0, max_font_size=250, font_path="C:/venvs/final/wslFinal/finalProject/article/ditAPI/BMDOHYEON_ttf.ttf")
# gen = wc.generate_from_frequencies(c)
# plt.figure()
# plt.imshow(gen)