# https://cloud.google.com/pubsub/docs/create-topic#create_a_topic
# https://cloud.google.com/python/docs/reference/pubsub/latest


# %%
from google.cloud import pubsub_v1

# TODO(developer)
project_id = "podact-topic-extractor"
topic_id = "your-topic-id"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

topic = publisher.create_topic(request={"name": topic_path})

print(f"Created topic: {topic.name}")
# %%
# When you delete a topic, its subscriptions are not deleted. 
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

publisher.delete_topic(request={"topic": topic_path})

print(f"Topic deleted: {topic_path}")
# %%
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
project_path = f"projects/{project_id}"

for topic in publisher.list_topics(request={"project": project_path}):
    print(topic)
# %%
"""Publishes multiple messages to a Pub/Sub topic with an error handler."""
from concurrent import futures
from typing import Callable

from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)
publish_futures = []

def get_callback(
    publish_future: pubsub_v1.publisher.futures.Future, data: str
) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        try:
            # Wait 60 seconds for the publish call to succeed.
            print(publish_future.result(timeout=60))
        except futures.TimeoutError:
            print(f"Publishing {data} timed out.")

    return callback

for i in range(10):
    data = str(i)
    # When you publish a message, the client returns a future.
    publish_future = publisher.publish(topic_path, data.encode("utf-8"))
    # Non-blocking. Publish failures are handled in the callback function.
    publish_future.add_done_callback(get_callback(publish_future, data))
    publish_futures.append(publish_future)

# Wait for all the publish futures to resolve before exiting.
futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

print(f"Published messages with error handler to {topic_path}.")
# %%
from google.cloud import pubsub_v1

# TODO(developer)
# project_id = "your-project-id"
# topic_id = "your-topic-id"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

for n in range(1, 10):
    data_str = f"Message number {n}"
    # Data must be a bytestring
    data = data_str.encode("utf-8")
    # Add two attributes, origin and username, to the message
    future = publisher.publish(
        topic_path, data, origin="python-sample", username="gcp"
    )
    print(future.result())

print(f"Published messages with custom attributes to {topic_path}.")
# %%
from google.cloud import pubsub_v1

# TODO(developer): Choose an existing topic.
# project_id = "your-project-id"
# topic_id = "your-topic-id"

publisher_options = pubsub_v1.types.PublisherOptions(enable_message_ordering=True)
# Sending messages to the same region ensures they are received in order
# even when multiple publishers are used.
client_options = {"api_endpoint": "us-east1-pubsub.googleapis.com:443"}
publisher = pubsub_v1.PublisherClient(
    publisher_options=publisher_options, client_options=client_options
)
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)

for message in [
    ("message1", "key1"),
    ("message2", "key2"),
    ("message3", "key1"),
    ("message4", "key2"),
]:
    # Data must be a bytestring
    data = message[0].encode("utf-8")
    ordering_key = message[1]
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data=data, ordering_key=ordering_key)
    print(future.result())

print(f"Published messages with ordering keys to {topic_path}.")
# %%
from concurrent import futures

from google.cloud import pubsub_v1

# TODO(developer)
# project_id = "your-project-id"
# topic_id = "your-topic-id"

# Configure the batch to publish as soon as there are 10 messages
# or 1 KiB of data, or 1 second has passed.
batch_settings = pubsub_v1.types.BatchSettings(
    max_messages=10,  # default 100
    max_bytes=1024,  # default 1 MB
    max_latency=1,  # default 10 ms
)
publisher = pubsub_v1.PublisherClient(batch_settings)
topic_path = publisher.topic_path(project_id, topic_id)
publish_futures = []

# Resolve the publish future in a separate thread.
def callback(future: pubsub_v1.publisher.futures.Future) -> None:
    message_id = future.result()
    print(message_id)

for n in range(1, 10):
    data_str = f"Message number {n}"
    # Data must be a bytestring
    data = data_str.encode("utf-8")
    publish_future = publisher.publish(topic_path, data)
    # Non-blocking. Allow the publisher client to batch multiple messages.
    publish_future.add_done_callback(callback)
    publish_futures.append(publish_future)

futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

print(f"Published messages with batch settings to {topic_path}.")
# %%
from google import api_core
from google.cloud import pubsub_v1

# %%
# TODO(developer)
# project_id = "your-project-id"
# topic_id = "your-topic-id"

# Configure the retry settings. Defaults shown in comments are values applied
# by the library by default, instead of default values in the Retry object.
custom_retry = api_core.retry.Retry(
    initial=0.250,  # seconds (default: 0.1)
    maximum=90.0,  # seconds (default: 60.0)
    multiplier=1.45,  # default: 1.3
    deadline=300.0,  # seconds (default: 60.0)
    predicate=api_core.retry.if_exception_type(
        api_core.exceptions.Aborted,
        api_core.exceptions.DeadlineExceeded,
        api_core.exceptions.InternalServerError,
        api_core.exceptions.ResourceExhausted,
        api_core.exceptions.ServiceUnavailable,
        api_core.exceptions.Unknown,
        api_core.exceptions.Cancelled,
    ),
)

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

for n in range(1, 10):
    data_str = f"Message number {n}"
    # Data must be a bytestring
    data = data_str.encode("utf-8")
    future = publisher.publish(topic=topic_path, data=data, retry=custom_retry)
    print(future.result())

print(f"Published messages with retry settings to {topic_path}.")