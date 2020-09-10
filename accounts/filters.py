import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class CarFilter(django_filters.FilterSet):
	#car_number = DateFilter(field_name="car_number", lookup_expr='gte')
	#status = DateFilter(field_name="status", lookup_expr='lte')
	#car_userid = CharFilter(field_name='car_userid', lookup_expr='icontains')


	class Meta:
		model = car
		fields=['car_number','status','nonconf','car_dept','implementedby']
		#fields = {
        #    'car_number': ['lt', 'gt'],
        #    'car_dateoccur': ['exact', 'year__gt'],
        #}
		
		
		#exclude = ['customer', 'date_created']