from codex.baseerror import *
from codex.baseview import APIView

import urllib
import urllib.parse
import urllib.request
from urllib.request import urlopen
import time
import json

class MeetingDetail(APIView):

    def get(self):
        url = "http://60.205.137.139/adminweb/REST/API-V2/confInfo?confid=" + self.input['confid']
        req = urllib.request.urlopen(url)
        content = req.read().decode('utf-8')
        datas = json.loads(content)
        print(datas)
        name = datas['data']['basic']['name']
        address = datas['data']['detail']['address']
        image = datas['data']['basic']['image']
        start_date = datas['data']['basic']['start_date']
        web = datas['data']['detail']['website']
        phone = datas['data']['detail']['phone']
        fax = datas['data']['detail']['fax']
        email = datas['data']['detail']['email']
        weixin = datas['data']['detail']['weixin']
        qq = datas['data']['detail']['qq']
        weibo = datas['data']['detail']['weibo']
        desc = datas['data']['detail']['desc']
        test = {
            'name': name,
            'address': address,
            'start_date': start_date,
            'image':'http://60.205.137.139/adminweb/'+image,
            'web':web,
            'phone':phone,
            'fax':fax,
            'email':email,
            'weixin':weixin,
            'qq':qq,
            'weibo':weibo,
            'desc':desc,
        }
        return(test)