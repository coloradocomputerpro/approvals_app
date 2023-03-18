from django.db import models
from django.contrib.auth.models import User

class Program(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class MemberType(models.Model):
    type_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.type_name

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    member_type = models.ForeignKey(MemberType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'program')

class Approver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    programs = models.ManyToManyField(Program)

class Request(models.Model):
    REQUEST_STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
        ('I', 'More Information Requested'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=255)
    description = models.TextField()
    attachments = models.FileField(upload_to='attachments/', null=True, blank=True)
    status = models.CharField(max_length=1, choices=REQUEST_STATUS_CHOICES, default='P')
    approver = models.ForeignKey(Approver, on_delete=models.CASCADE, null=True, blank=True)
