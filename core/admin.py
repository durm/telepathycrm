from django.contrib import admin
from .models import Contractor, EmailToContractor, Address, Contact, PreliminaryContact, MarketingCampaign, Deal,\
    Circulation, PhoneCall, Meeting, Task, Note, Document, Project
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

class ContractorForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Contractor

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        """
        self.fields['primary_email'].queryset = \
            Contractor.objects.get(id=self.instance.id).emails.all() or \
            EmailToContractor.objects.none()
        self.fields['primary_address'].queryset = \
            Contractor.objects.get(id=self.instance.id).addresses.all() or \
            Address.objects.none()
        """


class PrototypeAdmin(admin.ModelAdmin):
    readonly_fields = ("created_by", "created_at", "updated_by", "updated_at")

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'id', None) is None:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()


class ContractorAdmin(PrototypeAdmin):
    form = ContractorForm
    readonly_fields = ("created_by", "created_at", "updated_by", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name", "desc", "phone", "fax", "cite", "emails",
                    "primary_email", "addresses", "primary_address",
                )
            }
        ),
        (
            _("дополнительно"),
            {
                "fields": (
                    "kind", "sector", "annual_income", "annual_income_currency",
                    "employee_num", "sic", "stock_code", "own", "parent", "rating", "responsible"
                )
            }
        ),
        (
            None,
            {
                "fields": (
                    "created_by", "created_at", "updated_by", "updated_at"
                )
            }
        )
    )



    filter_horizontal = ('emails', "addresses",)


class AddressAdmin(PrototypeAdmin):
    readonly_fields = ("created_by", "created_at", "updated_by", "updated_at")
    fields = (
        "desc", "zipcode", "country", "region", "city", "street",
        "created_by", "created_at", "updated_by", "updated_at")


class EmailToContractorAdmin(PrototypeAdmin):
    #def get_model_perms(self, request):
    #    """
    #    Return empty perms dict thus hiding the model from admin index.
    #    """
    #    return {}
    pass


class ContactAdmin(PrototypeAdmin):
    pass


class PreliminaryContactAdmin(PrototypeAdmin):
    pass


class MarketingCampaignAdmin(PrototypeAdmin):
    pass


class DealAdmin(PrototypeAdmin):
    pass


class CirculationAdmin(PrototypeAdmin):
    pass


class PhoneCallAdmin(PrototypeAdmin):
    pass


class MeetingAdmin(PrototypeAdmin):
    pass


class TaskAdmin(PrototypeAdmin):
    pass


class NoteAdmin(PrototypeAdmin):
    pass


class DocumentAdmin(PrototypeAdmin):
    pass


class ProjectAdmin(PrototypeAdmin):
    pass


admin.site.register(Address, AddressAdmin)
admin.site.register(EmailToContractor, EmailToContractorAdmin)
admin.site.register(Contractor, ContractorAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(PreliminaryContact, PreliminaryContactAdmin)
admin.site.register(MarketingCampaign, MarketingCampaignAdmin)
admin.site.register(Deal, DealAdmin)
admin.site.register(Circulation, CirculationAdmin)
admin.site.register(PhoneCall, PhoneCallAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Project, ProjectAdmin)