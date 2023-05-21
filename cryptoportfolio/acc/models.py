from django.db import models


# Create your models here.


class Portfolio(models.Model):
    owner = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Cryptocoin(models.Model):
    name = models.CharField(max_length=7)
    idPortfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    amount = models.FloatField()
    avgBuyPrice = models.FloatField()

class Transaction(models.Model):
    name = models.CharField(max_length=7)
    price = models.FloatField()
    amount = models.FloatField()
    transType = models.IntegerField()  # 0-Покупка, 1-Продажа, нужно как-нибудь заменить

class Appeal(models.Model):
    email = models.CharField(max_length=300)
    text = models.CharField(max_length=3000)
    status = models.CharField(max_length=30)