from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    depatment_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    hired_at = models.DateField(max_length=100,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.full_name