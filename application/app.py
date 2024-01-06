from flask import Flask, request, jsonify
from flask_cors import CORS
from redis import Redis
from rq import Queue
import time, json

app = Flask(__name__)
CORS(app)

# RQ
redis_rq_conn = Redis(
    host = 'localhost',
    port = 4567,
    db = 0,
    decode_responses = True,
)
redis_rq = Queue('runs', connection = redis_rq_conn)

# QUESTIONS DB
redis_ques_conn = Redis(
    host = 'localhost',
    port = 5678,
    db = 0,
    decode_responses = True,
)

# metadata Redis conn
redis_metadata_conn = Redis(
    host = 'localhost',
    port = 6789,
    db = 0,
    decode_responses = True,
)

@app.route('/submit', methods=['POST'])
def submit():
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 400
    
    data = request.get_json()
    data["run_id"] = int(time.time_ns())

    # Specify the questionId you want to fetch
    question_id = str(data["question_id"])

    # Fetch the data for the specified questionId
    question_data = redis_ques_conn.get(f"questionId:{question_id}")
    question_data = json.loads(question_data)
    data["exampleTestcase"] = question_data["exampleTestcase"]
    data["exampleTestcaseResult"] = question_data["exampleTestcaseResult"]
    data["inplaceResult"] = question_data["inplaceResult"]

    data["code"] = data["fillCode"] + question_data["runnerSkeletonCode"]
    del data["fillCode"]

    try:
        # Enqueue the task
        enqueue_job = redis_rq.enqueue('tasks.process_data', data)
    except:
        return jsonify({"message": "Couldn't enqueue task."}), 400
    
    return jsonify({
        "run_id": data["run_id"],
        "message": "Data received and task enqueued",
        "job_id": enqueue_job.id}), 202

@app.route('/totalCount', methods=['GET'])
def totalCount():
    total_questions = redis_ques_conn.get("questionsCount")
    
    return jsonify({
        "totalCount": total_questions}), 202

@app.route('/problem', methods=['GET'])
def problem():
    question_id = request.args.get('questionId')
    question_data = redis_ques_conn.get(f"questionId:{question_id}")

    if question_data is None:
        # Handle the case where the question is not found
        return jsonify({
            "message": "Question not found",
        }), 404

    return jsonify({
        "question_data": json.loads(question_data)
    }), 202

@app.route('/runData', methods=['GET'])
def runData():
    run_id = request.args.get('runId')
    run_data = redis_metadata_conn.hgetall(f"run_id:{run_id}")

    if not run_data:
        # Handle the case where the question is not found
        return jsonify({
            "message": "Run Data not found",
        }), 404

    return jsonify({
        "run_data": run_data
    }), 202

        

if __name__ == '__main__':
    app.run(debug = True, port = 5577)
