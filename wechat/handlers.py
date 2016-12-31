# -*- coding: utf-8 -*-
#
from wechat.wrapper import WeChatHandler
import urllib
import json
from wechat.models import UserLogin
from urllib.parse import quote

import datetime
import time

__author__ = "Epsirom"

global currpage
currpage = 1

class ErrorHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，服务器现在有点忙，暂时不能给您答复 T T')


class DefaultHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，没有找到您需要的信息:(')


class BookEmptyHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['book_empty'])

    def handle(self):
        return self.reply_text(self.get_message('book_empty'))

class BindAccountHandler(WeChatHandler):

    def check(self):
        return self.is_text('绑定') or self.is_event_click(self.view.event_keys['account_bind'])

    def handle(self):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxe267a7a0c2634bae&secret=2e8fe91d582ead5f64035b3dccea3f13'
        req = urllib.request.urlopen(url)
        content = req.read().decode('utf-8')
        token = json.loads(content)['access_token']
        openid = self.input['FromUserName']
        temp = UserLogin.objects.filter(unionId = openid)
        if temp:
            for u in temp:
                uid = u.user_id
            return self.reply_text('你已经绑定过了，会佳id为：'+str(uid))

        url1 = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=' + token + '&openid=' + openid +'&lang=zh_CN'
        req1 = urllib.request.urlopen(url1)
        content1 = req1.read().decode('utf-8')

        nickname = json.loads(content1)['nickname']
        unionid = openid
        headimgurl = json.loads(content1)['headimgurl']
        sex = json.loads(content1)['sex']
        location = json.loads(content1)['country'] + json.loads(content1)['province'] + json.loads(content1)['city']
        language = json.loads(content1)['language']

        url2 = 'http://60.205.137.139/adminweb/REST/API-V2/loginToChinaByWeixin'
        post_data = urllib.parse.urlencode({'nickname':nickname, 'unionid':unionid, 'headimgurl':headimgurl, 'sex':sex, 'location':location, 'language':language}).encode('utf-8')
        req2 = urllib.request.urlopen(url2, post_data)
        content2 = req2.read().decode('utf-8')

        user = UserLogin.objects.create(user_id = json.loads(content2)['data']['id'], email = json.loads(content2)['data']['email'], unionId = openid)
        user.save()

        if json.loads(content2)['code'] == 0:
            return self.reply_text('绑定成功，会佳id为'+str(json.loads(content2)['data']['id']))
        else:
            return self.reply_text('绑定失败')

class GetAllConfListHandler(WeChatHandler):

    def check(self):
        return self.is_text('所有会议') or self.is_event_click(self.view.event_keys['get_ticket'])

    def handle(self):
        user = UserLogin.objects.filter(unionId = self.input['FromUserName'])
        if user:
            global currpage
            currpage = 1
            url = 'http://60.205.137.139/adminweb/REST/API-V2/allConfList?userid='+str(user[0].user_id)+'&page=1&page_size=3'
            currpage = currpage + 1
            req = urllib.request.urlopen(url)
            content = req.read().decode('utf-8')
            conflist = json.loads(content)
            total_size = conflist['total_size']
            result = []
            if total_size >= 3:
                for i in range(0,3):
                    result.append({
                        'Title': conflist['data'][i]['name'],
                        'PicUrl': 'http://60.205.137.139/adminweb/' + conflist['data'][i]['image'],
                        # 'Url': 'http://m2.huiplus.com.cn/app/#/confinfo/'+str(conflist['data'][i]['id'])
                        'Url': 'http://183.172.88.129/u/meeting/index.html?confid=' + str(conflist['data'][i]['id']) + '&userid=' + str(user[0].user_id)
                    })
                result.append({
                    'Title': '输入“显示更多”，查看更多会议'
                })
            else:
                for i in range(0,total_size):
                    result.append({
                        'Title': conflist['data'][i]['name'],
                        'PicUrl': 'http://60.205.137.139/adminweb/' + conflist['data'][i]['image'],
                        # 'Url': 'http://m2.huiplus.com.cn/app/#/confinfo/'+str(conflist['data'][i]['id'])
                        'Url': 'http://183.172.88.129/u/meeting/index.html?confid=' + str(conflist['data'][i]['id']) + '&userid=' + str(user[0].user_id)
                    })
                result.append({
                    'Title': '没有更多会议了'
                })
            print (result)
            return self.reply_news(result)
        else:
            return self.reply_text("请先绑定")

