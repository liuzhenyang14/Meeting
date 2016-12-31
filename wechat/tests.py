from django.test import TestCase, Client, LiveServerTestCase
from django.contrib.auth.models import User as Admin
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from wechat.models import *
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import time
import json
import os


class AllTest(TestCase):
    def setUp(self):
        Admin.objects.create_superuser('thssxsy', 'pxxsy@163.com', 'xsy2491239')
        Activity.objects.create(
            key='activity1',
            name='speech1',
            description='master speech',
            start_time='2016-11-11T12:00:00.000Z',
            end_time='2016-11-11T13:00:00.000Z',
            place='church',
            book_start='2016-11-01T12:00:00.000Z',
            book_end='2016-11-02T12:00:00.000Z',
            total_tickets=100,
            status=Activity.STATUS_PUBLISHED,
            pic_url='./static/img/logo.jpg',
            remain_tickets=100,
            menu_index=1,
            used_tickets=0,
            id='1'
        )
        self.client = Client(enforce_csrf_checks=True)

    def test_MeetingDetail(self):
        response = self.client.get('/api/u/meeting/', {'confid': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['code'], 0)

    def test_MeetingDetail(self):
        response = self.client.get('/api/u/meeting/pay', {'confid': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['code'], 0)

    def test_MeetingDetail(self):
        response = self.client.get('/api/u/meeting/outmeeting', {'confid': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['code'], 0)

class UserBind(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(UserBind, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(UserBind, cls).tearDownClass()

    def test_UserBind(self):
        self.browser.get('%s%s' % (self.live_server_url, '/wechat/'))
        # wrong input
        time.sleep(2)
        WebDriverWait(self.browser, 10).until(expected_conditions.element_to_be_clickable((By.ID, 'submitBtn')))
        submit = self.browser.find_element_by_id('submitBtn')
        submit.click()
        time.sleep(5)
        self.assertIn('认证成功', self.browser.find_element_by_id('mainbody').text)

class UserMeetingDetail(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(UserBind, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(UserBind, cls).tearDownClass()

    def test_UserBind(self):
        self.browser.get('%s%s' % (self.live_server_url, '/u/meeting'))


class UserMeetingDetail(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(UserBind, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(UserBind, cls).tearDownClass()

    def test_UserBind(self):
        self.browser.get('%s%s' % (self.live_server_url, '/u/meeting'))

class UserMeetingPay(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(UserBind, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(UserBind, cls).tearDownClass()

    def test_UserBind(self):
        self.browser.get('%s%s' % (self.live_server_url, '/u/meeting/pay'))

# Create your tests here.
