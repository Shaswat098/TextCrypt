from django.shortcuts import render
from .models import EncryptedMessage
import json
import os 
from django.conf import settings

#view for home page
def home(request):
    return render(request,'encryption_app/home.html')

# view for encryption
def encrypt_message(request):
    if request.method=='POST':
        message=request.POST['message']
        encyption_type=request.POST['encryption_type']
        encrypted_message=EncryptedMessage(message=message,encryption_type=encyption_type)
        encrypted_message.save()
        context={
            'encrypted_message':encrypted_message.encrypted_message,
            'key':encrypted_message.key,
            'encryption_type':encyption_type
        }
        return render(request,'encryption_app/result.html',context)
    return render(request,'encryption_app/encrypt.html')
    
# view for decryption
def decrypt_message(request):
    if request.method == 'POST':
        encrypted_message = request.POST['encrypted_message']  # Corrected variable name
        key = request.POST['key']
        encryption_type = request.POST['encryption_type']
        
        # Create an instance of EncryptedMessage
        encrypted_message_obj = EncryptedMessage(
            encrypted_message=encrypted_message,
            key=key,
            encryption_type=encryption_type
        )
        
        # Attempt to decrypt the message
        decrypted_message = encrypted_message_obj.decrypt()
        
        # Prepare context for rendering the result
        context = {
            'decrypted_message': decrypted_message
        }
        return render(request, 'encryption_app/result.html', context)
    
    return render(request, 'encryption_app/decrypt.html')

# view for about page
def about_view(request):
    json_file_path = os.path.join(settings.BASE_DIR,'about.json')
    with open(json_file_path,'r')as json_file:
        content = json.load(json_file)
    return render(request,'encryption_app/about.html',{'content':content})