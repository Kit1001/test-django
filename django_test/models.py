from django.db import models


# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=100,
                            unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(
        'Menu',
        on_delete=models.CASCADE,
    )
    url = models.CharField(max_length=255)
    parent = models.ForeignKey("MenuItem", on_delete=models.SET_NULL, null=True, default=None, blank=True)

    def __str__(self):
        return self.url
