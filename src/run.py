from parser import parser as ps 
from kafkaReader import kafkaConsumer as Reader

from extract_data import extract_data_from_html as edfh 
from clickhouse import clickhouse
from clickhouse_sqlalchemy import types, engines
from extract_data import extract_data_from_html as edfh
from settings import *
#
# crawl without Temporal 
# 

reader = Reader.KafkaConsumer(TOPIC_KAFKA, GROUP_ID_COUNSUMER)


def count_words(s: str) -> int:
    s = s.split(" ")
    return len(s)

def get_msg() -> dict:
    msg = reader.read_next_message()
    if msg is None:
        return None
    text, text_with_xpath, link_img = edfh.extract(msg['content']) 
    if count_words(text) < 100:
        msg['content'] = ps.get_content(msg['url'])
        if msg['content'] == None:
            return None
        text, text_with_xpath, link_img = edfh.extract(msg['content'])
    msg['content'] = text
    msg['link_img'] = link_img
    msg['sign'] = 1
    return msg

def push_msg(data: dict) -> bool:
    orm = clickhouse.ClickHouseORM(database=DATABASE)
    return orm.insert(TABLE_NAME, data)
    
if __name__ == "__main__":
    count = 0
    while True:
        try:
            msg = get_msg()
            # print(msg)   
            if msg is not None:
                if push_msg(msg):
                    print(f"push success {msg['id']}")
                    count += 1
            else:
                print("None")
        except KeyboardInterrupt:
            break
    print("\n" + str(count) + " message")
            