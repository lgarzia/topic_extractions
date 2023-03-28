# %%
from google.cloud import pubsub_v1

project_id = "podact-topic-extractor"
topic_id = "your-topic-id"
subscription_id = "your-subscription-id"
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
topic_path = publisher.topic_path(project_id, topic_id)
subscription_path = subscriber.subscription_path(project_id, subscription_id)

# Wrap the subscriber in a 'with' block to automatically call close() to
# close the underlying gRPC channel when done.
with subscriber:
    subscription = subscriber.create_subscription(
        request={"name": subscription_path, "topic": topic_path}
    )

print(f"Subscription created: {subscription}")
# %%
from google.cloud import pubsub_v1

# TODO(developer)
subscription_id = "your-subscription-id-push"
# endpoint = "https://my-test-project.appspot.com/push"

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
topic_path = publisher.topic_path(project_id, topic_id)
subscription_path = subscriber.subscription_path(project_id, subscription_id)

push_config = pubsub_v1.types.PushConfig(push_endpoint=endpoint)

# Wrap the subscriber in a 'with' block to automatically call close() to
# close the underlying gRPC channel when done.
with subscriber:
    subscription = subscriber.create_subscription(
        request={
            "name": subscription_path,
            "topic": topic_path,
            "push_config": push_config,
        }
    )

print(f"Push subscription created: {subscription}.")
print(f"Endpoint for subscription is: {endpoint}")

# %%
from google.cloud import pubsub_v1

# TODO(developer)
# project_id = "your-project-id"
# topic_id = "your-topic-id"
# subscription_id = "your-subscription-id"
# bigquery_table_id = "your-project.your-dataset.your-table"

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
topic_path = publisher.topic_path(project_id, topic_id)
subscription_path = subscriber.subscription_path(project_id, subscription_id)

bigquery_config = pubsub_v1.types.BigQueryConfig(
    table=bigquery_table_id, write_metadata=True
)

# Wrap the subscriber in a 'with' block to automatically call close() to
# close the underlying gRPC channel when done.
with subscriber:
    subscription = subscriber.create_subscription(
        request={
            "name": subscription_path,
            "topic": topic_path,
            "bigquery_config": bigquery_config,
        }
    )

print(f"BigQuery subscription created: {subscription}.")
print(f"Table for subscription is: {bigquery_table_id}")

# %%
# Modify
from google.cloud import pubsub_v1

# TODO(developer)
# project_id = "your-project-id"
# topic_id = "your-topic-id"
# subscription_id = "your-subscription-id"
# endpoint = "https://my-test-project.appspot.com/push"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

push_config = pubsub_v1.types.PushConfig(push_endpoint=endpoint)

subscription = pubsub_v1.types.Subscription(
    name=subscription_path, topic=topic_id, push_config=push_config
)

update_mask = {"paths": {"push_config"}}

# Wrap the subscriber in a 'with' block to automatically call close() to
# close the underlying gRPC channel when done.
with subscriber:
    result = subscriber.update_subscription(
        request={"subscription": subscription, "update_mask": update_mask}
    )

print(f"Subscription updated: {subscription_path}")
print(f"New endpoint for subscription is: {result.push_config}.")

# %%
from google.cloud import pubsub_v1

subscriber = pubsub_v1.SubscriberClient()
project_path = f"projects/{project_id}"

# Wrap the subscriber in a 'with' block to automatically call close() to
# close the underlying gRPC channel when done.
with subscriber:
    for subscription in subscriber.list_subscriptions(
        request={"project": project_path}
    ):
        print(subscription.name)
# %%
from google.cloud import pubsub_v1

# TODO(developer)
# project_id = "your-project-id"
topic_id = "your-topic-id"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

response = publisher.list_topic_subscriptions(request={"topic": topic_path})
for subscription in response:
    print(subscription)
# %%
from google.api_core.exceptions import GoogleAPICallError, RetryError
from google.cloud import pubsub_v1

# TODO(developer): Choose an existing subscription.
# project_id = "your-project-id"
# subscription_id = "your-subscription-id"

publisher_client = pubsub_v1.PublisherClient()
subscriber_client = pubsub_v1.SubscriberClient()
subscription_path = subscriber_client.subscription_path(project_id, subscription_id)

try:
    publisher_client.detach_subscription(
        request={"subscription": subscription_path}
    )
except (GoogleAPICallError, RetryError, ValueError, Exception) as err:
    print(err)

subscription = subscriber_client.get_subscription(
    request={"subscription": subscription_path}
)
if subscription.detached:
    print(f"{subscription_path} is detached.")
else:
    print(f"{subscription_path} is NOT detached.")
# %%
