*Pub Sub Documentation*
https://cloud.google.com/pubsub/docs/building-pubsub-messaging-system 

*Cloud Run* Documentation
https://cloud.google.com/run/docs/tutorials/pubsub
https://cloud.google.com/run/docs/triggering/pubsub-push

*App Engine* Documentation
https://cloud.google.com/appengine/docs/flexible/writing-and-responding-to-pub-sub-messages?tab=python

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

https://cloud.google.com/python/docs/reference/pubsub/latest

https://cloud.google.com/pubsub/docs/push#receive_push
When Pub/Sub delivers a message to a push endpoint, Pub/Sub sends the message in the body of a POST request. 
The body of the request is a JSON object and the message data is in the message.data field. 
The message data is **base64-encoded**.

The following example is the body of a POST request to a push endpoint:
102 - The 102 Processing status code means that the server has accepted the full request but has not yet completed it and no response is available as of yet
200
201
202
204

https://jwt.io/introduction
JSON Web Token (JWT) is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed. JWTs can be signed using a secret (with the HMAC algorithm) or a public/private key pair using RSA or ECDSA.

**Authorization**: This is the most common scenario for using JWT. Once the user is logged in, each subsequent request will include the JWT, allowing the user to access routes, services, and resources that are permitted with that token. Single Sign On is a feature that widely uses JWT nowadays, because of its small overhead and its ability to be easily used across different domains.

**Information Exchange**: JSON Web Tokens are a good way of securely transmitting information between parties. Because JWTs can be signed—for example, using public/private key pairs—you can be sure the senders are who they say they are. Additionally, as the signature is calculated using the header and the payload, you can also verify that the content hasn't been tampered with.

In its compact form, JSON Web Tokens consist of three parts separated by dots (.), which are:

* Header
* Payload
* Signature
Therefore, a JWT typically looks like the following.

xxxxx.yyyyy.zzzzz

---
If subscribers use a firewall, they can't receive push requests. To receive push requests, you must turn off the firewall and verify the JWT.
https://openid.net/specs/draft-jones-json-web-token-07.html
https://developers.google.com/identity/openid-connect/openid-connect

Validating tokens sent by Pub/Sub to the push endpoint involves:

Checking the token integrity by using signature validation.
Ensuring that the email and audience claims in the token match the values set in the push subscription configuration.
The following example illustrates how to authenticate a push request to an App Engine application not secured with Identity-Aware Proxy. If your App Engine application is secured with IAP, the HTTP request header that contains the IAP JWT is x-goog-iap-jwt-assertion and must be validated accordingly.

Cloud Run, App Engine, and Cloud Functions authenticate HTTP calls from Pub/Sub by verifying Pub/Sub-generated tokens. The only configuration that you require is to grant the necessary IAM roles to the caller account.

https://cloud.google.com/pubsub/docs/push#cloud-run:

To temporarily stop Pub/Sub from sending requests to the push endpoint, change the subscription to pull. The changeover can take several minutes to take effect.

If a push subscriber sends too many negative acknowledgments, Pub/Sub might start delivering messages using a push backoff. When Pub/Sub uses a push backoff, it stops delivering messages for a predetermined amount of time. This time span can range between 100 milliseconds to 60 seconds. After the time has elapsed, Pub/Sub starts delivering messages again.

Push backoff uses an exponential backoff algorithm to determine the delay Pub/Sub that uses between sending messages. This amount of time is calculated based on the number of negative acknowledgments that push subscribers send.

Pub/Sub adjusts the number of concurrent push requests using a slow-start algorithm. The maximum allowed number of concurrent push requests is the push window. The push window increases on any successful delivery and decreases on any failure. The system starts with a small single-digit window size.

https://cloud.google.com/pubsub/docs/bigquery

* Use topic schema. 
* Write metadata. 
* Drop unknown fields

If you do not select the Write metadata option, then the destination BigQuery table only requires the data field unless use_topic_schema is true

