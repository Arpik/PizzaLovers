from django.db import models

# Specify the size of a pizza

class Size(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

# Specify Pizza class

class Pizza(models.Model):
    topping1 = models.CharField(max_length=100)
    topping2 = models.CharField(max_length=100)
    size = models.ForeignKey(Size, on_delete = models.CASCADE)
