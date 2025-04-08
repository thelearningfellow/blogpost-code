""" Example of creating an endpoint with the Runpod API. """

import runpod
import requests
import os 

# Set your global API key with `runpod config` or other set environment variable:
runpod.api_key = os.getenv("RUNPOD_API_KEY")

try:

    new_template = runpod.create_template(
        name="test-template", image_name="runpod/worker-v1-vllm:v2.2.0stable-cuda12.1.0", is_serverless=True, env={
            "MODEL_NAME": "microsoft/Phi-4-mini-instruct", # Replace with your model name
            # "HF_TOKEN": os.getenv("HF_TOKEN"), # Replace with your Hugging Face token
            "MAX_MODEL_LEN": 4096,
            "TENSOR_PARALLEL_SIZE": 1,
            "MAX_NUM_SEQS": 64,
            "MAX_CONCURRENCY": 1
        }
    )

    print(new_template)
    response = requests.post("https://rest.runpod.io/v1/endpoints",
        headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {runpod.api_key}"
        },
        json={
        "name": "test-endpoint",
        "allowedCudaVersions": [
            "12.1",
            "12.2",
            "12.3"
        ],
        "computeType": "GPU",
        # If you want to use the endpoint in a specific region, uncomment the following line and specify the region IDs
        # "dataCenterIds": [
        #     "EU-RO-1",
        #     "CA-MTL-1"
        # ],
        "executionTimeoutMs": 600000,
        "flashboot": True,
        "gpuCount": 1,
        "gpuTypeIds": [
            "NVIDIA GeForce RTX 4090"
        ],
        "idleTimeout": 5,
        "name": "",
        "networkVolumeId": "",
        "scalerType": "QUEUE_DELAY",
        "scalerValue": 4,
        "templateId": new_template["id"],
        "vcpuCount": 2,
        "workersMax": 1,
        "workersMin": 0
        }
    )

    response.raise_for_status()
    new_endpoint = response.json()
    print(new_endpoint)

except runpod.error.QueryError as err:
    print(err)
    print(err.query)