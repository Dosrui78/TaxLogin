import base64
import json
from utils import *

bg = 'https://etax.anhui.chinatax.gov.cn/captchaFile/355x200/93595c7a-cbdc-11ec-8155-fa6f151b9200.jpg'
ft = 'https://etax.anhui.chinatax.gov.cn/captchaFile/355x200/935751b4-cbdc-11ec-8155-fa6f151b9200.png'
C = Common()
bg_content = requests.get(bg).content
ft_content = requests.get(ft).content


# res = requests.post('https://mock.kdzwy.com/captchaplatform/api/', data=json.dumps({'captcha_type': 4002, 'imgsr': bg_content, 'imgtm': ft_content}))
# print(res.text)
#
#
# def decode_captcha(captcha_type, img_sr, img_tm):
#     url = 'https://mock.kdzwy.com/captchaplatform/api/'
#     payload = {
#         'name': 'decodeCaptcha',
#         'captcha_type': captcha_type,
#         'imgsr': img_sr,
#         'imgtm': img_tm
#     }
#
#     r = requests.request("POST", url, data=json.dumps(payload))
#     print(r.text)
#
#
# decode_captcha(4002, bg_content, ft_content)

def decode_(img, imgtm='', captcha_type=1001, captcha_desc=''):
    if captcha_type == 4002:
        data = {
            'captcha_type': captcha_type,
            'imgsr': base64.b64encode(img).decode(),
            'imgtm': base64.b64encode(imgtm).decode(),
        }
    else:
        data = {
            'image': base64.b64encode(img).decode(),
            'captcha_type': captcha_type,
            'captcha_desc': captcha_desc,
        }
    res = requests.post('https://mock.kdzwy.com/captchaplatform/decodeCaptcha/', data=data)
    # print(res.text)
    return res.text

# decode(bg_content, ft_content, captcha_type=4002, captcha_desc='')
