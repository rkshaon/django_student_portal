from django.shortcuts import render, redirect, get_object_or_404
from django.urls import resolve
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Sum
from django.db import transaction
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator

from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm

from django.contrib.auth.models import User
from authy.models import Profile

def sign_up(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('edit_profile')
	else:
		form = SignupForm()

	context = {
		'form':form,
	}

	return render(request, 'registration/signup.html', context)

def SideNavInfo(request):
	user = request.user
	nav_profile = None
	fans = None
	follows = None

	if user.is_authenticated:
		nav_profile = Profile.objects.get(user=user)
		fans = Subscription.objects.filter(subscribed=user).count()
		follows = Subscription.objects.filter(subscriber=user).count()

	return {'nav_profile': nav_profile, 'fans': fans, 'follows': follows}


def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	url = request.resolver_match.url_name

	tiers = None
	no_a_subscriber = None
	posts = None
	page_type = None
	posts_data = None

	if request.user != user:
		try:
			#Check if the user is subscribed to the profile
			subscriber_tier = Subscription.objects.get(subscriber=request.user, subscribed=user, expired=False)
			#Then we get the tiers of the profile and exclude the tiers that we are currently subscribed
			tiers = Tier.objects.filter(user=user).exclude(number=subscriber_tier.tier.number)
			if url == 'profilephotos':
				posts = PostFileContent.objects.filter(user=user, tier__number__lte=subscriber_tier.tier.number).order_by('-posted').exclude(file__endswith='mp4')
				page_type = 1
			elif url == 'profilevideos':
				posts = PostFileContent.objects.filter(user=user, tier__number__lte=subscriber_tier.tier.number).order_by('-posted').exclude(file__endswith='jpg')
				page_type = 2
			else:
				posts = Post.objects.filter(user=user, tier__number__lte=subscriber_tier.tier.number).order_by('-posted')
				page_type = 3
		except Exception:
			tiers = Tier.objects.filter(user=user)
			no_a_subscriber = False
	else:
		if url == 'profilephotos':
			posts = PostFileContent.objects.filter(user=user).order_by('-posted').exclude(file__endswith='mp4')
			page_type = 1
		elif url == 'profilevideos':
			posts = PostFileContent.objects.filter(user=user).order_by('-posted').exclude(file__endswith='jpg')
			page_type = 2
		else:
			posts = Post.objects.filter(user=user).order_by('-posted')
			page_type = 3

	#Pagination
	if posts:
		paginator = Paginator(posts, 6)
		page_number = request.GET.get('page')
		posts_data = paginator.get_page(page_number)

	#Profile stats
	income = Subscription.objects.filter(subscribed=user, expired=False).aggregate(Sum('tier__price'))
	fans_count = Subscription.objects.filter(subscribed=user, expired=False).count()
	posts_count = Post.objects.filter(user=user).count()


	#Favorite people lists select
	favorite_list = PeopleList.objects.filter(user=request.user)

	#Check if the profile is in any of favorite list
	person_in_list = PeopleList.objects.filter(user=request.user, people=user).exists()

	#New Favorite List form
	if request.method == 'POST':
		form = NewListForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data.get('title')
			PeopleList.objects.create(title=title, user=request.user)
			return HttpResponseRedirect(reverse('profile', args=[username]))
	else:
		form = NewListForm()

	template = loader.get_template('profile.html')

	context = {
		'profile':profile,
		'tiers': tiers,
		'form': form,
		'favorite_list': favorite_list,
		'person_in_list': person_in_list,
		'posts': posts_data,
		'page_type': page_type,
		'income': income,
		'fans_count': fans_count,
		'posts_count': posts_count,
		'no_a_subscriber': no_a_subscriber,

	}

	return HttpResponse(template.render(context, request))



@login_required
def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change_password_done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form':form,
	}

	return render(request, 'registration/change_password.html', context)

def PasswordChangeDone(request):
	return render(request, 'change_password_done.html')


@login_required
def edit_profile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	user_basic_info = User.objects.get(id=user)

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.banner = form.cleaned_data.get('banner')
			user_basic_info.first_name = form.cleaned_data.get('first_name')
			user_basic_info.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			user_basic_info.save()
			return redirect('index')
	else:
		form = EditProfileForm(instance=profile)

	context = {
		'form':form,
	}

	return render(request, 'registration/edit_profile.html', context)
