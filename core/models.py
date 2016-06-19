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
    name = models.CharField(
        max_length=192,
        null=False,
        verbose_name=_("наименование"),
        blank=False
    )

    def __str__(self):
        return self.name

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


MARKETING_CAMPAIGN_STATUS = (
    ("Planning", _("Планируется")),
    ("Active", _("Активна")),
    ("Inactive", _("Не активна")),
    ("Complete", _("Завершена")),
    ("In Queue", _("В очереди")),
    ("Sending", _("Отсылается")),
)
MARKETING_CAMPAIGN_KIND = (
    ("Telesales", _("Продажи по телефону")),
    ("Mail", _("Почтовая рассылка")),
    ("Email", _("Рассылка E-mail")),
    ("Print", _("Печать")),
    ("Web", _("Веб-реклама")),
    ("Radio", _("Радио")),
    ("Television", _("Телевидение")),
    ("NewsLetter", _("Информ. бюллетень")),
)
CURRENCY = (
    ("rubles", _("рубли")),
)

class MarketingCampaign(Named, Responsible, Prototype):
    opening_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("дата начала")
    )
    closing_date = models.DateField(
        null=False,
        blank=False,
        verbose_name=_("дата окончания")
    )
    currency = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=CURRENCY,
        verbose_name=_("валюта")
    )
    budget = models.DecimalField(
        max_digits=32,
        decimal_places=8,
        null=True,
        blank=True,
        verbose_name=_("бюджет")
    )
    expected_amount = models.DecimalField(
        max_digits=32,
        decimal_places=8,
        null=True,
        blank=True,
        verbose_name=_("ожидаемая стоимость")
    )
    actual_amount = models.DecimalField(
        max_digits=32,
        decimal_places=8,
        null=True,
        blank=True,
        verbose_name=_("фактическая стоимость")
    )
    expected_revenue = models.DecimalField(
        max_digits=32,
        decimal_places=8,
        null=True,
        blank=True,
        verbose_name=_("ожидаемый доход")
    )
    target = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("цель")
    )
    status = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=MARKETING_CAMPAIGN_STATUS,
        verbose_name=_("статус")
    )
    kind = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=MARKETING_CAMPAIGN_KIND,
        verbose_name=_("тип")
    )
    number_of_impressions = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("количество показов")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("маркетинговая кампания")
        verbose_name_plural = _("маркетинговые кампании")


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
    marketing_campaign = models.ForeignKey(
        MarketingCampaign,
        null=True,
        blank=True,
        verbose_name=_("маркетинговая кампания")
    )
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

class WithSrc(models.Model):
    src = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        choices=SRC,
        verbose_name=_("источник")
    )
    src_desc = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("описание источника пред. контакта")
    )

    class Meta:
        abstract = True


class Contact(Desc, GeoDestination, EmailDestination, WithSrc, Responsible, Prototype):
    first_name = models.CharField(
        max_length=64,
        null=True,
        verbose_name=_("имя"),
        blank=True
    )
    last_name = models.CharField(
        max_length=64,
        null=False,
        verbose_name=_("фамилия"),
        blank=False
    )
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
    cite = models.URLField(
        verbose_name=_("сайт"),
        blank=True,
        null=True
    )
    skype = models.CharField(
        max_length=64,
        verbose_name=_("skype"),
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
    marketing_campaign = models.ForeignKey(
        MarketingCampaign,
        null=True,
        blank=True,
        verbose_name=_("маркетинговая кампания")
    )

    def get_fullname(self):
        return "{} {}".format(self.first_name or "", self.last_name).strip()

    def __str__(self):
        return self.get_fullname()

    class Meta:
        verbose_name = _("контакт")
        verbose_name_plural = _("контакты")


PRELIMINARY_CONTACT_STATUS = (
    ("New", _("Новый")),
    ("Assigned", _("Назначенный")),
    ("In Process", _("В процессе")),
    ("Converted", _("Преобразован")),
    ("Recycled", _("Повторный")),
    ("Dead", _("Мёртвый")),
)


class PreliminaryContact(Contact):
    status = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        choices=PRELIMINARY_CONTACT_STATUS,
        verbose_name=_("статус")
    )
    status_desc = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("описание статуса")
    )
    amount = models.DecimalField(
        max_digits=32,
        decimal_places=8,
        null=True,
        blank=True,
        verbose_name=_("сумма сделки")
    )
    transmitted_from = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_("передан от")
    )

    class Meta:
        verbose_name = _("предварительный контакт")
        verbose_name_plural = _("предварительные контакты")


