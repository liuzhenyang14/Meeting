from codex.baseerror import *
from codex.baseview import APIView
import urllib
import json
from wechat.models import UserLogin
class JoinConf(APIView)
    def post(self):
    	self.check_input('user_id', 'confid', 'type', 'code')
    	result = joinconf(self.input['user_id'], self.input['confid'], self.input['type'], self.input['code'])
    	return result


def joinconf(userid, confid, type, code):
	urlvalue = urllib.parse.urlencode({"userid": userid, "confid": confid, "type": type, "code": code})
	postdata = (""), encode('utf-8')
	url = "http://60.205.137.139/adminweb/REST/APT-V2/joinConf?" + urlvalue
	request = urllib.request.Request(url.postdata)
	response = urllib.request.urlopen(request)
	s = response.read().decode('utf-8')
	res = json.loads(s)
	return res
