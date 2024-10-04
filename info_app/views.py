from django.shortcuts import render
import json,os
from django.conf import settings

#view for encryption_info
def encryption_info(request):
    json_file_path = os.path.join(settings.BASE_DIR,'enc_dec.json')
    with open(json_file_path,'r') as json_file:
        content = json.load(json_file)
    return render(request,'info_app/encryption_info.html',{'content':content})

#view for encryption_techniques
def encryption_techniques(request):
    json_file_path = os.path.join(settings.BASE_DIR, 'types.json')
    with open(json_file_path,'r') as json_file:
        content = json.load(json_file)
    return render(request,'info_app/encryption_techniques.html',{'content':content})

