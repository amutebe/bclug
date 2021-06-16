from django.contrib import admin
from .models import *
import csv
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin



# Add more columns to be displayed in grid view under the admin panel and CSV data export



class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(mod9001_trainingplanner)
class mod9001_trainingplannerAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('plan_number','trainng_date','type')
    #list_filter = ("is_immortal", "category", "origin", IsVeryBenevolentFilter)
    actions = ["export_as_csv"]

@admin.register(mod9001_supplieregistration)
class mod9001_supplieregistrationAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('supplier_number','name','date_posted','manager','contact','phone','email','address')
    #list_filter = ("is_immortal", "category", "origin", IsVeryBenevolentFilter)
    actions = ["export_as_csv"]

@admin.register(process)
class processAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('description','dept','owner')
    #list_filter = ("is_immortal", "category", "origin", IsVeryBenevolentFilter)
    actions = ["export_as_csv"]








# Register your models here.

admin.site.register(document_standard)
admin.site.register(document_type)
admin.site.register(document_format)
admin.site.register(document_location)
admin.site.register(mod9001_document_manager)
admin.site.register(maintenance)
admin.site.register(schedule)
admin.site.register(equipment)
admin.site.register(mod9001_qmsplanner)
admin.site.register(status)
admin.site.register(prod_description)
admin.site.register(qmsstatus)

admin.site.register(noteffective)


admin.site.register(train_status)
admin.site.register(train_objective)
admin.site.register(train_desc)

admin.site.register(incident_description)
admin.site.register(incident_type)
admin.site.register(mod9001_incidentregister)
admin.site.register(mod9001_incidentregisterStaff)
admin.site.register(mod9001_processtable)
#admin.site.register(process) 
admin.site.register(mod9001_customeregistration)
admin.site.register(classification)
admin.site.register(rootcause)
admin.site.register(costs)
admin.site.register(providerparameters)
admin.site.register(mod9001_providerassessment)
#admin.site.register(mod9001_supplieregistration)
admin.site.register(providers)
admin.site.register(mod9001_correctiveaction)
admin.site.register(mod9001_planning)
#admin.site.register(mod9001_trainingplanner,mod9001_trainingplannerAdmin)
admin.site.register(mod9001_trainingregister)
admin.site.register(mod9001_customerSatisfaction)
admin.site.register(mod9001_customerComplaint)
admin.site.register(mod9001_changeRegister)





