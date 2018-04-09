from __future__ import unicode_literals
# Create your models here.

from django.core.files.storage import FileSystemStorage
from hashlib import sha1
from db.base_model import BaseModel
from django.db import models

from tinymce.models import HTMLField
fs = FileSystemStorage(location='/media/photos')


def get_hash(str):
	sh = sha1()
	sh.update(str.encode('utf-8'))
	return sh.hexdigest()


class PassportManager(models.Manager):
	def add_one_passport(self, username, password, email):
		passport = self.create(username=username, password=get_hash(password), email=email)
		return passport

	"""查找"""

	def get_one_passport(self, username, password):
		try:
			passport = self.get(username=username, password=get_hash(password))
		except Exception as e:
			passport=None
			print('用户不存在')
		else:
			return passport
class Passport(BaseModel):
	username = models.CharField(max_length=20,verbose_name='用户名称')
	password = models.CharField(max_length=40,verbose_name='密码')
	email = models.EmailField(verbose_name='用户邮件')
	is_active = models.BooleanField(default=False,verbose_name='激活状态')
	objects = PassportManager()
	class Meta:
		db_table ='s_users_account'

class HeroInfo(models.Model):

	hcontent = HTMLField()

class AddressManager(models.Manager):
	def get_default_address(self, passport_id):
		try:
			addr = self.get(passport_id=passport_id, is_default=True)
		except self.model.DoesNotExist:
			addr = None
		return addr

	def add_one_address(self, passport_id, recipient_name, recipient_addr, zip_code, recipient_phone):
		addr = self.get_default_address(passport_id=passport_id)
		if addr:
			is_default = False
		else:
			is_default = True

		addr = self.create(passport_id=passport_id,
						   recipient_name=recipient_name,
						   recipient_addr=recipient_addr,
						   zip_code=zip_code,
						   recipient_phone=recipient_phone,
						   is_default=is_default)

		return addr
class Address(BaseModel):
	recipient_name =models.CharField(max_length=20,verbose_name='收件人')
	recipient_addr = models.CharField(max_length=256,verbose_name='收件地址')
	zip_code = models.CharField(max_length=6,verbose_name='邮政编码')
	recipient_phone = models.CharField(max_length=11, verbose_name='联系电话')
	is_default = models.BooleanField(default=False, verbose_name='是否默认')
	passport = models.ForeignKey('Passport', verbose_name='账户')

	objects = AddressManager()
	class Meta:
		db_table = 's_user_address'