class ShowMoreConfHandler(WeChatHandler):
    def check(self):
        return self.is_text('显示更多')

    def handle(self):
        user = UserLogin.objects.filter(unionId = self.input['FromUserName'])
        if user:
            global currpage
            url = 'http://60.205.137.139/adminweb/REST/API-V2/allConfList?userid='+str(user[0].user_id)+'&page=' + str(currpage) +'&page_size=3'
            req = urllib.request.urlopen(url)
            content = req.read().decode('utf-8')
            conflist = json.loads(content)
            total_size = conflist['total_size']
            if currpage * 3 < total_size:
            # print (conflist['data'][0])
                result = []
                for i in range(0,3):
                    result.append({
                        'Title': conflist['data'][i]['name'],
                        'PicUrl': 'http://60.205.137.139/adminweb/' + conflist['data'][i]['image'],
                        # 'Url': 'http://m2.huiplus.com.cn/app/#/confinfo/'+str(conflist['data'][i]['id'])
                        'Url': 'http://183.172.88.129/u/meeting/index.html?confid=' + str(conflist['data'][i]['id']) + '&userid=' + str(user[0].user_id)
                    })
                result.append({
                    'Title': '输入“显示更多”，查看更多会议'
                })
                currpage = currpage + 1
                print (currpage)
            else:
                result = []
                for i in range(0,total_size-(currpage-1)*3):
                    result.append({
                        'Title': conflist['data'][i]['name'],
                        'PicUrl': 'http://60.205.137.139/adminweb/' + conflist['data'][i]['image'],
                        # 'Url': 'http://m2.huiplus.com.cn/app/#/confinfo/'+str(conflist['data'][i]['id'])
                        'Url': 'http://183.172.88.129/u/meeting/index.html?confid=confid=' + str(conflist['data'][i]['id']) + '&userid=' + str(user[0].user_id)
                    })
                result.append({
                    'Title': '没有更多会议了'
                })
                currpage = 1
            return self.reply_news(result)
        else:
            return self.reply_text("请先绑定")

class GetComingConfListHandler(WeChatHandler):
    def check(self):
        return self.is_text('近期会议') or self.is_event_click(self.view.event_keys['book_what'])

    def handle(self):
        user = UserLogin.objects.filter(unionId = self.input['FromUserName'])
        if user:
            url = 'http://60.205.137.139/adminweb/REST/API-V2/upcomingConfList?userid='+str(user[0].user_id)+'&page=1&page_size=3'
            req = urllib.request.urlopen(url)
            content = req.read().decode('utf-8')
            conflist = json.loads(content)
            total_size = conflist['total_size']
            if total_size >= 3:
                result = []
                for i in range(0,3):
                    result.append({
                        'Title': conflist['data'][i]['name'],
                        'PicUrl': 'http://60.205.137.139/adminweb/' + conflist['data'][i]['image'],
                        # 'Url': 'http://m2.huiplus.com.cn/app/#/confinfo/'+str(conflist['data'][i]['id'])
                        'Url': 'http://183.172.88.129/u/meeting/index.html?confid=' + str(conflist['data'][i]['id']) + '&userid=' + str(user[0].user_id)
                    })
            else:
                result = []
                for i in range(0,total_size):
                    result.append({
                        'Title': conflist['data'][i]['name'],
                        'PicUrl': 'http://60.205.137.139/adminweb/' + conflist['data'][i]['image'],
                        # 'Url': 'http://m2.huiplus.com.cn/app/#/confinfo/'+str(conflist['data'][i]['id'])
                        'Url': 'http://183.172.88.129/u/meeting/index.html?confid=' + str(conflist['data'][i]['id']) + '&userid=' + str(user[0].user_id)
                    })
            return self.reply_news(result)
        else:
            return self.reply_text("请先绑定")

