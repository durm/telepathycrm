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
    desc = models.TextField(verbose_name=_("Описание"))

class Named(Desc):
    name = models.TextField(null=False, verbose_name=_("Наименование"))

#####

class Address(Desc, Prototype):
    latitude = models.FloatField(verbose_name=_("Широта"))
    longitude = models.FloatField(verbose_name=_("Долгота"))

    # manuals
    street = models.TextField(verbose_name=_("Улица, дом/строение"))
    city = models.CharField(max_length=128, verbose_name=_("Город"))
    region = models.CharField(max_length=128, verbose_name=_("Область"))
    zipcode = models.IntegerField(verbose_name=_("Индекс"))
    country = models.CharField(max_length=128, verbose_name=_("Страна"))

class EmailToContractor(Prototype):
    email = models.EmailField(null=False, verbose_name=_("Email"))
    noreply = models.BooleanField(null=False, default=False, verbose_name=_("Не писать"))
    wrong = models.BooleanField(null=False, default=False, verbose_name=_("Неверный"))

class Contractor(Named, Prototype):
    cite = models.URLField(verbose_name=_("Сайт"))
    phone = models.CharField(max_length=128, verbose_name=_("Телефон"))
    fax = models.CharField(max_length=128, verbose_name=_("Факс"))
    emails = models.ManyToManyField(EmailToContractor, verbose_name=_("Emails"), related_name="+")
    email = models.ForeignKey(EmailToContractor, related_name="+")
