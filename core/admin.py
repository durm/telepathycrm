from django.contrib import admin
from .models import Contractor, EmailToContractor
from django.forms import ModelForm

class ContractorAdmin(admin.ModelAdmin):
    pass

class EmailToContractorAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

admin.site.register(EmailToContractor, EmailToContractorAdmin)
admin.site.register(Contractor, ContractorAdmin)