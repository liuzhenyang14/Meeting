from codex.baseerror import *
from codex.baseview import APIView

from wechat.models import UserLogin
from wechat.models import ConfBasic
from wechat.models import InConf

import urllib
import urllib.parse
import urllib.request
from urllib.request import urlopen
import time
import json

class JoinConf(APIView):
    def get(self):

        
        url = "http://60.205.137.139/adminweb/REST/API-V2/confInfo?confid=" + self.input['confid']
        req = urllib.request.urlopen(url)
        content = req.read().decode('utf-8')
        datas = json.loads(content)
        type = datas['data']['detail']['privateType']
        result = joinconf(self.input['user_id'], self.input['confid'], type)
        InConf.objects.create(user_id=self.input['user_id'], confid=self.input['confid'])
        return result


def joinconf(userid, confid, type):
    urlvalue = urllib.parse.urlencode({"userid": userid, "confid": confid, "type": type})
    postdata = ("").encode('utf-8')
    url = "http://60.205.137.139/adminweb/REST/API-V2/joinConf?" + urlvalue
    request = urllib.request.Request(url, postdata)
    response = urllib.request.urlopen(request)
    s = response.read().decode('utf-8')
    res = json.loads(s)
    return res

class CancelConf(APIView):
    def get(self):
        result = cancelConf(self.input['user_id'], self.input['confid'])
        InConf.objects.filter(user_id=self.input['user_id'], confid=self.input['confid']).delete()
        return result
    
def cancelConf(userid, confid):
    urlvalue = urllib.parse.urlencode({"userid": userid, "confid": confid})
    postdata = ("").encode('utf-8')
    url = "http://60.205.137.139/adminweb/REST/API-V2/cancelConf?" + urlvalue
    request = urllib.request.Request(url, postdata)
    response = urllib.request.urlopen(request)
    s = response.read().decode('utf-8')
    res = json.loads(s)
    return res

class payDetail(APIView):
    def get(self):
        a = {"reason":"", "money":"100w",}
        return a

        
class MeetingDetail(APIView):

    def get(self):
        url = "http://60.205.137.139/adminweb/REST/API-V2/confInfo?confid=" + self.input['confid']
        req = urllib.request.urlopen(url)
        content = req.read().decode('utf-8')
        datas = json.loads(content)
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
        t = datas['data']['detail']['privateType']
        inconf = len(InConf.objects.filter(user_id=self.input['user_id'], confid=self.input['confid']))
        print(inconf)
        test = {
            'name': name,
            'address': address,
            'date': start_date,
            'image':'http://60.205.137.139/adminweb/'+image,
            'web':web,
            'phone':phone,
            'fax':fax,
            'email':email,
            'weixin':weixin,
            'qq':qq,
            'weibo':weibo,
            'desc':desc,
            'type':t,
            'id':self.input['confid'],
            'userid':self.input['user_id'],
            'inconf': inconf,
        }
        return(test)
