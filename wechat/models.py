from django.db import models

from codex.baseerror import LogicError

class UserLogin(models.Model):
    user_id = models.IntegerField()
    email = models.CharField(max_length=256, blank=True, null=True)
    unionId = models.CharField(max_length=256)

class ConfBasic(models.Model):
    confbasic_id = models.IntegerField()
    name = models.CharField(max_length=128)
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(db_index=True)
    location = models.CharField(max_length=256)
    image = models.CharField(max_length=256)
    version = models.IntegerField()
    private_type = models.IntegerField()
    color = models.CharField(max_length=64)
    sequence = models.CharField(max_length=256)
    status = models.IntegerField()

    TYPE_PUBLIC = 0
    TYPE_PRIVATE = 1
    TYPE_MONEY = 2
    STATUS_INIT = 0
    STATUS_PREPARE = 1
    STATUS_TEST = 2
    STATUS_PUBLISHED = 3
    STATUS_FILE = 4
    STATUS_END = 9

class ConfDetail(models.Model):
    confid = models.IntegerField()
    preview_code = models.CharField(max_length = 128)
    zipcode = models.CharField(max_length=16)
    desc = models.CharField(max_length=256)
    poster = models.CharField(max_length=256)
    org = models.CharField(max_length=128)
    website = models.CharField(max_length=256)
    reg_url = models.CharField(max_length=256)
    phone = models.CharField(max_length=32)
    fax = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    address = models.CharField(max_length=128)
    weibo = models.CharField(max_length=64)
    weixin = models.CharField(max_length=64)
    qq = models.CharField(max_length=16)
    longitude = models.CharField(max_length=32)
    latitude = models.CharField(max_length=32)
    timeZone = models.CharField(max_length=32)
    privateType = models.IntegerField()

    TYPE_PUBLIC = 0
    TYPE_PRIVATE = 1
    TYPE_MONEY = 2

class User(models.Model):
    open_id = models.CharField(max_length=64, unique=True, db_index=True)
    # student_id = models.CharField(max_length=32, unique=True, db_index=True)

    @classmethod
    def get_by_openid(cls, openid):
        try:
            return cls.objects.get(open_id=openid)
        except cls.DoesNotExist:
            raise LogicError('User not found')


class Activity(models.Model):
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=64, db_index=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    place = models.CharField(max_length=256)
    book_start = models.DateTimeField(db_index=True)
    book_end = models.DateTimeField(db_index=True)
    total_tickets = models.IntegerField()
    status = models.IntegerField()
    pic_url = models.CharField(max_length=256)
    remain_tickets = models.IntegerField()

    STATUS_DELETED = -1
    STATUS_SAVED = 0
    STATUS_PUBLISHED = 1


class Ticket(models.Model):
    student_id = models.CharField(max_length=32, db_index=True)
    unique_id = models.CharField(max_length=64, db_index=True, unique=True)
    activity = models.ForeignKey(Activity)
    status = models.IntegerField()

    STATUS_CANCELLED = 0
    STATUS_VALID = 1
    STATUS_USED = 2
