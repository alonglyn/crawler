from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import os
import time
import json
'''
无UI界面取消下面的注释
'''
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--no-sandbox')


def wait_for(dr,by,param,multy=False,duration=5):
    try:
        if multy:
            ret = WebDriverWait(dr, duration).until(
                EC.presence_of_all_elements_located((by, param)),
                message="{}超时".format(str((by, param)))
            )
        else:
            ret = WebDriverWait(dr, duration).until(
                EC.presence_of_element_located((by, param)),
                message="{}超时".format(str((by, param)))
            )
        return ret
    except Exception as e:
        print('等待失败',e)
    return None
    

def extract_comment(comment):
    try:
        comment_id = comment.get_attribute('comment_id')
        text_box = comment.find_element_by_class_name('WB_text')
        user = text_box.find_elements_by_tag_name('a')[0].text
        text = text_box.text.split('：')[-1]
        ttime = comment.find_element_by_class_name('WB_from').text
        likes = re.findall('\d+',comment.find_element_by_class_name('WB_handle').text)
        if likes:
            like = likes[-1]
        else:
            like = 0
        return [comment_id,user,text,ttime,like]
    except:
        return None

def next_page(dr):
    next_btn = wait_for(dr,By.CLASS_NAME,'next')
    if next_btn:
        next_btn.click()
        time.sleep(0.5)
        return True
    else:
        return False
    
def run(dr, url,name='default'):
    dr.get(url)
    data = []
    page = 0
    try:
        while True:
            print('page=',page)
            for i in range(3):
                try:
                    time.sleep(2)
                    list_box = wait_for(dr,By.CLASS_NAME,'list_ul')
                    comments = wait_for(list_box,By.CLASS_NAME,'list_li',multy=True)
                    if comments:
                        break
                except Exception as e:
                    print(e)
                    pass
            print('comments count',len(comments))
            for comment in comments:
                ret = extract_comment(comment)
                if ret:
                    data.append(ret)
            if not next_page(dr):
                break
            page += 1
    except Exception as e:
        print(e)
    finally:
        df = pd.DataFrame(data)
        df.to_excel('{}.xlsx'.format(name))

if __name__ == "__main__":
    urls = [
        'https://weibo.com/1784473157/DuQsX4MiV?type=comment#_rnd1604515371338',
        'https://weibo.com/2286908003/CjNyU67L1?type=comment#_rnd1604514859040',
        'https://www.weibo.com/2286908003/E0W0CFnH9?s=6cm7D0&type=comment#_rnd1605508735837',
        'https://www.weibo.com/2656274875/E0VZulozf?type=comment#_rnd1605508801123',
        'https://weibo.com/2803301701/E0W6beT8B?type=comment#_rnd1605509251601',#
        'https://weibo.com/2656274875/E0W9laMcp?type=comment#_rnd1605509351165',#
        'https://weibo.com/2656274875/E0WPN5Ns1?type=comment#_rnd1605509395853',#
        'https://www.weibo.com/2803301701/E0ZoN2kpX?type=comment#_rnd1605508674420',#
        "https://weibo.com/2656274875/B1CCKwX8E?type=comment#_rnd1606279789919",
        "https://weibo.com/2656274875/B7po0CxOP?type=comment#_rnd1606279963786",
        "https://weibo.com/2656274875/BhF7OtDe7?type=comment#_rnd1606280009740",
        "https://weibo.com/2803301701/BEfwIDVaj?refer_flag=1001030103_&type=comment#_rnd1606280059797",
        "https://weibo.com/2656274875/C4exacAxm?type=comment#_rnd1606280098119",
        "https://weibo.com/2286908003/CjNyU67L1?type=comment#_rnd1606280144578",
        "https://weibo.com/2803301701/CEsnVDOFi?type=comment#_rnd1606280248151",
        "https://weibo.com/2656274875/CFWSG1NMH?type=comment#_rnd1606280273952",
        "https://weibo.com/1974576991/Dq9AebTLZ?type=comment#_rnd1606280332236",
        "https://weibo.com/2803301701/DtQGMFkOW?type=comment#_rnd1606280368568",
        "https://weibo.com/2803301701/DufeCgrGL?type=comment#_rnd1606280494006",
        "https://weibo.com/2286908003/DuHhDki1Q?type=comment",
        "https://weibo.com/2803301701/DAGeMdztj?type=comment#_rnd1606280561928",
    ]
    dr = webdriver.Chrome()
    dr.get('https://weibo.com/login.php#_loginLayer_1604515522042')
    input('手动登录后点回车')
    dir_name = str(int(time.time()))
    os.mkdir(dir_name)  
    for i, url in enumerate(urls):
        fime_name = os.path.join(dir_name,'linzhonglong'+str(i))
        print('current:', fime_name)
        run(dr,url,fime_name)

