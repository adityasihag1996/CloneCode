# CloneCode
A toy Leetcode clone, with separate standalone services like Application Layer, Message Queue, Worker Layer, MetadataDB, QuestionsDB.

**_(This is by no means a production ready code. It was developed more as a learning than a product.)_**

**_(All docker, redis shell commands are for MacOS, porting it for linux is pending. But the code can be still deployed on linux if manually each component is started.)_**

## Table of Contents

- [Installation](#Installation)
- [Architecture](#Architecture)
- [Contributing](#Contributing)

## Installation
To use this implementation, you will need to have Python >= 3.10 installed on your system.
Conda and Docker are also required.

```
bash start_full_service.sh
python application/add_sample_question_data.py
```

The FE is very crude, again, because CloneCode was developed for learning purposes, not productifying it.

## Architecture
The architecture has multiple components:-
- User/Client - The CloneCode FE client.
- Application Layer - Hosts all API calls for question fetch, and submit action flow.
- Message Queue - Queues all submit jobs to be evaluated.
- Worker Layer - Subscribed to the Message Queue, fetches a job, evaluates the code by executing them in docker isolated container. Each worker machine has several docker conatainers running, taking advantage of the hardware and isolation principles.
- QuestionsDB - redis server hosting all questions related data.
- MetadataDB - redis server hosting all runs metadata (run time, results, etc).

The submit flow looks something like this:-

![Sample Image](/submit_flow_40.jpg "Submit Flow")

The result fetch flow is simple:-
- When client hits submit, a *run_id* is returned by the API, along with enqueueing the job in RedisRQ.
- The *run_id* is then used to poll the MetadataDB to see if results are ready or not. (Can be changed to Long polling also)

![Sample Image](/FE1.jpg "FE1")
![Sample Image](/FE2.jpg "FE2")

## Contributing
Contributions to improve the project are welcome. Please follow these steps to contribute:

Fork the repository.\
Create a new branch for each feature or improvement.\
Submit a pull request with a comprehensive description of changes.