STAGE = (
    ("Account is liquidated", _("Счёт оплачен")),
    ("Assembling", _("Сборка заказа / Счёт оплачен")),
    ("Assembling1", _("Сборка заказа / Счёт частично оплачен")),
    ("Assembling2", _("Сборка заказа / Счёт не оплачен")),
    ("Shipping0", _("Частичная готовность к отгрузке")),
    ("Shipping", _("Готовность к отгрузке")),
    ("Shipping1", _("Заказ отгружен / Счёт частично оплачен")),
    ("Shipping2", _("Заказ отгружен / Счёт не оплачен")),
    ("Prospecting", _("Разведка")),
    ("Qualification", _("Оценка")),
    ("Needs Analysis", _("Анализ потребностей")),
    ("Value Proposition", _("Предложение ценности")),
    ("Id. Decision Makers", _("Опред. лиц, принимающих решения")),
    ("Perception Analysis", _("Анализ реакции")),
    ("Proposal/Price Quote", _("Ком. предложение /Выставление счёта")),
    ("Negotiation/Review", _("Согласование / Пересмотр")),
    ("Closed Won", _("Закрыто с успехом / Товар отгружен")),
    ("Closed Lost", _("Закрыто с потерями / Товар возвращён")),
)
DEAL_KIND = (
    ("existing", _("существующий бизнес")),
    ("new", _("новый бизнес")),
)


class Deal(Named, WithSrc, Responsible, Prototype):
    currency = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=CURRENCY,
        verbose_name=_("валюта")
    )
    amount = models.DecimalField(
        max_digits=32,
        decimal_places=8,
        null=False,
        blank=False,
        verbose_name=_("сумма сделки")
    )
    stage = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        choices=STAGE,
        verbose_name=_("стадия продаж")
    )
    posibility = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("вероятность (%)")
    )
    next_step = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_("следующий шаг")
    )
    contractor = models.ForeignKey(
        Contractor,
        null=False,
        blank=False,
        verbose_name=_("контрагент")
    )
    closing_date = models.DateField(
        null=False,
        blank=False,
        verbose_name=_("ожидаемая дата закрытия")
    )
    kind = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=DEAL_KIND,
        verbose_name=_("тип")
    )
    marketing_campaign = models.ForeignKey(
        MarketingCampaign,
        null=True,
        blank=True,
        verbose_name=_("маркетинговая кампания")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("сделка")
        verbose_name_plural = _("сделки")


PRIORITY = (
    (0, _("Низкий")),
    (1, _("Средний")),
    (2, _("Высокий")),
)

CIRCULATION_STATUS = (
    ("Open_New", _("Новое")),
    ("Open_Assigned", _("Назначенное")),
    ("Closed_Closed", _("Закрытое")),
    ("Open_Pending Input", _("Ожидание решения")),
    ("Closed_Rejected", _("Отклонённое")),
    ("Closed_Duplicate", _("Продублированное")),
)

CIRCULATION_KIND = (
    ("Administration", _("Административное")),
    ("Product", _("Продукция")),
    ("User", _("Пользовательское")),
)

class Circulation(Named, Responsible, Prototype):
    priority = models.IntegerField(
        choices=PRIORITY,
        null=False,
        blank=False,
        verbose_name=_("приоритет")
    )
    status = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        choices=CIRCULATION_STATUS,
        verbose_name=_("статус")
    )
    contractor = models.ForeignKey(
        Contractor,
        null=False,
        blank=False,
        verbose_name=_("контрагент")
    )
    kind = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        choices=CIRCULATION_KIND,
        verbose_name=_("тип")
    )
    resolution = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("резолюция")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("обращение")
        verbose_name_plural = _("обращения")


class StartAndDuration(models.Model):
    starting_datetime = models.DateTimeField(
        null=False,
        blank=False,
        verbose_name=_("время начала")
    )
    finishing_datetime = models.DateTimeField(
        null=False,
        blank=False,
        verbose_name=_("время окончания")
    )

    class Meta:
        abstract = True


PHONE_CALL = (
    ("inbound", _("входящий")),
    ("outbound", _("исходящий")),
)

