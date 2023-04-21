https://cloud.google.com/bigtable/docs/overview

An SSTable provides a persistent, ordered immutable map from keys to values, where both keys and values are arbitrary byte strings.
Each tablet is associated with a specific Bigtable node.
SSTable files, all writes are stored in Colossus's shared log as soon as they are acknowledged by Bigtable, providing increased durability.

Importantly, data is never stored in Bigtable nodes themselves; each node has pointers to a set of tablets that are stored on Colossus. As a result:

To get the best write performance from Bigtable, it's important to distribute writes as evenly as possible across nodes.

At the same time, it's useful to group related rows so they are next to one another
https://cloud.google.com/bigtable/docs/schema-design#row-keys

Bigtable treats all data as raw byte strings for most purposes.
The only time Bigtable tries to determine the type is for increment operations, where the target must be a 64-bit integer encoded as an 8-byte big-endian value.

https://cloud.google.com/bigtable/docs/overview#memory-disk
Each row is essentially a collection of key/value entries, where the key is a combination of the column family, column qualifier and timestamp.

Column qualifiers take up space in a row, since each column qualifier used in a row is stored in that row. As a result, it's often efficient to use column qualifiers as data.

To use Cloud Bigtable, you create instances, which contain clusters that your applications can connect to. Each cluster contains nodes, the compute units that manage your data and perform maintenance tasks.



Note: You can perform Bigtable operations at the command line using either the HBase shell or the cbt tool. Use the HBase shell if you are accustomed to it and prefer to use it. Otherwise, we recommend that you use the cbt CLI, which has fewer dependencies and installation steps. The cbt CLI is a component of the Google Cloud CLI.

**Cloud Bigtable allows for queries using point lookups by row key or row-range scans that return a contiguous set of rows.**
if your schema isn't well thought out, you might find yourself piecing together multiple row lookups, or worse, doing full table scans, which are extremely slow operations.

https://cloud.google.com/bigtable/docs/choosing-ssd-hdd
https://cloud.google.com/bigtable/docs/creating-instance
A Cloud Bigtable instance is a container for Bigtable clusters. An instance that has more than one cluster uses replication. You can create clusters in up to 8 regions, with as many clusters in each region as there are zones.

https://cloud.google.com/bigtable/docs/modifying-instance
After you create a Cloud Bigtable instance, you can update the following settings without any downtime:
* Autoscaling
* The number of nodes in manually scaled clusters
* The number of clusters in the instance
* The application profiles for the instance, which contain replication settings
* The location of your data
* The labels for the instance, which provide metadata about the instance
* The display name for the instance

If you delete a cluster, and some writes to that cluster have not been replicated yet, Bigtable finishes the replication process before it removes the deleted cluster's copy of your data. The remaining cluster continues to show incoming writes and CPU utilization until the replication process is complete.

If one of your application profiles routes all traffic to a single cluster, Bigtable will not allow you to delete that cluster. You must edit or delete the application profile before you can remove the cluster.

Application profiles, or app profiles, control how your applications connect to an instance that uses replication. Every instance with more than 1 cluster has its own default app profile. You can also create many different custom app profiles for each instance, using a different app profile for each kind of application that you run.

Labels are key-value pairs that you can use to group related instances and store metadata about an instance.

For example, if your cluster is under heavy load and its CPU utilization is high, you can add nodes to the cluster until its CPU usage drops. You can also save money by removing nodes from the cluster when it is not being used heavily.

https://cloud.google.com/bigtable/docs/scaling#scaling_options
* Autoscaling
* Manual node allocation
* Programmatic scaling

https://cloud.google.com/bigtable/docs/scaling#availability
https://cloud.google.com/bigtable/docs/scaling#schema_design_issues

Scaling Clusters:
Scaling a cluster is the process of adding or removing nodes to a cluster in response to changes in the cluster's workload or data storage needs.

https://cloud.google.com/bigtable/docs/cbt-reference
When you create a table, you do not need to specify the column families to use in the table. You can add or delete column families later.
You can add columns now or later. A table must have at least one column family before you can write data to it.

