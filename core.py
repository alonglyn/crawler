from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests

class Crawler
    def __init__(self, dr):
        self.dr = dr
    def next_page(self, by, params):
        """
        点击下一页
        """
        next_btn = self.wait_for(by,params)
        if next_btn:
            next_btn.click()
            time.sleep(0.5)
            return True
        else:
            return False
    def wait_for(self,by,param,multy=False,duration=5):
        try:
            if multy:
                ret = WebDriverWait(driver, duration).until(
                    EC.presence_of_all_elements_located((by, param)),
                    message="{}超时".format(str((by, param)))
                )
            else:
                ret = WebDriverWait(driver, duration).until(
                    EC.presence_of_element_located((by, param)),
                    message="{}超时".format(str((by, param)))
                )
            return ret
        except Exception as e:
            print('等待失败',e)
        return None
    
    def run(self, *args, **kw):
        """
        docstring
        """
        raise NotImplementedError

