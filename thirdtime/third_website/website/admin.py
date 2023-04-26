from django.contrib import admin
import models
from clickhouse_models import ClickHouseUser

# Register your models here.
admin.site.register(ClickHouseUser)