Pre-splitting your table is not essential, but it is beneficial because it provides Bigtable information about where the load and data footprint are likely to land when the table is created. The pre-split prevents Bigtable from having to split the tables and rebalance the load all at once as the data arrives.

Warning: When you delete a column family, you also delete the data stored in that column family. Deleting a column family can't be undone.

https://cloud.google.com/bigtable/docs/managing-tables#gc-policies
A garbage collection policy tells Bigtable which data to keep and which data to mark for deletion. Garbage collection policies are set at the column family level. You can set them when you create the table or later.

https://cloud.google.com/bigtable/docs/managing-tables#undelete-table <-- note difference with Column Family

https://cloud.google.com/bigtable/docs/replication-overview
With replication, you can use app profiles with single-cluster routing to route batch analytics jobs and application traffic to different clusters, so that batch jobs don't affect your applications' users

By default, replication for Bigtable is eventually consistent.

 Bigtable can also provide read-your-writes consistency when replication is enabled, which ensures that an application will never read data that is older than its most recent writes
 Bigtable can also provide strong consistency, which ensures that all of your applications see your data in the same state. 

 Each cell value in a Bigtable table is uniquely identified by the four-tuple (row key, column family, column qualifier, timestamp).

 https://cloud.google.com/bigtable/docs/replication-overview#app-profiles
 * If an instance uses replication, you use application profiles, or app profiles, to specify routing policies.

https://cloud.google.com/bigtable/docs/replication-overview#routing-policies
* Single-cluster routing: Sends all requests to a single cluster that you specify.
* Multi-cluster routing to any cluster: Sends requests to the nearest available cluster in the instance.
* Cluster group routing: Sends requests to the nearest available cluster within a cluster group that you specify in the app profile settings.

common use cases for enabling Cloud Bigtable replication,
* Isolate batch analytics workloads from other applications
* Create high availability
* Provide near-real-time backup
* Maintain high availability and regional resilience
* Store data close to your users

https://cloud.google.com/bigtable/docs/failovers#manual
* The cluster starts to return a large number of transient system errors.
* A large number of requests start timing out.
* The average response latency increases to an unacceptable level.

Fully integrated: Backups are handled entirely by the Bigtable service, with no need to import or export.
Cost effective: Using Bigtable backups lets you avoid the costs associated with exporting, storing, and importing data using other services.
Automatic expiration: Each backup has a user-defined expiration date that can be up to 30 days after the backup is created.
Flexible restore options: You can restore from a backup to a table in any instance or project.

Backups can help you recover from application-level data corruption or from operator errors such as accidentally deleting a table.

https://cloud.google.com/bigtable/docs/schema-design
he recommendations on this page are designed to help you optimize for row range reads. In most cases, that means sending a query based on row key prefixes.
Rows are sorted lexicographically by row key, from the lowest to the highest byte string. Row keys are sorted in big-endian byte order (sometimes called network byte order), the binary equivalent of alphabetical order.

Because all tables in an instance are stored on the same tablets, a schema design that results in hotspots in one table can affect the latency of other tables in the same instance. Hotspots are caused by frequently accessing one part of the table in a short period of time.

Put columns that have different data retention needs in different column families. This practice is important if you want to limit storage costs. Garbage collection policies are set at the column family level, not at the column level. For example, if you only need to keep the most recent version of a particular piece of data, don't store it in a column family that is set to store 1,000 versions of something else.

Create as many columns as you need in the table. Bigtable tables are sparse, and there's no space penalty for a column that is not used in a row. You can have millions of columns in a table, as long as no row exceeds the maximum limit of 256 MB per row.

 The most efficient Bigtable queries retrieve data using one of the following:

Row key
Row key prefix
Range of rows defined by starting and ending row keys

Often, you should design row keys that start with a common value and end with a granular value. For example, if your row key includes a continent, country, and city, you can create row keys that look like the following so that they automatically sort first by values with lower cardinality:

https://cloud.google.com/bigtable/docs/schema-design#row-keys-avoid