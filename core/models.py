from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# timestamps
class Prototype(models.Model):
    created_by = models.ForeignKey(
        User,
        null=False,
        verbose_name=_("Создал"),
        related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False, verbose_name=_("Время создания"))
    updated_by = models.ForeignKey(
        User,
        null=False,
        verbose_name=_("Изменил"),
        related_name="+"
    )
    updated_at = models.DateTimeField(auto_now=True, null=False, verbose_name=_("Время изменения"))

    class Meta:
        abstract = True

class Desc(models.Model):
    desc = models.TextField(verbose_name=_("Описание"), blank=True)

class Named(Desc):
    name = models.TextField(null=False, verbose_name=_("Наименование"))

#####

class Address(Desc, Prototype):
    latitude = models.FloatField(verbose_name=_("Широта"), blank=True)
    longitude = models.FloatField(verbose_name=_("Долгота"), blank=True)

    # manuals
    street = models.TextField(verbose_name=_("Улица, дом/строение"), blank=True)
    city = models.CharField(max_length=128, verbose_name=_("Город"), blank=True)
    region = models.CharField(max_length=128, verbose_name=_("Область"), blank=True)
    zipcode = models.IntegerField(verbose_name=_("Индекс"), blank=True)
    country = models.CharField(max_length=128, verbose_name=_("Страна"), blank=True)

    def __str__(self):
        return "{} {} {} {} {}".format(
            self.zipcode or "",
            self.country or "",
            self.region or "",
            self.city or "",
            self.street
        ).strip()

class EmailToContractor(Prototype):
    email = models.EmailField(null=False, verbose_name=_("Email"))
    noreply = models.BooleanField(null=False, default=False, verbose_name=_("Не писать"))
    wrong = models.BooleanField(null=False, default=False, verbose_name=_("Неверный"))

    def __str__(self):
        return self.email

class Contractor(Named, Prototype):
    cite = models.URLField(verbose_name=_("Сайт"), blank=True)
    phone = models.CharField(max_length=128, verbose_name=_("Телефон"))
    fax = models.CharField(max_length=128, verbose_name=_("Факс"), blank=True)
    emails = models.ManyToManyField(EmailToContractor, verbose_name=_("Emails"), related_name="+", blank=True)
    email = models.ForeignKey(EmailToContractor, related_name="+")
 
    def __str__(self):
        return self.name