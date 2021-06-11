from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.
def login_view(request):
	if(request.method == 'POST'):
		u = request.POST['username']
		p = request.POST['password']
		user = auth.authenticate(username=u,password=p)

		if( user is not None):
			auth.login(request, user) 
			return redirect('/')
		else:
			messages.info(request,'invalid credentials')

	return render(request,'login.html')

def register(request): 
	if request.method=='POST':

		f = request.POST['first_name']
		l = request.POST['last_name']
		username = request.POST['username']
		p1 = request.POST['password1']
		p2 = request.POST['password2']
		email = request.POST['email']

		if(p1==p2): 
			if(User.objects.filter(username=username).exists()):
				messages.info(request,'username aleady taken')
			elif(User.objects.filter(email=email).exists()):
				messages.info(request,'email already taken')
			else:
				user = User.objects.create_user(username=username, password=p1, email=email,first_name=f,last_name=l)
				user.save();
				print('user created')
				auth.login(request, user)
				return redirect('/') # going to home page

		else:
			messages.info(request,'password does not matched')
	return render(request,'register.html')
def logout_view(request):
	auth.logout(request)
	return redirect('/')