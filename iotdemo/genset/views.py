from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .datafile.dataoperation import DataOperation
from .iotsrc.utils import Utilities
from datetime import datetime, date, time
from django.views.static import serve
from . import models
import json
import chardet
import logging
import os
logging.basicConfig(filename='/var/log/iotdemo/digimove_new.log',level=logging.DEBUG)


# Create your views here.

device_info = {'cPin':'0','avg_voltage':0,'avg_current':0,'avg_load':0,'data':'ok'}

			   
def insert_user(request):
	try:
		obj = models.NodePin(nodepin = '0001')
		obj.save()
		return HttpResponse('ok')
	except Exception as ex:
		return HttpResponse('error')

def login(request):
	return render(request,'genset/index.html')

def get_login_data(request):
	node_pin = request.POST.get('npin')
	if models.NodePin.objects.filter(nodepin=node_pin):
		request.session['node_pin'] = node_pin
		return render(request,'genset/genset_deshboard.html')
	else:
		return HttpResponse("<html><body><h1 align='center' style='color:red'>OOPS! Incorrect Pin </h1></body></html>")

def logout(request):
	try:
		del request.session['node_pin']
	except:
		pass
	return redirect('/')

def genset_deshboard(request):
	if request.session.has_key('node_pin'):
		return render(request, 'genset/genset_deshboard.html')
	else:
                return render(request,'genset/notfound.html')

def get_status_flag(voltage):
	data = dict(DataOperation().read_data_from_file())
	before_resp_voltage =  int(data['avg_voltage'])
	after_resp_voltage = int(voltage)
	if before_resp_voltage == 0 and after_resp_voltage > 0:
		return 'start'
	elif before_resp_voltage > 0 and after_resp_voltage <= 0:
		return 'stop'
	else:
		return 'ok'
def get_one_day_running_time():
	today_min = datetime.combine(date.today(), time.min)
	today_max = datetime.combine(date.today(), time.max)
	start_data = models.GenSetData.objects.filter(date__range=(today_min, today_max), status_tag = 'start')
	stop_data = models.GenSetData.objects.filter(date__range=(today_min, today_max), status_tag = 'stop')
	start_list = []
	stop_list = []
	for item in start_data:
		start_list.append(item.date)
	for item in stop_data:
		stop_list.append(item.date)
	couple_list = zip(start_list,stop_list)
	running_time = []
	total_running_time = []
	for start,stop in couple_list:
		temp_list = []
		temp  = stop - start
		total_running_time.append(temp)
		duration = str(temp)
		temp1 = start.strftime("%y/%m/%d,%H:%M:%S").split(',')
		mydate = temp1[0]
		mytime = temp1[1]
		temp_list.append(mydate)
		temp_list.append(mytime)
		temp_list.append(duration)
		running_time.append(temp_list)
	time1 = datetime.now()
	time2 = datetime.now()
	total_time = time2 - time1
	for i in total_running_time:
		total_time = total_time + i
	temp = str(total_time).split('.')
	total_time = temp[0]
	data = {}
	if len(running_time) != 0:
		data['day_running_time'] = running_time
	else:
		data['day_running_time'] = [['NA','NA','NA']]
	if len(total_time) != 0:
		data['total_running_time'] = total_time
	else:
		data['total_running_time'] = '00:00:00'
	return data


