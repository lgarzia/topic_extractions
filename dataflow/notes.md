
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

