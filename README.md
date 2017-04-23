# excusMeLambdas

## DB Schema
Table: Calls
* Partition key: Phone number-number (string)
* Sort key: Scheduled call time-datetime (int, as datetime.timestamp())
* Fake caller-caller (string)
* Fake excuse-excuse (string)
