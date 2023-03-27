*Pub Sub Documentation*
https://cloud.google.com/pubsub/docs/building-pubsub-messaging-system 

*Cloud Run* Documentation
https://cloud.google.com/run/docs/tutorials/pubsub
https://cloud.google.com/run/docs/triggering/pubsub-push

### Certification Notes
https://cloud.google.com/pubsub/docs/choosing-pubsub-or-lite
Pub/Sub Lite is only recommended for applications where achieving extremely low cost justifies some additional operational work.

https://cloud.google.com/pubsub/docs/choosing-pubsub-or-cloud-tasks
The core difference between Pub/Sub and Cloud Tasks is in the notion of implicit vs. explicit invocation.
**Pub/Sub** gives publishers no control over the delivery of the messages save for the guarantee of delivery. 
In this way, **Pub/Sub** supports implicit invocation: a publisher implicitly causes the subscribers to execute by publishing an event.


By contrast, **Cloud Tasks** is aimed at explicit invocation where the publisher retains full control of execution. In particular, a publisher specifies an endpoint where each message is to be delivered.

**Cloud Tasks** are appropriate for use cases where a task producer needs to defer or control the execution timing of a specific webhook or remote procedure call. 
**Pub/Sub** is optimal for more general event data ingestion and distribution patterns where some degree of control over execution can be sacrificed.

https://cloud.google.com/pubsub/docs/choosing-pubsub-or-cloud-tasks#detailed-feature-comparison

Max size of task/message	1MB	10MB (Pub/Sub)

https://cloud.google.com/pubsub/architecture
Topic: a named entity that represents a feed of messages.
*Subscription*: a named entity that represents an interest in receiving messages on a particular topic.
Subscriber (also called a consumer): receives messages on a specified *subscription*.
Pub/Sub is divided into two primary parts: the data plane, which handles moving messages between publishers and subscribers, 
and the control plane, which handles the assignment of publishers and subscribers to servers on the data plane.

The servers in the data plane are called forwarders, and the servers in the control plane are called routers.

steps of processing a message:
A publisher sends a message.
The message is written to storage.
Pub/Sub sends an acknowledgement to the publisher that it has received the message and guarantees its delivery to all attached subscriptions.
At the same time as writing the message to storage, Pub/Sub delivers it to subscribers.
Subscribers send an acknowledgement to Pub/Sub that they have processed the message.
**Once at least one subscriber for each subscription** has acknowledged the message, Pub/Sub deletes the message from storage.

The metrics that are most interesting to users of the service are exposed through Google Cloud Monitoring. 

https://cloud.google.com/pubsub/docs/reliability-intro#use_snapshot_and_seek_for_safe_deployments
Therefore, a bug introduced in new subscriber code you deploy that acknowledges messages without having processed them correctly could result in subscriber-induced message loss.

Pub/Sub offers the snapshot and seek feature, which can help you to ensure you process every message correctly, even in the face of subscriber bugs.
https://cloud.google.com/pubsub/docs/replay-overview#seek_to_a_snapshot
The only way to exit the flow of steps is when a subscriber is deemed working, at which point the snapshot can be deleted.

https://cloud.google.com/pubsub/docs/publish-receive-messages-client-library

https://cloud.google.com/pubsub/docs/authentication

https://cloud.google.com/pubsub/docs/resource-location-restriction
You can set a message storage policy when you create a new topic or when you update a topic.

https://cloud.google.com/pubsub/docs/create-topic
**Properties of Topics**
* Add a default subscription:
* Schema
* Message retention duration: Specifies how long the Pub/Sub topic retains messages after publication. After the message retention duration is over, Pub/Sub might discard the message regardless of its acknowledgment state.
    * Default = Not enabled
    * Minimum value = 10 minutes
    * Maximum value = 31 days

A Pub/Sub resource name uniquely identifies a Pub/Sub resource, such as a topic, subscription, schema or snapshot. The resource name must fit the following format:
projects/project-identifier/collection/ID
* collection: Must be one of topics, subscriptions, schemas, or snapshots.

A message consists of fields with the message data and metadata. Specify at least one of the following in the message:
* The message data
* An ordering key
* Attributes with additional metadata
If you're using the **REST API, the message data must be base64-encoded**.

After you publish a message, the Pub/Sub service returns the message ID to the publisher.
Attribute keys should not start with goog and should not exceed 256 bytes.

Use ordering keys
If messages have the same ordering key and you publish the messages to the same region, subscribers can receive the messages in order. Publishing messages with ordering keys might increase latency. To publish messages to the same region, use a regional endpoint.
https://cloud.google.com/pubsub/docs/publisher#retry_ordering

You can batch messages based on message request size, number of messages, and time. 
Variable	Description	Value
max_messages	The number of messages in a batch.	Default=100
max_bytes	The maximum size of a batch in MB.	Default=1 MB
max_latency	The time after which a batch is published, even if the batch is not filled.	Default=10 ms

To turn off batching in your client library, set the value of max_messages to 1.

https://cloud.google.com/pubsub/docs/publisher#retry
Publishing failures are automatically retried, except for errors that do not warrant retries. This sample code demonstrates creating a publisher with custom retry settings

https://cloud.google.com/pubsub/docs/subscriber
https://cloud.google.com/pubsub/docs/subscriber#what-subscription
Only messages published to the topic after the subscription is created are available to subscriber clients. However, you can also enable topic retention to allow a subscription attached to the topic to seek back in time and replay previously published messages. 

1. After a message is sent to a subscriber, the subscriber must acknowledge the message.
2. If a message is sent out for delivery and a subscriber is yet to acknowledge it, the message is called outstanding.
3.Pub/Sub repeatedly attempts to deliver any message that is not yet acknowledged. However, Pub/Sub tries not to deliver an outstanding message to any other subscriber on the same subscription.
4. The subscriber has a configurable, limited amount of time, known as the ackDeadline, to acknowledge the outstanding message. After the deadline passes, the message is no longer considered outstanding, and Pub/Sub attempts to redeliver the message.

# types of subscriptions
* Pull subscription
* Push subscription
* BigQuery subscription

For a single streaming pull request, a subscriber client can have multiple responses returned due to the open connection. In contrast, only one response is returned for each pull request.

The pull mode can use one of the two service APIs, Pull or StreamingPull. To run the chosen API, you can select a Google-provided high-level client library, or a low-level auto-generated client library. You can also choose between asynchronous and synchronous message processing.

Key Point: For most use cases, we recommend the Google-provided high-level client library with the StreamingPull API and asynchronous message processing.

https://cloud.google.com/pubsub/docs/pull#types_of_message_processing_modes
https://cloud.google.com/pubsub/docs/push#properties_of_a_push_subscription

* Endpoint URL (required)
* Enable authentication
* User-managed service account (required)
* Audience
* Google-managed service account (required)
