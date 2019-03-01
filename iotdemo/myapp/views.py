from django.shortcuts import render
from django.http import HttpResponse
import json
import chardet
# Create your views here.

status = ""
def home(request):
	global status
	status = "OFF"
	data = {'status':status}
	return render(request,'index.html',data)
def subscribe(request):
	data = {'status':status}
	var = status
	#return render(request,'sub.html',data)
	return HttpResponse("OFF")
def publish_on(request):
	global status	
	status = "ON"
	data = {'status':status}
	return render(request,'index.html',data)
def publish_off(request):
	global status
	status="OFF"
	data = {'status':status}
	return render(request,'index.html',data)
def check_data(request):
	data = request.GET.get('data')
	return HttpResponse(data)
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@require_http_methods(["POST"])
def check_data_test(request):
	if request.body:
		json_data = request.body.decode('utf-8')
		body_data = json.loads(json_data)
		data = body_data['data']
	return HttpResponse(data)
        #data = request.POST.get('data')
        #return HttpResponse(data)
