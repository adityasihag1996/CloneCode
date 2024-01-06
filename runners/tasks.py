import time
import docker
from redis import Redis

from utils import timeout

def process_data(json_data):
    # local Redis conn
    local_redis = Redis(
        host = 'localhost',
        port = 8899,
        db = 0,
        decode_responses = True,
    )

    # metadata Redis conn
    metadata_redis = Redis(
        host = 'localhost',
        port = 6789,
        db = 0,
        decode_responses = True,
    )

    free_containers = local_redis.zrangebyscore('containers', min=0, max=0, start=0, num=1)
    container = docker.from_env().containers.get(str(free_containers[0]))
    local_redis.zadd('containers', {container.id: 1})  # Mark as busy

    ## DO SOME PROCESSSING IN THE CONTAINER
    code = json_data['code']
    code = code.replace("#$HERE GOES THE INPLACE RESULT#$", str(json_data["inplaceResult"]))

    processing_times = []
    outputs = []
    test_cases_passed = 0

    for tc, tcr in zip(json_data["exampleTestcase"], json_data["exampleTestcaseResult"]):
        if type(tc) == str:
            tc = f'''"{tc}"'''

        if type(tcr) == str:
            tcr = f'''"{tcr}"'''

        new_code = code.replace("#$HERE GOES THE TESTCASE#$", str(tc))
        new_code = new_code.replace("#$HERE GOES THE TESTCASE RESULT#$", str(tcr))

        start_time = time.time_ns()
        try:
            out = exec_on_docer_container(container, new_code)
        except Exception as e:
            out = "Timeout Error."
        end_time = time.time_ns()
        total_time_taken = round((end_time - start_time) / 1000000, 2)

        parsed_out = parse_output(out)

        processing_times.append(total_time_taken)
        outputs.append(parsed_out)

        print(f"Container {container.id} output:")
        print(parsed_out)

        if parsed_out["error"] != "$$__REDIS__NONE__$$":
            test_cases_passed += 1

    local_redis.zadd('containers', {container.id: 0})  # Mark as free

    # log metadata in metadaba_db
    run_id = json_data["run_id"]
    log_data = {
        "run_id": run_id,
        "time_taken": str([o["time_taken"] for o in outputs]),
        "total_time_taken": total_time_taken,
        "pass_status": str([o["pass_status"] for o in outputs]),
        "result": str([o["result"] for o in outputs]),
        "error": str([o["error"] for o in outputs]),
        "test_cases_passed": test_cases_passed,
    }

    metadata_redis.hmset(f"run_id:{run_id}", log_data)


@timeout(5)
def exec_on_docer_container(container, new_code):
    exec_id = container.exec_run(f"python -c '{new_code}'", workdir = "/app")
    out = exec_id.output.decode()
    return out
    

def parse_output(output):
    lines = output.split('\n')
    
    if "PASSED QWERTY" in lines[0]:
        # Extracting data from the following lines
        time_taken, pass_status = lines[1].split()
        result = lines[2]
        return {
            "time_taken": time_taken,
            "pass_status": pass_status,
            "result": result,
            "error": "$$__REDIS__NONE__$$",
        }
    else:
        # Entire output is considered as an error message
        return {
            "time_taken": "$$__REDIS__NONE__$$",
            "pass_status": "$$__REDIS__NONE__$$",
            "result": "$$__REDIS__NONE__$$",
            "error": output,
        }
    