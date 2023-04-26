from django_clickhouse.clickhouse_models import ClickHouseModel
from django_clickhouse.engines import MergeTree
from infi.clickhouse_orm import fields
from .models import User

class ClickHouseUser(ClickHouseModel):
    django_model = User
    
    # Uncomment the line below if you want your models to be synced automatically
    sync_enabled = True
    
    id = fields.UInt32Field()
    first_name = fields.StringField()
    birthday = fields.DateField()
    visits = fields.UInt32Field(default=0)

    engine = MergeTree('birthday', ('birthday',))

    def __str__(self):
        return self.first_name