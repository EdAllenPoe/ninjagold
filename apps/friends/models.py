from __future__ import unicode_literals

from django.db import models



import re, bcrypt, datetime


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z\s]*$')
PW_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')




class UserManager(models.Manager):


	def register(self, post):
		reg_errors=[]


		if len(post['name']) <= 2:
			reg_errors.append('Name must be longer than 2 characters')
		elif not NAME_REGEX.match(post['name']):
			reg_errors.append('Name must be alphabetical characters only')

		if len(post['alias']) <= 2:
			reg_errors.append('Alias must be longer than 2 characters')

		if len(post['email']) == 0:
			reg_errors.append('Email field cannot be empty')
		elif not EMAIL_REGEX.match(post['email']):
			reg_errors.append('Email address is not valid')


		if len(post['password']) < 8:
			reg_errors.append('Password must be at least 8 characters')
		elif post['password'] != post['confirm']:
			reg_errors.append('Passwords do not match')

		if not post['birth_date']:
			reg_errors.append('Please enter a date of birth')
		elif datetime.datetime.strptime(post['birth_date'], '%Y-%m-%d').date() > datetime.datetime.now().date():
			reg_errors.append('Cmon, I know you are older than that')


		if len(reg_errors) != 0:
			return(False, reg_errors)


		else:
			pw_str = str(post['password'])
			hashed = bcrypt.hashpw(pw_str, bcrypt.gensalt())
			user = User.usrMgr.create(
				name=post['name'],
				alias=post['alias'],
				email=post['email'],
				password=hashed,
				birth_date=post['birth_date']
				)
			users = User.usrMgr.filter(email=post['email'])
			user_id = users[0].id
			return (True, user_id)



	def login(self, post):
		log_errors = []

		user = User.usrMgr.filter(email=post['email'])

		if len(post['email']) == 0:
			log_errors.append('Email field cannot be empty')
		elif not EMAIL_REGEX.match(post['email']):
			log_errors.append('Email address is not valid')


		if len(post['password']) == 0:
			log_errors.append('Password field cannot be empty')
		elif bcrypt.hashpw(str(post['password']), str(user[0].password)) != user[0].password:
			log_errors.append('Password is not correct')

		if len(log_errors) != 0:
			return(False, log_errors)


		else:
			user_id = user[0].id
			return (True, user_id)



	def addFriend(self, user, friend):
		user = user[0]
		friend = friend[0]

		added_friend = friend.friends.add(user)
		return added_friend



	def removeFriend(self, user, friend):
		user = user[0]
		friend = friend[0]

		removed_friend = friend.friends.remove(user)
		return removed_friend



class User(models.Model):
	name = models.CharField(max_length=50)
	alias = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	friends = models.ManyToManyField('self', related_name='friends')
	password = models.CharField(max_length=50)
	birth_date = models.DateField(auto_now=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	usrMgr = UserManager()
