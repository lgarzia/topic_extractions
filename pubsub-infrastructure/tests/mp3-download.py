# Publish
# https://cloud.google.com/pubsub/docs/publish-receive-messages-client-library
# %%
import sys

sys.path.append(r"C:\Users\lgarzia\Documents\GitHub\topic_extractions\pubsub-infrastructure\schemas")
import mp3_download_request_pb2

# %%
m = mp3_download_request_pb2.MP3DownloadRequest()
# %%
# View SCHEMA DETAILS:
# https://cloud.google.com/pubsub/docs/schemas#view-schema
from google.api_core.exceptions import NotFound
from google.cloud.pubsub import SchemaServiceClient

# TODO(developer): Replace these variables before running the sample.
project_id = "podact-topic-extractor"
schema_id = "mp3-download-request"
schema_revision_id = "2488c5fc"

schema_client = SchemaServiceClient()
schema_path = schema_client.schema_path(
    project_id, schema_id + "@" + schema_revision_id
)

try:
    result = schema_client.get_schema(request={"name": schema_path})
    print(f"Got a schema revision:\n{result}")
except NotFound:
    print(f"{schema_id} not found.")
# %%
# LIST SCHEMAS
project_path = f"projects/{project_id}"
schema_client = SchemaServiceClient()
for schema in schema_client.list_schemas(request={"parent": project_path}):
    print(schema)
print("Listed schemas.")
# %%
# schema revisions
for schema in schema_client.list_schema_revisions(request={"name": schema_path}):
    print(schema)
print("Listed schema revisions.")
# %%
# publish with a message
import sys

import mp3_download_request_pb2

sys.path.append(r"C:\Users\lgarzia\Documents\GitHub\topic_extractions\pubsub-infrastructure\schemas")
import mp3_download_request_pb2
from google.api_core.exceptions import NotFound
from google.cloud.pubsub import PublisherClient
from google.protobuf.json_format import MessageToJson, Parse
from google.pubsub_v1.types import Encoding

# https://cloud.google.com/pubsub/docs/publisher#using-schema
# TODO(developer): Replace these variables before running the sample.
project_id = "podact-topic-extractor"
topic_id = "mp3-download-request"

publisher_client = PublisherClient()
topic_path = publisher_client.topic_path(project_id, topic_id)

try:
    # Get the topic encoding type.
    topic = publisher_client.get_topic(request={"topic": topic_path})
    encoding = topic.schema_settings.encoding
    print(f"encoding is - {encoding}")
    # Instantiate a protoc-generated class defined in `us-states.proto`.
    mp3 = mp3_download_request_pb2.MP3DownloadRequest()
    mp3.collection_id = '4656556'  
    mp3.episode_id = '47557'
    mp3.episode_url = 'http2-I-will-download.ulr'

    # Encode the data according to the message serialization type.
    if encoding == Encoding.BINARY:
        data = mp3.SerializeToString()
        print(f"Preparing a binary-encoded message:\n{data}")
    elif encoding == Encoding.JSON:
        json_object = MessageToJson(mp3)
        print(f"json object-{str(json_object)}")
        data = str(json_object).encode("utf-8")
        print(data)
        print(f"Preparing a JSON-encoded message:\n{data}")
    else:
        print(f"No encoding specified in {topic_path}. Abort.")
        exit(0)

    future = publisher_client.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")

except NotFound:
    print(f"{topic_id} not found.")
# %%
s = 'ewogICAgJ2NvbGxlY3Rpb25faWQnOiAgJzEnLCAgCiAgICAnZXBpc29kZV9pZCc6ICcyJywKICAgICdlcGlzb2RlX3VybCc6ICczLCcKfQ=='
# %%
import base64

data = base64.b64decode(s).decode("utf-8").strip()
print(data)
import json

bdict = Parse(json.dumps(data), mp3_download_request_pb2.MP3DownloadRequest())
# %%
