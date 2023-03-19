# https://cloud.google.com/pubsub/docs/schemas#proto_6
# %%
import os

from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1
from google.cloud.pubsub import SchemaServiceClient
from google.pubsub_v1.types import Schema

# %%
project_id = "podact-topic-extractor"
topic = "mp3-download-request"
schema_id = "mp3-download-request"
proto_file = "schemas\mp3_download_request.proto"
proto_file = os.path.join(os.getcwd(), proto_file)
project_path = f"projects/{project_id}"
# %%
with open(proto_file, "rb") as f:
    proto_source = f.read().decode("utf-8")
# %%
schema_client = SchemaServiceClient()
schema_path = schema_client.schema_path(project_id, schema_id)
schema = Schema(
    name=schema_path, type_=Schema.Type.PROTOCOL_BUFFER, definition=proto_source
)
# %%
try:
    result = schema_client.create_schema(
        request={"parent": project_path, "schema": schema, "schema_id": schema_id}
    )
    print(f"Created a schema using a protobuf schema file:\n{result}")
except AlreadyExists:
    print(f"{schema_id} already exists.")
# %%

# %%
publisher = pubsub_v1.PublisherClient()
# %%
# %%
topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=project_id,
    topic=topic,  # Set this to something appropriate.
)
# %%
publisher.create_topic(name=topic_name)
# %%
