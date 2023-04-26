from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table, ForeignKey, DDL
from clickhouse_sqlalchemy import types, engines, make_session, get_declarative_base
from datetime import date, timedelta

class ClickHouseORM:
    def __init__(self, host = "localhost", username = "user1", password = "123456", database = "default"):
        self.engine = create_engine(f'clickhouse://{username}:{password}@{host}:8123/default')
        self.engine.execute(DDL(f'CREATE DATABASE IF NOT EXISTS {database}'))
        self.engine = create_engine(f'clickhouse://{username}:{password}@{host}:8123/{database}')
        self.metadata = MetaData(bind=self.engine)
        self.Base = get_declarative_base(metadata=self.metadata)
        self.session = make_session(self.engine)

        class Table1(self.Base):
            __tablename__ = "table1"
            id = Column(types.Int32, primary_key=True)
            title = Column(types.String)
            content = Column(types.String)
            link_img = Column(types.String)
            url = Column(types.String)
            published_at = Column(types.DateTime64)
            sign = Column(types.Int8, nullable=-1)
            __table_args__ = (
                engines.CollapsingMergeTree(
                    sign_col=sign,
                    partition_by=id,
                    order_by=(id)
                ),
            )

        self.Table1 = Table1
        if not self.Table1.__table__.exists():
            self.Table1.__table__.create()
    
    def drop_table(self, table_name: str) -> bool:
        if table_name == "table1":
            table = self.Table1
        else:
            return False
        try:
            table.__table__.drop()
            # print("Drop success")
            return True
        except Exception as e:
            print(f"Failed to drop {table_name}: {str(e)}")
            return False
        
    
    def insert(self, table_name: str, data: dict) -> bool:
        if table_name == "table1":
            table = self.Table1
        else:
            return False
        try:
            self.session.execute(table.__table__.insert(), data)
            # print('Push data success')
            return True
        except Exception as e:
            print(f"Failed to push data: {str(e)}")
            return False

    def drop_database(self, database_name: str) -> bool:
        try:
            self.engine.execute(DDL(f"DROP DATABASE IF EXISTS {database_name}"));
            return True
        except Exception as e:
            print(f"Failed to drop database {database_name}: {str(e)}")
            return False

    def __del__(self):
        self.session.close()

class ClickHouseORMContext:
    def __init__(self, host = "localhost", username = "user1", password = "123456", database = "default"):
        self.orm = ClickHouseORM(host, username, password, database)
    
    def __enter__(self):
        return self.orm
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.orm.session.close()
        del self.orm