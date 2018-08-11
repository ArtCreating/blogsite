import datetime
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from read_statistics.utils import *
from blog.models import Blog


def get_hot_blogs_in_seven_days():
	today = timezone.now().date()
	date = today - datetime.timedelta(days=7)
	blogs = Blog.objects \
					.filter(read_details__date__lt=today, read_details__date__gte=date) \
					.values('id','title') \
					.annotate(read_num_sum=Sum('read_details__read_num')) \
					.order_by('-read_num_sum')
	return blogs[:7]


def home(request):
	blog_content_type = ContentType.objects.get_for_model(Blog)
	dates, read_nums = get_seven_days_read_data(blog_content_type)

	#获取7天热门博客的缓存数据
	hot_blogs_in_seven_days = cache.get('hot_blogs_in_seven_days')
	if hot_blogs_in_seven_days is None:
		hot_blogs_in_seven_days = get_hot_blogs_in_seven_days()
		cache.set('hot_blogs_in_seven_days', hot_blogs_in_seven_days , 3600)
		print('cae')
	else:
		print('use cache')

	context = {}
	context['read_nums'] =read_nums
	context['dates'] = dates
	context['today_hot_read_data'] = get_today_hot_read_data(blog_content_type)
	context['yesterday_hot_read_data'] = get_yesterday_hot_read_data(blog_content_type)
	context['hot_blogs_in_seven_days'] = hot_blogs_in_seven_days
	return render(request, 'home.html', context)

