
https://cloud.google.com/dataflow/docs/about-dataflow

pipeline options
--dataflow_service_options=enable_prime

https://cloud.google.com/dataflow/docs/guides/enable-dataflow-prime#feature-comparison

https://cloud.google.com/dataflow/docs/about-dataflow#shuffle_data_efficiently
Dataflow Shuffle moves the shuffle operation, used for grouping and joining data, out of worker VMs and into Dataflow for batch pipelines. Batch pipelines scale seamlessly, without any tuning required, into hundreds of terabytes.

https://cloud.google.com/dataflow/docs/about-dataflow#reduce_batch_processing_costs
Flexible Resource Scheduling (FlexRS) reduces batch processing costs by using advanced scheduling techniques, the Dataflow Shuffle service, and a combination of preemptible VM instances and regular VMs.

https://github.com/apache/beam/tree/master/sdks/python/apache_beam/examples

https://cloud.google.com/dataflow/docs/pipeline-lifecycle
What an execution graph is, and how an Apache Beam pipeline becomes a Dataflow job.

During graph construction, Apache Beam locally executes the code from the main entry point of the pipeline code, stopping at the calls to a source, sink or transform step, and turning these calls into nodes of the graph. 

Consequently, a piece of code in a pipeline's entry point (Java and Go main() method or the top-level of a Python script) locally executes on the machine that runs the pipeline, while the same code declared in a method of a DoFn object executes in the Dataflow workers.

The execution graph is then translated into JSON format, and the JSON execution graph is transmitted to the Dataflow service endpoint.

The Dataflow service then validates the JSON execution graph. When the graph is validated, it becomes a job on the Dataflow service. 

https://cloud.google.com/dataflow/docs/guides/pipeline-workflows
Streaming pipelines can be more complex to deploy than batch pipelines, and therefore can be more difficult to automate using continuous deployment. For example, you might need to determine how to replace or update an existing streaming pipeline. If you can't update a pipeline, or if you choose not to update it, you can use other methods such as coordinating multiple Dataflow jobs to minimize or prevent business disruption.

https://cloud.google.com/dataflow/docs/guides/pipeline-workflows#traditional-vs-templates
Dataflow offers the following types of job templates:

Classic Templates: Developers use the Apache Beam SDK to run the pipeline code and save the JSON serialized execution graph as the template. The Apache Beam SDK stages the template file to a Cloud Storage location, along with any dependencies that are required by the pipeline code.

Flex Templates: Developers use the Google Cloud CLI to package the pipeline as a Docker image, which is then stored in Artifact Registry. A Flex Template spec file is also automatically generated and stored to a user-specified Cloud Storage location. The Flex Template spec file contains metadata that describes how to run the template, such as pipeline parameters.

https://cloud.google.com/dataflow/docs/guides/pipeline-workflows#optimize-resource-usage
Streaming Engine: Streaming Engine moves the execution of streaming pipelines out of VM workers and into a dedicated service. 
Dataflow Shuffle: Dataflow Shuffle moves shuffle operations for batch pipelines out of VM workers and into a dedicated service.
Flexible resource scheduling (FlexRS): FlexRS reduces batch processing costs by using advanced scheduling techniques, the Dataflow Shuffle service, and a combination of preemptible VM instances and regular VMs.

https://cloud.google.com/dataflow/docs/guides/pipeline-workflows#update-streaming-pipelines-prod
https://cloud.google.com/dataflow/docs/guides/pipeline-workflows#in-place-updates
https://cloud.google.com/dataflow/docs/guides/pipeline-workflows#stop-and-replace
https://cloud.google.com/dataflow/docs/guides/pipeline-workflows#message-reprocessing
Pub/Sub Seek is a feature that lets you replay messages from a Pub/Sub Snapshot. You can use the Pub/Sub Seek feature with Dataflow pipelines to reprocess messages from the time when the subscription snapshot is created

https://cloud.google.com/dataflow/docs/guides/pipeline-workflows#run-parallel-pipelines
Facade pattern

https://cloud.google.com/dataflow/docs/guides/pipeline-workflows#schema-mutations
https://cloud.google.com/dataflow/docs/guides/pipeline-workflows#schema-tables

https://cloud.google.com/dataflow/docs/guides/pipeline-workflows#dataflow-snapshots

https://cloud.google.com/dataflow/docs/guides/pipeline-workflows#job-submission-failures

https://cloud.google.com/dataflow/docs/concepts/exactly-once
https://cloud.google.com/dataflow/docs/concepts/streaming-with-cloud-pubsub
