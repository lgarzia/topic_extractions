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