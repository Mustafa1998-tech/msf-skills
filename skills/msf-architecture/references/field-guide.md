# Field procedure

For each boundary write who calls, who owns the write and who handles retry. A synchronous call is acceptable where latency and availability fit. Use an outbox only if a committed write and asynchronous notification must survive a crash together. Choose a correlation ID, a bounded retry policy and failure retention. Compare the cheapest safe migration with a staged compatible change. Record estimated workload separately from benchmark evidence.
