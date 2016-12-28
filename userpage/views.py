from codex.baseerror import *
from codex.baseview import APIView

from wechat.models import UserLogin

import urllib
import urllib.parse
import urllib.request
from urllib.request import urlopen
import time
import json

class JoinConf(APIView):
    def get(self):
    	self.check_input('user_id', 'confid', 'type')
    	result = joinconf(self.input['user_id'], self.input['confid'], self.input['type'])
    	return result


	def joinconf(userid, confid, type, code):
		urlvalue = urllib.parse.urlencode({"userid": userid, "confid": confid, "type": type, "code": code})
		postdata = ("").encode('utf-8')
		url = "http://60.205.137.139/adminweb/REST/APT-V2/joinConf?" + urlvalue
		request = urllib.request.Request(url.postdata)
		response = urllib.request.urlopen(request)
		s = response.read().decode('utf-8')
		res = json.loads(s)
		return res

class CancelConf(APIView):
	def get(self):
		result = cancelConf(self.input['user_id'], self.input['confid'])
		return result

	def cancelConf():
		urlvalue = urllib.parse.urlencode({"userid": userid, "confid": confid})
		postdata = ("").encode('utf-8')
		url = "http://60.205.137.139/adminweb/REST/APT-V2/cancelConf?" + urlvalue
		request = urllib.request.Request(url.postdata)
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
        }
        return(test)
