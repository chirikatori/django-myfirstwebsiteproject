from clickhouse import clickhouse
from settings import *

data = 10
with clickhouse.ClickHouseORMContext(database=DATABASE) as orm:
    result = orm.insert(TABLE_NAME, data)
    if result:
        print("Sava data success")
    print("Failed to save data")