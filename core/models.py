from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _


class Prototype(models.Model):
    created_by = models.ForeignKey(
        User,
        null=False,
        verbose_name=_("создал"),
        related_name="+"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        verbose_name=_("время создания"))
    updated_by = models.ForeignKey(
        User,
        null=False,
        verbose_name=_("изменил"),
        related_name="+"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=False,
        verbose_name=_("время изменения")
    )

    class Meta:
        abstract = True


class Desc(models.Model):
    desc = models.TextField(
        verbose_name=_("описание"),
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class Responsible(models.Model):
    responsible = models.ForeignKey(
        User,
        blank=True,
        null=True,
        verbose_name=_("ответственный")
    )

    class Meta:
        abstract = True


class Named(Desc):
    name = models.TextField(
        null=False,
        verbose_name=_("наименование"),
        blank=False
    )

    class Meta:
        abstract = True


class Address(Desc, Prototype):
    street = models.TextField(
        verbose_name=_("улица, дом/строение"),
        blank=True,
        null=True
    )
    city = models.CharField(
        max_length=128,
        verbose_name=_("город"),
        blank=False,
        null=False,
    )
    region = models.CharField(
        max_length=128,
        verbose_name=_("область"),
        blank=True,
        null=True
    )
    zipcode = models.IntegerField(
        verbose_name=_("индекс"),
        blank=True,
        null=True
    )
    country = models.CharField(
        max_length=128,
        verbose_name=_("страна"),
        blank=True,
        null=True
    )

    def __str__(self):
        return ", ".join(
            map(
                str,
                filter(
                    None,
                    (
                    self.zipcode,
                    self.country,
                    self.region,
                    self.city,
                    self.street,
                    )
                )
            )
        ).strip()

    class Meta:
        verbose_name = _("адрес")
        verbose_name_plural = _("адреса")


class GeoDestination(models.Model):
    addresses = models.ManyToManyField(
        Address,
        verbose_name=_("адреса"),
        related_name="+"
    )
    primary_address = models.ForeignKey(
        Address,
        verbose_name=_("адрес"),
        related_name="+",
        blank=True,
        null=True,
        help_text=_("перед тем как задать главный адрес добавьте его и перезагрузите страницу.")
    )

    class Meta:
        abstract = True


class EmailToContractor(Prototype):
    email = models.EmailField(
        null=False,
        verbose_name=_("эл. адрес"),
        blank=False
    )
    noreply = models.BooleanField(
        null=False,
        default=False,
        verbose_name=_("не писать")
    )
    wrong = models.BooleanField(
        null=False,
        default=False,
        verbose_name=_("неверный")
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("эл. адрес")
        verbose_name_plural = _("эл. адреса")


class EmailDestination(models.Model):
    emails = models.ManyToManyField(
        EmailToContractor,
        verbose_name=_("эл. адреса"),
        related_name="+"
    )
    primary_email = models.ForeignKey(
        EmailToContractor,
        verbose_name=_("эл. адрес"),
        related_name="+",
        blank=True,
        null=True,
        help_text=_("перед тем как задать главный email добавьте его и перезагрузите страницу.")
    )

    class Meta:
        abstract = True


class Contractor(Named, GeoDestination, EmailDestination, Responsible, Prototype):
    cite = models.URLField(
        verbose_name=_("сайт"),
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=128,
        verbose_name=_("телефон"),
        null=False,
        blank=False
    )
    fax = models.CharField(
        max_length=128,
        verbose_name=_("факс"),
        blank=True,
        null=True
    )
    kind = models.CharField(
        max_length=24,
        null=True,
        blank=True,
        verbose_name=_("тип контрагента")
    )
    sector = models.CharField(
        max_length=24,
        null=True,
        blank=True,
        verbose_name=_("отрасль")
    )
    annual_income = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_("годовой доход")
    )
    annual_income_currency = models.CharField(
        max_length=8,
        blank=True,
        null=True,
        verbose_name=_("валюта")
    )
    employee_num = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("число сотрудников")
    )
    sic = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_("ОКВЭД/SIC")
    )
    stock_code = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_("биржевой код")
    )
    own = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_("собственность")
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        verbose_name=_("состоит в")
    )
    # TODO marketing company
    rating = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_("рейтинг")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("контрагент")
        verbose_name_plural = _("контрагенты")


SRC = (
    ('phone', _("холодный прозвон")),
    ('existing_client', _("существующий клиент")),
    ('own', _("собственный")),
    ('employee', _("сотрудник")),
    ('pr', _("pr-деятельность")),
    ('direct_link', _("прямая ссылка")),
    ('conference', _("конференция")),
    ('special_galery', _("спец. выставка")),
    ('web', _("сайт")),
    ('talk', _("разговор")),
    ('email', _("Email")),
    ('marketing', _("маркетинговая кампания")),
)


class Contact(Named, GeoDestination, EmailDestination, Responsible, Prototype):
    position = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_("должность")
    )
    department = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_("отдел")
    )
    phone_work = models.CharField(
        max_length=128,
        verbose_name=_("телефон (раб.)"),
        null=True,
        blank=True
    )
    phone_mobile = models.CharField(
        max_length=128,
        verbose_name=_("телефон (моб.)"),
        null=True,
        blank=True
    )
    fax = models.CharField(
        max_length=128,
        verbose_name=_("факс"),
        blank=True,
        null=True
    )
    contractor = models.ForeignKey(
        Contractor,
        null=True,
        blank=True,
        verbose_name=_("контрагент")
    )
    head = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        verbose_name=_("руководитель")
    )
    src = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        choices=SRC,
        verbose_name=_("источник")
    )
    # TODO marketing company

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("контакт")
        verbose_name_plural = _("контакты")