from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
import time

app = Flask(__name__)

# RQ
redis_server = Redis(
    host = 'localhost',
    port = 4567,
    db = 0,
    password = 'yourpassword'
)
redis_rq = Queue('runs', connection = redis_server)

# QUESTIONS DB
redis_server = Redis(
    host = 'localhost',
    port = 5678,
    db = 0,
    password = 'yourpassword'
)

@app.route('/submit', methods=['POST'])
def submit():
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 400
    
    data = request.get_json()
    data["run_id"] = int(time.time_ns())

    # fetch question for QUESTION_DB, using questionId / titleSlug
    # send the entire code packet in "data"

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
