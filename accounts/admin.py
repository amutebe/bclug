from django.contrib import admin
from .models import  *
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
admin.site.register(employees)