class SearchConfListHandler(WeChatHandler):
    def check(self):
        return self.is_text_command('查询')

    def handle(self):
        search_name = self.input['Content'][3:]
        user = UserLogin.objects.filter(unionId = self.input['FromUserName'])
        if user:
            url = 'http://60.205.137.139/adminweb/REST/API-V2/searchConfList?userid='+str(user[0].user_id)+'&content='+ urllib.parse.quote(search_name) + '&page=1&page_size=3'
            req = urllib.request.urlopen(url)
            content = req.read().decode('utf-8')
            conflist = json.loads(content)
            total_size = conflist['total_size']
            if len(conflist['data']) == 0:
                return self.reply_text("对不起，并没有找到相应的会议")
            if total_size >= 3:
                result = []
                for i in range(0,3):
                    result.append({
                        'Title': conflist['data'][i]['name'],
                        'PicUrl': 'http://60.205.137.139/adminweb/' + conflist['data'][i]['image'],
                        # 'Url': 'http://m2.huiplus.com.cn/app/#/confinfo/'+str(conflist['data'][i]['id'])
                        'Url': 'http://183.172.88.129/u/meeting/index.html?confid=' + str(conflist['data'][i]['id']) + '&userid=' + str(user[0].user_id)
                    })
            else:
                result = []
                for i in range(0,total_size):
                    result.append({
                        'Title': conflist['data'][i]['name'],
                        'PicUrl': 'http://60.205.137.139/adminweb/' + conflist['data'][i]['image'],
                        # 'Url': 'http://m2.huiplus.com.cn/app/#/confinfo/'+str(conflist['data'][i]['id'])
                        'Url': 'http://183.172.88.129/u/meeting/index.html?confid=' + str(conflist['data'][i]['id']) + '&userid=' + str(user[0].user_id)
                    })
            return self.reply_news(result)
        else:
            return self.reply_text("请先绑定")

class favoriteConfListHandler(WeChatHandler):
    def check(self):
        return self.is_text('我的会议') or self.is_event_click(self.view.event_keys['my_meeting'])

    def handle(self):
        user = UserLogin.objects.filter(unionId = self.input['FromUserName'])
        if user:
            url = 'http://60.205.137.139/adminweb/REST/API-V2/favoriteConfList?userid='  +str(user[0].user_id)+  '&page=1&page_size=3'
            req = urllib.request.urlopen(url)
            content = req.read().decode('utf-8')
            conflist = json.loads(content)
            total_size = conflist['total_size']
            print (total_size)
            if len(conflist['data']) == 0:
                return self.reply_text("您并未关注，收藏或参加任何会议")
            if total_size >= 3:
                result = []
                for i in range(0, 3):
                    result.append({
                        'Title': conflist['data'][i]['name'],
                        'PicUrl': 'http://60.205.137.139/adminweb/' + conflist['data'][i]['image'],
                        'Url': 'http://m2.huiplus.com.cn/app/#/confinfo/'+str(conflist['data'][i]['id'])
                        
                    })
            else:
                result = []
                for i in range(0, total_size):
                    result.append({
                        'Title': conflist['data'][i]['name'],
                        'PicUrl': 'http://60.205.137.139/adminweb/' + conflist['data'][i]['image'],
                        'Url': 'http://m2.huiplus.com.cn/app/#/confinfo/'+str(conflist['data'][i]['id'])
                        
                    })
            return self.reply_news(result)
        else:
            return self.reply_text("请先绑定")


class confRemindHandler(WeChatHandler):
    def check(self):
        return self.is_text('提醒') or self.is_event_click(self.view.event_keys['remind'])

    def handle(self):
        user = UserLogin.objects.filter(unionId = self.input['FromUserName'])
        if user:
            url = 'http://60.205.137.139/adminweb/REST/API-V2/favoriteConfList?userid='  +str(user[0].user_id)+  '&page=1&page_size=3'
            req = urllib.request.urlopen(url)
            content = req.read().decode('utf-8')
            conflist = json.loads(content)
            total_size = conflist['total_size']
            mtime = time.localtime(int(self.input['CreateTime']))
            timeStr=time.strftime("%Y-%m-%d", mtime)
            result = ""
            if len(conflist['data']) == 0:
                return self.reply_text("没有与您相关的会议，不需要提醒")
            for i in range(0, total_size):
                for j in (0, i-1):
                    if conflist['data'][i]['start_date'] < conflist['data'][j]['start_date']:
                        temp = conflist['data'][i]
                        conflist['data'][i] = conflist['data'][j]
                        conflist['data'][j] = temp
            for i in range(0, total_size):
                # if conflist['data'][i]['start_date'] > timeStr:
                    result = result + "你的会议" + conflist['data'][i]['name'] + "将于" + conflist['data'][i]['start_date'] + "在" + conflist['data'][i]['location'] + "召开"
                    if i != total_size - 1:
                        result = result + '\n\n'
            if result == "":
                return self.reply_text("你近期没有会议")
            else:
                return self.reply_text(result)
        else:
            return self.reply_text("请先绑定")