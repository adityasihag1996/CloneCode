from flask import Flask, request, jsonify
import redis
from rq import Queue
import time

app = Flask(__name__)

# Configure the Redis connection and RQ Queue
jobs_rq_url = "redis://localhost:4567"
redis_server = redis.Redis.from_url(jobs_rq_url)
redis_rq = Queue('runs', connection = redis_server)

@app.route('/submit', methods=['POST'])
def submit():
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 400
    
    data = request.get_json()
    data["run_id"] = int(time.time_ns())

    try:
        # Enqueue the task
        enqueue_job = redis_rq.enqueue('tasks.process_data', data)
    except:
        return jsonify({"message": "Couldn't enqueue task."}), 400
    
    return jsonify({
        "run_id": data["run_id"],
        "message": "Data received and task enqueued",
        "job_id": enqueue_job.id}), 202
        

if __name__ == '__main__':
    app.run(debug = True, port = 5577)



# from redis import Redis
# from rq import Queue
# import time

# # Connect to Redis server
# redis_conn = Redis(
#     host = 'localhost',
#     port = 4567,
#     db = 0,
#     password = 'yourpassword'
# )

# # Setup the queue and worker
# redis_rq = Queue('runs', connection = redis_conn)

# data = {}

# for i in range(100):
#     data["idx"] = i
#     data["code"] = f"print(\"hello world, {i}\")"
#     data["run_id"] = int(time.time_ns())
#     enqueue_job = redis_rq.enqueue('tasks.process_data', data)
#     # time.sleep(0.1)