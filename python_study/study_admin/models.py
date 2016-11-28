from django.db import models
from django.utils import timezone
import os
import binascii
from hashlib import pbkdf2_hmac

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=128)
    encrypted_password = models.CharField(max_length=256)
    salt = models.CharField(max_length=256)
    encrypt_cycle = models.IntegerField(default=25000)
    is_valid = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    @staticmethod
    def now_login(request):
        if 'login_user_id' in request.session:
            return True
        else:
            return False

    @staticmethod
    def get_login_user(request):
        if User.now_login(request):
            return User.objects.get(pk=request.session.get('login_user_id'))
        return None

    @staticmethod
    def login_user_is_admin(request):
        user = User.get_login_user(request)
        if user and user.is_admin:
            return True
        else:
            return False

    def _generate_salt(self):
        return binascii.hexlify(os.urandom(255)).decode()[:255]

    def _encrypt_password(self, raw_password, salt, encrypt_cycle=25000):
        return binascii.hexlify(pbkdf2_hmac('sha256', raw_password.encode('utf-8'), salt.encode('utf-8'), encrypt_cycle)).decode()

    def set_password(self, raw_password):
        salt = self._generate_salt()
        self.salt = salt
        self.encrypted_password = self._encrypt_password(raw_password, salt)
        return

    def compare_password(self, raw_password):
        if self._encrypt_password(raw_password, self.salt, int(self.encrypt_cycle)) == self.encrypted_password:
            return True
        else:
            return False

    @staticmethod
    def set_login(request, username, raw_password):
        user_qs = User.objects.filter(username=username)
        if not user_qs:
            return (False, 'username 또는 password가 잘못되었습니다')
        user = user_qs.last()
        if not user.compare_password(raw_password):
            return (False, 'username 또는 password가 잘못되었습니다')
        if not user.is_valid:
            return (False, '유효하지 않은 계정입니다')
        request.session['login_user_id'] = user.id
        return (True, '로그인 성공')

    @staticmethod
    def set_logout(request):
        if 'login_user_id' in request.session:
            del request.session['login_user_id']
        return

    @staticmethod
    def create_user(username, raw_password):
        if User.objects.filter(username=username):
            return (None, '해당 username이 이미 존재합니다')
        user = User(
            username=username,
        )
        user.set_password(raw_password)
        user.save()
        return (user, '가입 성공')

    def __str__(self):
        return self.username


class Article(models.Model):
    chapter = models.CharField(max_length=8)  # e.g. 1.10
    title = models.CharField(max_length=128)
    content = models.TextField()
    write_at = models.DateTimeField(default=timezone.now)
    publish_at = models.DateTimeField(null=True, blank=True)
    is_visible = models.BooleanField(default=False)

    def publish(self):
        self.publish_at = timezone.now()
        self.is_visible = True
        self.save()
        return

    def __str__(self):
        return '%s.%s %s' % (self.big_chapter, self.small_chapter, self.title)
