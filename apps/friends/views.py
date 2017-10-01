from django.shortcuts import render, redirect

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.

def index(request):
	return render(request, 'friends/index.html')

def register(request):
	if request.method == 'POST':

		users = User.usrMgr.filter(email=request.POST['email'])
		if users:
			messages.add_message(request, messages.ERROR, 'User already exists', extra_tags='registration')
			return redirect('/')

		else:
			reg = User.usrMgr.register(request.POST)

			if reg[0] == True:
				request.session['id'] = reg[1]
				request.session['status'] = 'registered'
				return redirect('/friends')

		# Fail:
			else:
				error_reg = reg[1]
				for i in range (len(error_reg)):
					messages.add_message(request, messages.ERROR,
						error_reg[i], extra_tags='registration')
				return redirect('/')
	else:
		return redirect('/')


def login(request):
	if request.method == 'POST':
		users = User.usrMgr.filter(email=request.POST['email'])

		if not users and len(request.POST['email']) != 0:
			messages.add_message(request, messages.ERROR, 'User is not in database -- Please register', extra_tags='login')
			return redirect('/')

		else:
			log_in = User.usrMgr.login(request.POST)

			if log_in[0] == True:
				request.session['id'] = log_in[1]
				request.session['status'] = 'logged_in'
				return redirect('/friends')

		## If Fail:
			else:
				error_login = log_in[1]
				for i in range (len(error_login)):
					messages.add_message(request, messages.ERROR,
						error_login[i], extra_tags='login')
				return redirect('/')
	else:
		return redirect('/')



def friends(request):
	user = User.usrMgr.filter(id=request.session['id'])
	this_user = user[0]
	user_friends = User.usrMgr.filter(friends=this_user)
	all_users = User.usrMgr.exclude(friends=this_user).exclude(name=this_user.name)

	context = {
		'user': user[0],
		'user_friends': user_friends,
		'all_users': all_users
		}
	return render(request, 'friends/friends.html', context)



def addFriend(request, id):

	user = User.usrMgr.filter(id=request.session['id'])
	friend = User.usrMgr.filter(id=id)

	added_friend = User.usrMgr.addFriend(user, friend)
	return redirect('/friends')


def user(request, id):
	user = User.usrMgr.filter(id=id)
	this_user = user[0]

	context = {'this_user': this_user}
	return render(request, 'friends/user.html', context)


def remove(request, id):

	user = User.usrMgr.filter(id=request.session['id'])
	friend = User.usrMgr.filter(id=id)

	removed_friend = User.usrMgr.removeFriend(user, friend)
	return redirect('/friends')


def logout(request):
	request.session.pop('id')
	return redirect('/')
