from django.contrib import admin
from mavlink_serial_http_adaptor.models import Users,BBSPost
# Register your models here.
# Register your models here.

admin.site.register(Users)
admin.site.register(BBSPost)

admin.site.site_header = 'Mavlink_adaptor'
admin.site.site_title = 'Anglersking'
admin.site.index_title = 'welcom_addaptor'

