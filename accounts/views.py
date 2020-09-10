from django.core.mail import send_mail
from django.shortcuts import redirect

def send_login_email(request):
	email = request.POST['email']
	send_mail(
		'Your login link for TheToDoListSite', 
		'body text tbc', 
		'noreply@thetodolistsite', 
		[email]
	)
	return redirect('/')
