from django.db import models
from django.contrib.auth.models import User
# Create your models here.


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



class Results(models.Model):
    pass