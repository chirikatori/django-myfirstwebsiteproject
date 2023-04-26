from django.contrib import admin
from .clickhouse_model import ClickHouseUser
from .models import ClickHouseSyncModel

# Register your models here.

admin.site.register(ClickHouseUser)
#admin.site.register(ClickHouseSyncModel)
