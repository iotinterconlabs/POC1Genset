"""
WSGI config for iotdemo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""
"""
exposes the WSGI callable as a module-level variable named ``application``. 
For more information on this file, see 
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/ 
""" 
import os 
import time 
import traceback 
import signal 
import sys 
 
from django.core.wsgi import get_wsgi_application 
 
sys.path.append('/home/ubuntu/iotdemo') 
# adjust the Python version in the line below as needed 
sys.path.append('/usr/lib/python3/dist-packages') 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iotdemo.settings")

application = get_wsgi_application()
