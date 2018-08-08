from django.db import models

# Create your models here.
class Province(models.Model):
    provinceid=models.CharField(max_length=20)
    province=models.CharField(max_length=50)
    class Meta:
        db_table='provinces'

class Cities(models.Model):
    cityid=models.CharField(max_length=20)
    city=models.CharField(max_length=50)
    provinceid=models.CharField(max_length=20)
    class Meta:
        db_table='cities'
class Areas(models.Model):
    areaid=models.CharField(max_length=20)
    area=models.CharField(max_length=50)
    cityid=models.CharField(max_length=20)
    class Meta:
        db_table='areas'