def genset_report(request):
	if request.session.has_key('node_pin'):
		data = dict(DataOperation().read_data_from_file())
		v1_range = range(1,220)
		v_range  = range(220,251)
		c_range  = range(0,201)
		l_range  = range(0,100000)
		if data['avg_voltage'] in v_range:
			data['vFlage'] = ['ok']
		elif data['avg_voltage'] in v1_range:
			data['vFlage'] = ['warning']
		elif data['avg_voltage'] == 0 :
			data['vFlage'] = ['ok']
		else:
			data['vFlage'] = ['error']
		if data['avg_current'] in c_range:
			data['cFlage'] = ['ok']
		else:
			data['cFlage'] = ['error']
		if data['avg_load'] in l_range:
			data['lFlage'] = ['ok']
		else:
			data['lFlage'] = ['error']
		if data['avg_voltage'] >= 1 :
			data['cstatus'] = ['running']
		else:
			data['cstatus'] = ['not_running']
		try:
			data['one_day_total_running_time'] = get_one_day_running_time()['total_running_time']
		except Exception as ex:
			logging.error("Error in addind total running time")
			logging.error(ex)
			data['one_day_total_running_time'] = '00:00:00'
		try:
			data['whole_day_running_time'] = get_one_day_running_time()['day_running_time']
		except Exception as ex:
			logging.error("Error in adding whole day running time")
			logging.error(ex)
			data['whole_day_running_time'] = [['NA','NA','NA']]
		return render(request, 'genset/genset_report.html',data)
	else:
                return render(request,'genset/notfound.html')

def genset_alarm(request):
	if request.session.has_key('node_pin'):
		return render(request, 'genset/genset_alarm.html')
	else:
                return render(request,'genset/notfound.html')


#data_test = {'v1':'100','v2':'','v3':''}
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@require_http_methods(["POST"])
def data(request):
	if request.body:
		try:
			data_dict = json.loads(request.body.decode('utf-8'))
		except Exception as ex:
			return HttpResponse('ok')
		else:
			logging.info(("Getting data..."))
			logging.info((data_dict))
			global device_info
			if 'cPin' in data_dict:
			#if data_dict['cPin'] == '0002':
				device_info['cPin'] = data_dict['cPin']
				'''if 'voltageT1' in data_dict:
					if int(data_dict['voltageT1']) >= 100:
						device_info['v1'] = int((0.345*int(data_dict['voltageT1']))-56)
					else:
						device_info['v1'] = 0
				if 'voltageT2' in data_dict:
					if int(data_dict['voltageT2']) >= 100:
						device_info['v2'] = int((0.345*int(data_dict['voltageT2']))-56)
					else:
						device_info['v2'] = 0
				if 'voltageT3' in data_dict:
					if int(data_dict['voltageT3']) >= 100:
						device_info['v3'] = int((0.345*int(data_dict['voltageT3']))-56)
					else:
						device_info['v3'] = 0
				if 'currentT1' in data_dict:
					if int(data_dict['currentT1']) >= 525:
						device_info['c1'] = int(((int(data_dict['currentT1'])-511)*8.63)-30)
					else:
						device_info['c1'] = 0
				if 'currentT2' in data_dict:
					if int(data_dict['currentT2']) >= 525:
						device_info['c2'] = int(((int(data_dict['currentT2'])-511)*8.63)-30)
					else:
						device_info['c2'] = 0
				if 'currentT3' in data_dict:
					if int(data_dict['currentT3']) >= 525:
						device_info['c3'] = int(((int(data_dict['currentT3'])-511)*8.63)-30)
					else:
						device_info['c3'] = 0
				if 'batteryStatus' in data_dict:
					device_info['battery_status'] = data_dict['batteryStatus'] '''
				if 'timeStamp' in data_dict:
					time_split = data_dict['timeStamp'].split(',')
					device_info['current_date'] = str(time_split[0])
					device_info['current_time'] = str(time_split[1])
				if 'data' in data_dict:
					device_info['data'] = data_dict['data']
					if len(data_dict['data']) >= 2:
						mydata = str(data_dict['data'])
						mydata = mydata.split(' ')
						v1 = int(mydata[10])
						v2 = int(mydata[11])
						i1 = int(mydata[12])
						i2 = int(mydata[13])
						l1 = int(mydata[2])
						l2 = int(mydata[3])
						ut = Utilities()
						avg_voltage = ut.result_energy(v1,v2)
						avg_current = ut.result_energy(i1,i2)
						avg_load = (ut.result_energy(l1,l2))/1000
						device_info['avg_voltage'] = int(avg_voltage)
						device_info['avg_current'] = int(avg_current)
						device_info['avg_load'] = int(avg_load)
					else:
						device_info['avg_voltage'] = 0
						device_info['avg_current'] = 0
						device_info['avg_load'] = 0
				else:
					device_info['avg_voltage'] = 0
					device_info['avg_current'] = 0
					device_info['avg_current'] = 0 
			'''avg_voltage = int((int(device_info['v1']) + int(device_info['v2']) + int(device_info['v3']))/3)
			device_info['avg_voltage'] = int(avg_voltage)
			avg_current = int((int(device_info['c1']) + int(device_info['c2']))/2)
			device_info['avg_current'] = int(avg_current)
			avg_load = (avg_voltage*avg_current)
			avg_load = int(int(avg_load)/1000)
			device_info['avg_load'] = avg_load'''
			try:
				status_tag = get_status_flag(int(device_info['avg_voltage']))
			except Exception as ex:
				logging.error("error in getting status tag {}".format(ex))
			try: 
				DataOperation().write_data_in_file(device_info)
				logging.info("data inserted to json!")
			except Exception as ex:
				logging.error("Data not able to insert to json file! Reason is {}".format(ex))
			try:
				dt = datetime.strptime(data_dict['timeStamp'], "%y/%m/%d,%H:%M:%S")
				avg_voltage = int(device_info['avg_voltage'])
				avg_current = int(device_info['avg_current'])
				avg_load = int(device_info['avg_load'])
				var = models.GenSetData(nodepin = device_info['cPin'], date = dt, avg_voltage = avg_voltage, avg_current = avg_current, avg_load = avg_load, status_tag = status_tag)
				var.save()
				logging.info("data inserted to database!")
			except Exception as ex:
				logging.error("Data not able to insert to database! Reason is {}".format(ex))
			return HttpResponse("ok")
	else:
		return HttpResponse('ok')

		

