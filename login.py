import codecs
from time import sleep

import requests
import re
from utils import *
from zwy import *

PATH = "https://etax.anhui.chinatax.gov.cn"


class Login(Common):
    def getValidateType(self):
        """
        获取验证码类型
        """
        url = PATH + "/cas/login?service=https://etax.anhui.chinatax.gov.cn/shiro-cas"
        html = self.get_(url)
        captchaType = re.findall(r'var captchaType = "(.*?)";', html)[0]
        return captchaType

    def _getCaptchaImage(self):
        # browser = OpenBrowser().driver
        # element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//img[@class='captcha_slider_image_background']")))
        url = PATH + "/cas/captcha/conf"
        data = {
            "type": "2",
            "width": "355",
            "height": "200",
            "referer": "https://etax.anhui.chinatax.gov.cn/cas/login?service=https://etax.anhui.chinatax.gov.cn/shiro-cas"
        }
        res = self.post_(url, data=data)
        uuid = res['data']['uuid']
        url = PATH + "/cas/captcha/sources"
        data.update({'uuid': uuid})
        res = self.post_(url, data=data)
        data = res.get('data')
        bg = data.get('bg')
        ft = data.get('ft')
        token = data.get('token')
        data.update({'uuid': uuid})
        return data

    def captcha_slider(self):
        with codecs.open("./login.js", encoding="utf-8", errors='ignore') as f:
            calueLib = f.read()
        calueLib = calueLib.replace(
            "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALMiBO+tekLSFbQe7mf2U8bWhxvRgu059Pcw/I7Jckv9OSSiQU+m7uP+Iu+kQtAeMkYtOlW77E32njp4Se113rMCAwEAAQ==",
        self._getCaptchaImage()['token'])
        # calueLib = calueLib.replace("39.8611111111", str(result_decode))
        return calueLib

    def _decode_captcha(imgsr, imgtm):
        print('获取滑块验证码')
        driver = OpenBrowser().driver
        # 滑块拼图-cv2技术
        decodeCount = 0
        distance = 0
        # 再次确认是否登录成功
        try:
            yidun = driver.find_element_by_id("select2-syzSelect-container")
            return yidun
        except:
            pass
        try:
            distance = decode_(imgsr, imgtm=imgtm, captcha_type=4002)
        except Exception as e:
            try:
                sleep(0.5)
                # 确认刷新按钮是否存在
                driver.find_element_by_xpath('//div[@class="captcha_slider_image_box"]/i')
            except Exception as e:
                print('滑块页面异常，e:', e)
                # if self.retry('_login', 10):
                #     return 600, '登录异常'
                # else:
                #     return self._login(getLogin=getLogin)
            print('打码接口调用失败')
        while str(distance) == '0' and decodeCount < 5:
            decodeCount += 1
            sleep(0.5)
            driver.find_element_by_xpath('//div[@class="captcha_slider_image_box"]/i').click()
            sleep(0.5)
            print('重新获取滑块图片：', decodeCount)
            imgsr, imgtm = self._getCaptchaImage()
            distance = self.decode_captcha_zwy(imgsr, imgtm=imgtm, captcha_type=4001)
            self.log('第' + str(decodeCount) + '次打码，distance:', distance)
        if isinstance(distance, tuple):
            self.log('打码失败：', distance)
            return distance
        self.log('distance:', distance)
        return distance

if __name__ == '__main__':
    L = Login()
    capType = L.getValidateType()
    # if capType == 'slider':
    temp = L.captcha_slider()
    print(temp)
    # print(capType)