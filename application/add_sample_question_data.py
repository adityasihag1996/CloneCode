import json
import redis

with open("../sample_coding_data.json", "r") as json_file:
    data = json.load(json_file)

redis_host = 'localhost'
redis_port = 5678

# Establishing the Redis connection
r = redis.StrictRedis(host=redis_host, port=redis_port)

questions_counter_key = "questionsCount"
cc = 0

# Step 3: Write to Redis
for dp in data:
    question_id = dp["questionId"]
    if question_id is not None:
        r.set(f"questionId:{question_id}", json.dumps(dp))
        r.incr(questions_counter_key)
        cc += 1

print("Data written to Redis successfully.")
print("Count:", cc)