Without Drop unknown fields set, messages with extra fields are not written to BigQuery and remain in the subscription backlog.

https://cloud.google.com/pubsub/docs/create-subscription

Subscribers use a subscription to read messages from a topic. When you create a subscription, you attach it to a topic. You can attach many subscriptions to a single topic.

Subscription Prperties
https://cloud.google.com/pubsub/docs/create-subscription#subscription_properties

* Message retention duration
* Retain acknowledged messages
* Expiration period
* Acknowledgment deadline
* Subscription filter - You cannot update a filter for a subscription
* Message ordering
* Dead letter topic. When a message can't be delivered after a set number of delivery attempts or a subscriber can't acknowledge the message, the message is republished to a dead-letter topic.
* Retry policy
* Exactly-once delivery -> default is at-least-once

https://cloud.google.com/pubsub/docs/create-subscription#assign_bigquery_service_account
https://cloud.google.com/pubsub/docs/create-subscription#detach_a_subscription_from_a_topic
When you create a subscription, you attach the subscription to a topic, and subscribers can receive messages from the subscription. To stop subscribers from receiving messages, you can detach subscriptions from the topic.

**Configure Delivery Options**
https://cloud.google.com/pubsub/docs/flow-control
Flow control thus handles traffic spikes without driving up costs or until the subscriber is scaled up.
https://cloud.google.com/pubsub/docs/flow-control#flow_control_configuration

If the limit for setMaxOutstandingElementCount() or setMaxOutstandingRequestBytes() is crossed, the subscriber client does not pull more messages.

https://cloud.google.com/pubsub/docs/handling-failures
This page explains how to handle such processing failures by using a subscription retry policy or by forwarding undelivered messages to a dead-letter topic (also known as a dead-letter queue).
Note that these features are not supported by Dataflow. Refer to the Unsupported Pub/Sub features section of the Dataflow documentation for further information.

https://cloud.google.com/pubsub/docs/handling-failures#dead_letter_topic
A dead-letter topic is a subscription property, not a topic property. This means that you set a dead-letter topic when you create a subscription, not when you create a topic.

* Maximum number of delivery attempts
* Project with the dead-letter topic
https://cloud.google.com/pubsub/docs/handling-failures#configure_a_dead_letter_topic
1. Create the dead-letter topic. This topic is separate from the source topic.
2. Set the dead-letter topic on the subscription for the source topic.
3. To avoid losing messages from the dead-letter topic, attach at least one other subscription to the dead-letter topic. The secondary subscription receives messages from the dead-letter topic.
4. Grant the publisher and subscriber roles to the Pub/Sub service account. For more information, see Grant forwarding permissions.

https://cloud.google.com/pubsub/docs/replay-overview

The Seek feature extends subscriber functionality by allowing you to alter the acknowledgement state of messages in bulk. For example, you can replay previously acknowledged messages or purge messages in bulk. In addition, you can copy the state of one subscription to another by using seek in combination with a Snapshot.

To seek to a time in the past and replay previously-acknowledged messages, you must first configure message retention on the topic or configure the subscription to retain acknowledged messages.
https://cloud.google.com/pubsub/docs/replay-overview#seek_to_a_time

https://cloud.google.com/pubsub/docs/replay-overview#seek_to_a_snapshot
The snapshot feature allows you to capture the message acknowledgment state of a subscription. Once a snapshot is created, it retains:
All messages that were unacknowledged in the source subscription at the time of the snapshot's creation.
Any messages published to the topic thereafter.

https://cloud.google.com/pubsub/docs/lease-management#lease_management_configuration

https://cloud.google.com/pubsub/docs/ordering#receiving_messages_in_order

https://cloud.google.com/pubsub/docs/subscription-message-filter
The Pub/Sub service automatically acknowledges the messages that don't match the filter. You can filter messages by their attributes, but not by the data in the message.


