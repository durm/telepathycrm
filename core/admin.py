from django.contrib import admin
from .models import Contractor, EmailToContractor, Address, Contact, PreliminaryContact, MarketingCampaign, Deal,\
    Circulation, PhoneCall, Meeting, Task, Note, Document, Project
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

PROTOFIELDS = ("created_by", "created_at", "updated_by", "updated_at")

PROTOTYPE_FIELDSET = (
    None,
    {
        "fields": (
            "created_by", "created_at", "updated_by", "updated_at"
        )
    }
)

RESPONSIBLE_FIELDSET = (
    None,
    {
        "fields": (
            "responsible",
        )
    }
)

class PrototypeAdmin(admin.ModelAdmin):
    readonly_fields = PROTOFIELDS

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'id', None) is None:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()


class ContractorAdmin(PrototypeAdmin):
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
        PROTOTYPE_FIELDSET
    )


class AddressAdmin(PrototypeAdmin):
    params = (
        "desc", "zipcode", "country", "region",
        "city", "street"
    )
    search_fields = params
    list_display = ("address_view", "country", "region", "city")
    list_filter = ("country", "region", "city")
    def address_view(self, obj):
        return obj

    fieldsets = (
        (
            None,
            {
                "fields": params
            }
        ),
        PROTOTYPE_FIELDSET
    )


class EmailToContractorAdmin(PrototypeAdmin):
    pass


class ContactAdmin(PrototypeAdmin):
    def contact_view(self, obj):
        return obj.get_fullname()
    params = ("department", "position", "phone_work", "phone_mobile", "skype")
    list_display = ("contact_view", ) + params
    search_fields = ("first_name", "last_name",) + params
    fieldsets = (
        (
            _("личные данные"),
            {
                "fields": (
                    "first_name", "last_name", "department", "position", "head",
                    "phone_work", "phone_mobile", "fax", "cite", "skype", "desc"
                )
            }
        ),
        (
            None,
            {
                "fields": (
                    "contractor", "marketing_campaign"
                )
            }
        ),
        (
            None,
            {
                "fields": (
                    "emails", "primary_email"
                )
            }
        ),
        (
            None,
            {
                "fields": (
                    "addresses", "primary_address"
                )
            }
        ),
        (
            None,
            {
                "fields": (
                    "src", "src_desc"
                )
            }
        ),
        RESPONSIBLE_FIELDSET,
        PROTOTYPE_FIELDSET
    )



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
    list_display = ("name", "place", "status", "starting_datetime", "finishing_datetime", )
    search_fields = ("name", "desc", "place")
    list_filter = ("status", "responsible")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name", "desc", "status", "place",
                    "starting_datetime", "finishing_datetime",
                )
            }
        ),
        RESPONSIBLE_FIELDSET,
        PROTOTYPE_FIELDSET
    )


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