from django.contrib import admin
from .models import  *
import csv
from django.http import HttpResponse



# Add more columns to be displayed in grid view under the admin panel
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


@admin.register(employees)
class employeesAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('registered','firstName','lastName','email','dept_id','supervisor_id','title_id','employeeID')
    actions = ["export_as_csv"]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id','name','phone','email','date_created')
    actions = ["export_as_csv"]



class Employee_titlesAdmin(admin.ModelAdmin):
    list_display = ('title_id','title_name')

# Register your models here.

admin.site.register(Department)
admin.site.register(NonConformitySource)
admin.site.register(NonConformityList)
admin.site.register(NonConformityAction)
admin.site.register(car)
admin.site.register(RootCause)
admin.site.register(CorrectivePreventiveAction)
admin.site.register(Carstatus)
admin.site.register(Company)
admin.site.register(CarPriority)
admin.site.register(Carsverification)
#admin.site.register(employees)
admin.site.register(Employee_titles,Employee_titlesAdmin)




