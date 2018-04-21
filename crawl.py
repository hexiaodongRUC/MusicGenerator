#encoding=utf8
import unittest
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import json
import re
import os,sys,time

headers = {
    'Host':"music.163.com",
    'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'Accept-Encoding':"gzip, deflate",
    'Content-Type':"application/x-www-form-urlencoded",
    'Cookie':"mail_psc_fingerprint=5177029d6a3b3e46ec80e979d0a5be34; _ntes_nnid=94c02b2e4dcbed17069037c777094d0a,1489670064075; _ntes_nuid=94c02b2e4dcbed17069037c777094d0a; __utma=94650624.1220094660.1491465239.1491465239.1491465239.1; usertrack=3/zPBVjqCt4cxZLBBgpLAg==; _ga=GA1.2.1913188091.1494258079; vjuids=54d330ef0.15e8879b2ce.0.ad8064ab10ceb; NTES_CMT_USER_INFO=19332780%7Chexiaodong1993%7Chttp%3A%2F%2Fmimg.126.net%2Fp%2Fbutter%2F1008031648%2Fimg%2Fface_big.gif%7Cfalse%7CaGV4aWFvZG9uZ18xOTkzQDE2My5jb20%3D; __e_=1514874781140; _iuqxldmzr_=32; __f_=1517319657766; _ngd_tid=180tkCEceFFb56lmaCVDPoQmVMLhjqQx; nts_mail_user=hexiaodong_1993@163.com:-1:1; UM_distinctid=1615f9fddf50-0c6eb0b088a1d4-4323461-144000-1615f9fddf6ba5; __gads=ID=767ed1545835df7f:T=1517727769:S=ALNI_MZ_zJUrcd4WL0Hl5vHP7ZglWMh1gQ; vjlast=1505528231.1517825965.11; vinfo_n_f_l_n3=822321c6f599c21d.1.7.1505528230620.1517727872398.1517826008372; P_INFO=hexiaodong_1993@163.com|1518612998|0|urs|00&99|bej&1517539282&mail163#bej&null#10#0#0|132204&0||hexiaodong_1993@163.com; Province=0530; City=0531; JSESSIONID-WYYY=A30Ci6BswIGMUNAlYOfhKvyxVRbvVsYW307d%2BC4puHg0IGrv3nJmV5UMcJAwP%2FQ%2BDR%2B25mMsDdhQjU%5Ccllcn9cc4VvKYAAKO7ovkbIcu5QzZmR%2BqRjKDApI12rVzRD8%2FE4%5CNpnjvasmU15scAbJYbD4J9Gjlyg6hfxrxChGXUy1vVbG%5C%3A1519546232276",
    'Connection':"keep-alive",
    'Referer':'http://music.163.com/',
    'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}

class seleniumTest():
    def setUp(self):
        print('start')

    #取对应歌曲id的歌词
    def test_get_lyric(self, id=450853439):
        lrc_url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(id) + '&lv=1&kv=1&tv=-1'
        lyric = requests.get(lrc_url)
        json_obj = lyric.text
        j = json.loads(json_obj)
        lrc = j['lrc']['lyric']
        pat = re.compile(r'\[.*\]')
        lrc = re.sub(pat, "", lrc)
        lrc = lrc.strip()
        return lrc

    #取对应歌手id的Top热歌id列表
    def test_get_singer_songs_list(self, singerId = 6731):
        singer_url = 'http://music.163.com/artist?id=' + str(singerId)
        web_data = requests.get(singer_url)
        soup = BeautifulSoup(web_data.text, 'lxml')
        singer_name = soup.select("#artist-name")
        r = soup.find('ul', {'class': 'f-hide'}).find_all('a')
        r = (list(r))
        music_id_set = []
        for each in r:
            song_name = each.text  # print(each.text)
            song_id = each.attrs["href"]
            music_id_set.append(song_id[9:])
        return music_id_set

    #取对应歌单id的歌曲id列表
    def test_get_playlist_songs_list(self, playlistId = 498708023):
        top_singer_url = 'http://music.163.com/playlist?id=' + str(playlistId)
        web_data = requests.get(top_singer_url, headers=headers)
        soup = BeautifulSoup(web_data.text, 'lxml')
        title = soup.title.text
        R = soup.find('ul', {'class': 'f-hide'}).find_all('a')
        R = (list(R))
        top_singer_ID_set = []
        for each in R:
            song_name = each.text
            song_id = each.attrs["href"]
            top_singer_ID_set.append(song_id[9:])
        return top_singer_ID_set, title
    def tearDown(self):
        print('down')


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    test = seleniumTest()
    songList, title = test.test_get_playlist_songs_list()
    if os.path.exists(title) == False:
        os.mkdir(title)
    for tempId in songList:
        tempLrc = test.test_get_lyric(tempId)
        time.sleep(1)
        with open(title + '/'+str(tempId) + '.txt', 'w') as fout:
            fout.write(tempLrc)
        print(str(tempId) + " done!")