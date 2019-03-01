from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import chardet
import logging

logging.basicConfig(filename='/var/log/iotdemo/digimove.log',level=logging.DEBUG)

# Create your views here.
def login(request):
	return render(request,'genset/index.html')

def get_login_data(request):
	email = request.POST.get('email')
	pwd = request.POST.get('pass')
	if email == 'kripa@digimove.com' and pwd == 'iot@123':
		return render(request,'genset/deshboard.html')
	else:
		return render(request,'genset/notfound.html')

data_test = {'v1':'100','v2':'','v3':''}
@csrf_exempt
@require_http_methods(["POST"])
def data(request):
        if request.body:
                json_data = request.body.decode('utf-8')
                body_data = json.loads(json_data)
                global data_test
                data_test = {'v1':'100','v2':'','v3':''}
                data_test['v1'] = body_data['voltageT1']
                data_test['v2'] = body_data['voltageT2']
                data_test['v3'] = body_data['voltageT3']
                logging.info((data_test['v1']))
        return HttpResponse('ok')

def get_data(request):
	return HttpResponse(data_test['v1'])

@csrf_exempt
@require_http_methods(["POST"])
def get_data_from_node(request):
	if request.body:
                json_data = request.body.decode('utf-8')
                body_data = json.loads(json_data)
                temp_test  = {}
		time_stamp = body_data['timeStamp']
		logging.info("time stamp is >>>>>>>>>>>>>")
		logging.info(time_stamp)
		node_pin = body_data['nodePin']
		logging.info("node pin is >> {}".format(node_pin))
                temp_test['v1'] = body_data['voltageT1']
                temp_test['v2'] = body_data['voltageT2']
                temp_test['v3'] = body_data['voltageT3']
		logging.info("voltage in t1 >> {} , t2 >> {} and t3 >> {}".format(temp_test['v1'],temp_test['v2'],temp_test['v3']))
		temp_test['c1'] = body_data['currentT1']
		temp_test['c2'] = body_data['currentT2']
		temp_test['c3'] = body_data['currentT3']
		temp_test['c1'] = body_data['currentT1']
		logging.info("current in t1 >> {} , t2 >> {} and t3 >> {}".format(temp_test['c1'],temp_test['c2'],temp_test['c3']))
		avg_voltage = (int(body_data['voltageT1']) + int(body_data['voltageT2']) + int(body_data['voltageT1']))/3
		avg_current = (int(body_data['currentT1']) + int(body_data['currentT1']) + int(body_data['currentT1']))/3
                logging.info("avg voltage and current is >> {} and {}".format(avg_voltage,avg_current)
        return HttpResponse('ok')




















