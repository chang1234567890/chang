from django.shortcuts import render
from django.http import JsonResponse
from books.models import Books
from utils.decorators import login_required
from django_redis import get_redis_connection
# Create your views here.

def cart_add(request):
	if not request.session.has_key('islogin'):
		return  JsonResponse({'res':0,'errmsg':'请先登陆'})
	books_id = request.POST.get('books_id')
	books_count = request.POST.get('books_count')
	if not all([books_id,books_count]):
		return  JsonResponse({'res':1,'errmsg':'数据不完整'})
	books = Books.objects.get_books_by_id(books_id=books_id)
	if books is None:
		return JsonResponse({'res':2,'errmsg':'商品不存在'})
	try:
		count = int(books_count)
	except Exception as e:
		return  JsonResponse({'res':3,'errmsg':'商品数量必须为数字'})
	conn = get_redis_connection('default')
	cart_key = 'cart_%d' % request.session.get('passport_id')
	res = conn.hget(cart_key,books_id)
	if res is None:
		res = count
	else:
		res = int(res)+count
	if res > books.stock:

		return JsonResponse({'res':4,'errmsg':'商品库存不足'})
	else:
		conn.hset(cart_key,books_id,res)
	return JsonResponse({'res':5})
def cart_count(request):
	if not request.session.has_key('islogin'):
		return JsonResponse({'res':0})
	conn = get_redis_connection('default')
	cart_key = 'cart_%d' % request.session.get('passport_id')
	res = 0
	res_list = conn.hvals(cart_key)

	for i in res_list:
		res += int(i)

	return JsonResponse({'res':res})