PHONE_STATUS = (
    ("planned", _("запланирован")),
    ("held", _("состоялся")),
    ("not held", _("не состоялся")),
)


class RelatedTo(models.Model):
    # TODO related to

    class Meta:
        abstract = True


class Relation(Named, RelatedTo, Responsible, Prototype):

    class Meta:
        abstract = True


class PhoneCall(Relation, StartAndDuration):
    kind = models.CharField(
        max_length=16,
        null=False,
        blank=False,
        choices=PHONE_CALL,
        verbose_name=_("тип")
    )
    status = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        choices=PHONE_STATUS,
        verbose_name=_("статус")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("звонок")
        verbose_name_plural = _("звонки")


MEETING_STATUS = PHONE_STATUS


class Meeting(Relation, StartAndDuration):
    status = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        choices=MEETING_STATUS,
        verbose_name=_("статус")
    )
    place = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_("место встречи")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("встреча")
        verbose_name_plural = _("встречи")


TASK_STATUS = (
    ("Not Started", _("Не начата")),
    ("In Progress", _("В процессе")),
    ("Completed", _("Завершена")),
    ("Pending Input", _("Ожидание решения")),
    ("Deferred", _("Отложена")),
)


class Task(Relation, StartAndDuration):
    priority = models.IntegerField(
        choices=PRIORITY,
        null=False,
        blank=False,
        verbose_name=_("приоритет")
    )
    status = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        choices=TASK_STATUS,
        verbose_name=_("статус")
    )
    contact = models.ForeignKey(
        Contact,
        null=True,
        blank=True,
        verbose_name=_("контактное лицо")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("задача")
        verbose_name_plural = _("задачи")


class Note(Relation):
    contact = models.ForeignKey(
        Contact,
        null=True,
        blank=True,
        verbose_name=_("контактное лицо")
    )
    attach = models.FileField(
        verbose_name=_("вложение"),
        upload_to="attachs/notes",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("заметка")
        verbose_name_plural = _("заметки")


DOCUMENT_TYPE = (
    ("mailmerge", _("Слияние")),
    ("eula", _("Пользовательское соглашение (EULA)")),
    ("nda", _("Соглашение о неразглашении (NDA)")),
    ("license", _("Лицензионное соглашение")),
)

DOCUMENT_STATUS = (
    ("Active", _("Активен")),
    ("Draft", _("Черновик")),
    ("FAQ", _("ЧаВо")),
    ("Expired", _("Просрочен")),
    ("Under Review", _("На рассмотрении")),
    ("Pending", _("Ожидание решения")),
)


class Document(Named, Responsible, Prototype):
    attach = models.FileField(
        verbose_name=_("вложение"),
        upload_to="attachs/documents",
        null=False,
        blank=False,
    )
    version = models.IntegerField(
        null=False,
        blank=False,
        verbose_name=_("версия"),
        default=1
    )
    kind = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=DOCUMENT_TYPE,
        verbose_name=_("тип документа")
    )
    status = models.CharField(
        max_length=16,
        null=False,
        blank=False,
        choices=DOCUMENT_STATUS,
        verbose_name=_("статус")
    )
    is_template = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name=_("шаблон")
    )
    related_documents = models.ManyToManyField(
        'self',
        blank=True,
        verbose_name=_("связанный документ")
    )
    publication_date = models.DateField(
        null=False,
        blank=False,
        verbose_name=_("дата публикации")
    )
    expire_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("актуален до")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("документ")
        verbose_name_plural = _("документы")


PROJECT_STATUS = (
    ("Draft", _("Черновик")),
    ("In Review", _("На рассмотрении")),
    ("Published", _("Опубликован")),
)


class Project(Named, Responsible, Prototype):
    starting_date = models.DateField(
        null=False,
        blank=False,
        verbose_name=_("дата начала")
    )
    finishing_date = models.DateField(
        null=False,
        blank=False,
        verbose_name=_("дата окончания")
    )
    priority = models.IntegerField(
        choices=PRIORITY,
        null=False,
        blank=False,
        verbose_name=_("приоритет")
    )
    status = models.CharField(
        max_length=16,
        null=False,
        blank=False,
        choices=PROJECT_STATUS,
        verbose_name=_("статус")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("проект")
        verbose_name_plural = _("проекты")


# TODO addresses lists and emails