def transf_deshboard(request):
	if request.session.has_key('node_pin'):
		return render(request, 'genset/transf_deshboard.html')
	else:
                return render(request,'genset/notfound.html')

def transf_report(request):
	if request.session.has_key('node_pin'):
		data = dict(DataOperation().read_data_from_file())
		v1_range = range(1,220)
		v_range  = range(220,251)
		c_range  = range(0,201)
		l_range  = range(0,100000)
		if data['avg_voltage'] in v_range:
			data['vFlage'] = ['ok']
		elif data['avg_voltage'] in v1_range:
			data['vFlage'] = ['warning']
		elif data['avg_voltage'] == 0 :
			data['vFlage'] = ['ok']
		else:
			data['vFlage'] = ['error']
		if data['avg_current'] in c_range:
			data['cFlage'] = ['ok']
		else:
			data['cFlage'] = ['error']
		if data['avg_load'] in l_range:
			data['lFlage'] = ['ok']
		else:
			data['lFlage'] = ['error']
		if int(data['avg_voltage']) > 0:
			data['cstatus'] = ['running']
		else:
			data['cstatus'] = ['not_running']
		try:
			data['one_day_total_running_time'] = get_one_day_running_time()['total_running_time']
		except Exception as ex:
			logging.error("Error in addind total running time")
			logging.error(ex)
			data['one_day_total_running_time'] = '00:00:00'
		try:
			data['whole_day_running_time'] = get_one_day_running_time()['day_running_time']
		except Exception as ex:
			logging.error("Error in adding whole day running time")
			logging.error(ex)
			data['whole_day_running_time'] = [['NA','NA','NA']]
		return render(request, 'genset/transf_report.html',data)
	else:
                return render(request,'genset/notfound.html')

def transf_alarm(request):
	if request.session.has_key('node_pin'):
		return render(request, 'genset/transf_alarm.html')
	else:
                return render(request,'genset/notfound.html')
				
def gasc_deshboard(request):
	if request.session.has_key('node_pin'):
		return render(request, 'genset/gasc_deshboard.html')
	else:
                return render(request,'genset/notfound.html')

