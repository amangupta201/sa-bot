from azure.cosmos import CosmosClient
import pandas as pd
import os

def initialize_cosmos_client():
    uri = settings['host']
    key = settings['master_key']
    return CosmosClient(uri, {'masterKey': key})

def access_database_container():
    client = initialize_cosmos_client()
    database_name = settings['database_id']
    container_name = settings['container_id']
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container

def insert_data(data):
    container = access_database_container()
    for idx, row in data.iterrows():
        item = {
            'id': str(idx),  # Use a unique identifier for each item
            'Title': row['Title'],
            'Price': row['Price'],
            'Original Price': row['Original Price'],
            'Fabric': row['Fabric'],
            'Work Type': row['Work Type'],
            'out-of-stock': row['out-of-stock']
        }
        container.upsert_item(item)

def query_data(query, parameters=None):
    container = access_database_container()
    return container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True)

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://sareechatbotdb.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'dkbbyzCaZ6J2tupnwIcMljx602WkI7d26qBBthBeMA6IjIiyFbKPNCD2ervvfxCjso3tTvSJc7WdACDbF7ibeg=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'ToDoList'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'Items'),
}
