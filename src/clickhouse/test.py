import clickhouse

orm = clickhouse.ClickHouseORM(database="Data")
table_name = "table1"
data = {
    "id": 1, 
    "title": "title1", 
    "content": "content1", 
    "link_img": "img1", 
    "url": "url1", 
    "published_at": 1681451485000,
    "sign": 1,
    
}
print(orm.insert(table_name, data))