def gasc_report(request):
	if request.session.has_key('node_pin'):
		data = dict(DataOperation().read_data_from_file())
		v1_range = range(1,220)
		v_range  = range(220,251)
		c_range  = range(0,201)
		l_range  = range(0,100000)
		if data['avg_voltage'] in v_range:
			data['vFlage'] = ['ok']
		elif data['avg_voltage'] in v1_range:
			data['vFlage'] = ['warning']
		elif data['avg_voltage'] == 0 :
			data['vFlage'] = ['ok']
		else:
			data['vFlage'] = ['error']
		if data['avg_current'] in c_range:
			data['cFlage'] = ['ok']
		else:
			data['cFlage'] = ['error']
		if data['avg_load'] in l_range:
			data['lFlage'] = ['ok']
		else:
			data['lFlage'] = ['error']
		if int(data['avg_voltage']) > 0:
			data['cstatus'] = ['running']
		else:
			data['cstatus'] = ['not_running']
		try:
			data['one_day_total_running_time'] = get_one_day_running_time()['total_running_time']
		except Exception as ex:
			logging.error("Error in addind total running time")
			logging.error(ex)
			data['one_day_total_running_time'] = '00:00:00'
		try:
			data['whole_day_running_time'] = get_one_day_running_time()['day_running_time']
		except Exception as ex:
			logging.error("Error in adding whole day running time")
			logging.error(ex)
			data['whole_day_running_time'] = [['NA','NA','NA']]
		return render(request, 'genset/gasc_report.html',data)
	else:
                return render(request,'genset/notfound.html')

def gasc_alarm(request):
	if request.session.has_key('node_pin'):
		return render(request, 'genset/gasc_alarm.html')
	else:
                return render(request,'genset/notfound.html')

def waterm_deshboard(request):
	if request.session.has_key('node_pin'):
		return render(request, 'genset/waterm_deshboard.html')
	else:
                return render(request,'genset/notfound.html')

def waterm_report(request):
	if request.session.has_key('node_pin'):
		data = dict(DataOperation().read_data_from_file())
		v1_range = range(1,220)
		v_range  = range(220,251)
		c_range  = range(0,201)
		l_range  = range(0,100000)
		if data['avg_voltage'] in v_range:
			data['vFlage'] = ['ok']
		elif data['avg_voltage'] in v1_range:
			data['vFlage'] = ['warning']
		elif data['avg_voltage'] == 0 :
			data['vFlage'] = ['ok']
		else:
			data['vFlage'] = ['error']
		if data['avg_current'] in c_range:
			data['cFlage'] = ['ok']
		else:
			data['cFlage'] = ['error']
		if data['avg_load'] in l_range:
			data['lFlage'] = ['ok']
		else:
			data['lFlage'] = ['error']
		if int(data['avg_voltage']) > 0:
			data['cstatus'] = ['running']
		else:
			data['cstatus'] = ['not_running']
		try:
			data['one_day_total_running_time'] = get_one_day_running_time()['total_running_time']
		except Exception as ex:
			logging.error("Error in addind total running time")
			logging.error(ex)
			data['one_day_total_running_time'] = '00:00:00'
		try:
			data['whole_day_running_time'] = get_one_day_running_time()['day_running_time']
		except Exception as ex:
			logging.error("Error in adding whole day running time")
			logging.error(ex)
			data['whole_day_running_time'] = [['NA','NA','NA']]
		return render(request, 'genset/waterm_report.html',data)
	else:
                return render(request,'genset/notfound.html')

def waterm_alarm(request):
	if request.session.has_key('node_pin'):
		return render(request, 'genset/waterm_alarm.html')
	else:
                return render(request,'genset/notfound.html')

def get_data(request):
	return HttpResponse(str(DataOperation().read_data_from_file()))

def get_log(request):
        filepath = '/var/log/iotdemo/digimove_new.log'
        return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

