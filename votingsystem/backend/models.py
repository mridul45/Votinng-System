from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import secrets
import random
from nacl.secret import SecretBox
from nacl.utils import random
from django.core.mail import send_mail
from django.conf import settings
from PIL import Image, ImageDraw
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from io import BytesIO
import os
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage



class Election(models.Model):

    host = models.ForeignKey(User,on_delete=models.CASCADE)
    elcetion_name = models.TextField(null=True,blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.elcetion_name


class Candidate(models.Model):
    
    acc_holder = models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    aadhar_num = models.BigIntegerField(default=0)
    candidate_id = models.BigIntegerField(default=0)
    party_affiliated = models.TextField(null=True,blank=True)
    election_name = models.ManyToManyField(Election)
    email = models.EmailField(max_length=500,null=True,blank=True)
    photo = models.TextField()

    def __str__(self):
        return self.acc_holder.username


class Voter(models.Model):
    
    acc_holder = models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    aadhar_number = models.CharField(max_length=500,null=True,blank=True)
    election_name = models.ManyToManyField(Election)
    email = models.EmailField(max_length=500,null=True,blank=True)
    age = models.IntegerField(default=18)

    def __str__(self):
        return self.acc_holder.username


class Voted(models.Model):

    voter_id = models.TextField(null=True,blank=True)
    candidate_id = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.voter_id


class Shares(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share1 = models.ImageField(upload_to='shares/')
    share2 = models.ImageField(upload_to='shares/')
    share2_sent = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)



class Results(models.Model):
    pass



def encrypt_email(email, iv):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=b'salt',
        length=32,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(email.encode())
    cipher = Cipher(algorithms.AES(key[:32]), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_email = encryptor.update(email.encode()) + encryptor.finalize()
    return encrypted_email


# Modify your save_share function to generate and pass an IV
@receiver(post_save, sender=Voted)
def save_share(sender, instance, **kwargs):
    user = User.objects.get(pk=1)  # Assuming Voted model has a ForeignKey to User
    iv = secrets.token_bytes(16)  # 16 bytes = 128 bits
    encrypted_email = encrypt_email(user.email, iv)
    share1, share2 = create_visual_shares(encrypted_email, iv)
    
    share_model_instance = Shares.objects.create(
        user=user,
        share2_sent=False
    )

    # Save share1 to the ImageField
    share1_content = BytesIO()
    share1.save(share1_content, format='PNG')
    share1_content.seek(0)
    share_model_instance.share1.save('file.png', ContentFile(share1_content.read()), save=False)

    # Save share2 to the ImageField
    share2_content = BytesIO()
    share2.save(share2_content, format='PNG')
    share2_content.seek(0)
    share_model_instance.share2.save('file.png', ContentFile(share2_content.read()), save=False)

    # Save the Shares model with updated ImageField fields
    share_model_instance.save()

    # Send email with share1 attached
    send_email_with_share(user.email, share1, iv)

# Modify your create_visual_shares function to accept and use an IV
def create_visual_shares(data, iv):
    share1 = Image.new('1', (256, 256))
    share2 = Image.new('1', (256, 256))
    draw1 = ImageDraw.Draw(share1)
    draw2 = ImageDraw.Draw(share2)
    binary_data = ''.join(format(byte, '08b') for byte in data)
    
    for i, bit in enumerate(binary_data):
        x, y = i % 256, i // 256
        if bit == '1':
            draw1.point((x, y), fill=1)
            draw2.point((x, y), fill=0)
        else:
            draw1.point((x, y), fill=0)
            draw2.point((x, y), fill=1)

    return share1, share2

# Update your send_email_with_share function to pass the IV
def send_email_with_share(email, share1, iv):
    share1_content = BytesIO()
    share1.save(share1_content, format='PNG')
    share1_content.seek(0)

    subject = "Your Vote Confirmation"
    message = "Please find your share1 attached."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    # Create an EmailMessage object
    email_message = EmailMessage(subject, message, from_email, recipient_list)
    
    # Attach the share1 content to the email
    email_message.attach('file.png', share1_content.read(), 'image/png')

    # Send the email
    email_message.send(fail_silently=False)