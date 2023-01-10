# 获取虎牙直播的真实流媒体地址。

import requests
import re
import base64
import urllib.parse
import hashlib
import time
import random
import sys

def live(e):
    try:
        i, b = e.split('?') #问号分割
        r = i.split('/') #斜杠分割
        s = re.sub(r'.(flv|m3u8)', '', r[-1]) #替换掉flv m3u8 得78941969-2601386338-11172869245971202048-3120471182-10057-A-0-1-imgplus
        c = b.split('&')
        c = [i for i in c if i != ''] # &符号分割
        #print (c)
        n = {i.split('=')[0]: i.split('=')[1] for i in c} # =符号分割
        fm = urllib.parse.unquote(n['fm']) if ('fm' in n.keys()) else ''# fm的值进行url解码
        u = base64.b64decode(fm).decode('utf-8') if ('fm' in n.keys()) else ''#将二进制字符串解码成范式
        p = u.split('_')[0] # _符号分割 取第一个
        f = str(int(time.time() * 1e7)) #18位时间戳
        l = n['wsTime'] #wsTime的值
        
        mt = n['txyp'] if ('txyp' in n.keys()) else 'a' #txyp的值 不存在 则为a
        t = str(random.randint(1460000000000, 1660000000000)) #1460000000000-1660000000000 取随机

        mm = t+f #合并时间戳
        ml = n['ctype']
        fs = n['fs']
        sp = n['sphdcdn'] if ('sphdcdn' in n.keys()) else 'al_7-tx_3-js_3-ws_7-bd_2-hw_2'
        spp = n['sphdDC'] if ('sphdDC' in n.keys()) else 'huya'
        spd = n['sphd'] if ('sphd' in n.keys()) else '264_*-265_' #以上为取值 不存在则自定义
        ll = mm+'|'+ml+'|103' #字符串合并
        ms = hashlib.md5(ll.encode("utf-8")).hexdigest() #ll值utf-8编码md5加密后16进制字符
        h = '_'.join([p, t, s, ms, l])#使用_符号拼接字符串
        m = hashlib.md5(h.encode('utf-8')).hexdigest() #h值utf-8编码md5加密后16进制字符
        urls = "{}?wsSecret={}&wsTime={}&seqid={}&ctype={}&ver=1&txyp={}&fs={}&&sphdcdn={}&sphdDC={}&sphd={}&t=103&ratio=0&u={}&t=103&sv=2110211124".format(i, m, l, mm, ml, mt, fs, sp, spp, spd, t)
# 把 i, m, l, mm, ml, mt, fs, sp, spp, spd, t 的值粘贴到{}里面
        aa, ab = urls.split('//')
        url = 'https://'+ab # http换成https
       
        return url
    except Exception as e: 
        return ''


def get_real_url(room_id):
    room_url = 'https://mp.huya.com/cache.php?m=Live&do=profileRoom&roomid=' + str(room_id)
    
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/75.0.3770.100 Mobile Safari/537.36 '
    }
    data = requests.get(url=room_url, headers=header).json()
    
    multiLine=data['data']['stream']['flv']['multiLine']
    #print(multiLine)
    urls={}
    liveData=data['data']['liveData']
    
    urls['name']=liveData['nick']+'-'+liveData['introduction'].replace('"','')
    for i in   range(len(multiLine)):
            obj=multiLine[i]
            if obj['url'] is not None:
                #print (obj['url'])
                liveline = live(obj['url'])
                urls['url'+str(i+1)]=liveline
    return urls


if __name__ == '__main__':
    try:
        try:
            r=sys.argv[1]
        except:
            r = input('请输入虎牙直播房间号：\n')
        print(get_real_url(r))
    except Exception as e:
        print(e)    
