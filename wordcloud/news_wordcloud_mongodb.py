#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymongo
import pandas as pd
import jieba
import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from collections import Counter
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_gradient_magnitude


# In[2]:


client = pymongo.MongoClient("mongodb+srv://vicar1987:1ul3u03nji3@twfruit.i2omj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.TWFruits # connect database TWFruits


# 分別讀取afa_news、coa_news、ettoday_news_craw並轉換成dataframe進行讀取
# connect collection afa_news
afa_news = db.afa_news
df_afa = pd.DataFrame(list(afa_news.find()))

# connect collection coa_news
coa_news = db.coa_news  
df_coa = pd.DataFrame(list(coa_news.find()))

# connect collection ettoday_news_craw
ettoday_news = db.ettoday_news_craw
df_ettoday = pd.DataFrame(list(ettoday_news.find()))

# 將放置新聞內容的欄位轉成list後進行合併
afa_content = df_afa['content'].tolist()
coa_content = df_coa['content'].tolist()
ettoday_content = df_ettoday['內容'].tolist()
news_content = afa_content + coa_content + ettoday_content


# In[3]:


# 進行斷詞
jieba.set_dictionary('C:/Users/Tibame_T14/Desktop/專題/文字雲/Word_Dictionary/dict.txt')
jieba.load_userdict('C:/Users/Tibame_T14/Desktop/專題/文字雲/Word_Dictionary/mydict.txt')
all_article_text = ''.join(news_content)
seg_words_list = jieba.lcut(all_article_text)

with open(file='C:/Users/Tibame_T14/Desktop/專題/文字雲/Word_Dictionary/stop_words.txt', mode='r', encoding='utf-8') as file:
    stop_words = file.read().split('\n')

seg_words_list = []
for i in news_content:
    words = jieba.cut(i,cut_all=False)
    for s in words:
        if s.strip() in stop_words:
            pass
        elif s.strip() in [' ', '']:
            pass
        else:
            seg_words_list.append(s.strip())

seg_words = ' '.join(seg_words_list)

# 字詞統計
# wordcount = {}
# for word in seg_words_list:
#     wordcount[word] = wordcount.get(word, 0)+1
# sorted(wordcount.items(), key=lambda x: x[1], reverse=True)


# In[4]:


# 文字雲繪製
bg=np.array(Image.open("./Image/taiwan.jpg"))
wordcloud = WordCloud(background_color="white",
                      font_path='C:/Windows/Fonts/msjhbd.ttc', 
                      mask=bg, 
                      collocations=False, 
                      width=1920, 
                      height=1080).generate(seg_words)
image_colors=ImageColorGenerator(bg)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig('./Image/wordcloud.jpg',dpi=600) # 圖片存檔
plt.show()


# In[ ]:




