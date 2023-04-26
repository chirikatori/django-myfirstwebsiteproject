from kafkaReader import kafkaConsumer as Reader
from extract_data import extract_data_from_html as edfh 
from parser import parser as ps 
from clickhouse import clickhouse
from settings import *

import asyncio
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

# count the number of words of a content
def count_words(s):
    s = s.split(" ")
    return len(s)

# read a message from kafka that stores the information of an article
@activity.defn
async def read_data():
    with Reader.KafkaConsumer(TOPIC_KAFKA, GROUP_ID_COUNSUMER) as reader:
        msg = reader.read_next_message()
        # del reader
        return msg

# parsing of an article
@activity.defn
async def parse_data(data):
    if data is None:
        return None
    text, text_with_xpath, link_img = edfh.extract(data['content']) 
    if count_words(text) < 100:
        data['content'] = ps.get_content(data['url'])
        if data['content'] == None:
            return None
        text, text_with_xpath, link_img = edfh.extract(data['content'])
    data['content'] = text
    data['link_img'] = link_img
    data['sign'] = 1
    return data

# save data to db clickhouse
@activity.defn
async def save_data(data):
    with clickhouse.ClickHouseORMContext(database=DATABASE) as orm:
        result = orm.insert(TABLE_NAME, data)
        if result:
            return(f"Sava data success {data['id']}")
        return(f"Failed to save data {data['id']}")

# workflow to define activity read_data
@workflow.defn 
class ReadWorkflow:
    @workflow.run
    async def run(self):
        return await workflow.execute_activity(
            read_data,
            start_to_close_timeout=timedelta(seconds=5),
        )

# workflow to define activity parse_data
@workflow.defn
class ParseWorkflow:
    @workflow.run
    async def run(self, data):
        return await workflow.execute_activity(
            parse_data,
            data,
            start_to_close_timeout=timedelta(seconds=5),
        )

# workflow to define activity save_data
@workflow.defn
class SaveWorkflow:
    @workflow.run   
    async def run(self, data):
        return await workflow.execute_activity(
            save_data,
            data,
            start_to_close_timeout=timedelta(seconds=5),
        )


async def main():
    client = await Client.connect("localhost:7233")

    async with Worker(
        client=client,
        task_queue="task-queue",
        workflows=[ReadWorkflow, ParseWorkflow, SaveWorkflow],
        activities=[read_data, parse_data, save_data],
    ):
        while True:
            try:
                result = await client.execute_workflow(
                ReadWorkflow.run,
                id="read-id",
                task_queue="task-queue",
                )
            
                result = await client.execute_workflow(
                    ParseWorkflow.run,
                    result,
                    id="parse-id",
                    task_queue="task-queue",
                )

                result = await client.execute_workflow(
                    SaveWorkflow.run,
                    result,
                    id="save-id",
                    task_queue="task-queue",
                )
                print(result)
            except Exception as e:
                print(f"An Error: {str(e)}")
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    asyncio.run(main())