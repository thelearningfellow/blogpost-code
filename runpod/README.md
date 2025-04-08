# Runpod Endpoint

## Creating an endpoint
Create a virtual environment and install dependencies
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set the API Key from runpod in an environment variable
```sh
export RUNPOD_API_KEY=
```

Create the template using vllm and create endpoint 
```sh
cd endpoints/
python create_endpoint.py
```

### Send request to the endpoint
```sh
curl https://api.runpod.ai/v2/<ENDPOINT_ID>/openai/v1/chat/completions \                      
-H "Content-Type: application/json" \
-H "Authorization: Bearer <RUNPOD_API_KEY>" \
-d '{
"model": "YOUR_HF_MODEL_ID",
"messages": [
  {
    "role": "user",
    "content": "What is the best LLM out there?"
  }
],
"temperature": 0,
"max_tokens": 100
}'
```