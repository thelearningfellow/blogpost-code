## Install dependency
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Enable Docker Model Runner
```bash
docker desktop enable model-runner
docker desktop enable model-runner --tcp 12434
```

## Available models
https://hub.docker.com/u/ai

## Pull models
`docker model pull ai/smollm2:360M-Q4_K_M`

## List models
`docker model list`

## Interacting with models
`docker model run ai/smollm2:360M-Q4_K_M "Explain to me how AI works"`

or run `docker model run ai/smollm2:360M-Q4_K_M` to start in the interactive mode

or access via OpenAI compabitility API using curl or OpenAI sdk. 
Examples for making a request to an LLM and an embedding model are shared in `llm_request.py` and `embedding_request.py`, respectively.

## Access URLs

Model Runner exposes an OpenAI endpoint 
under http://model-runner.docker.internal/engines/v1 for containers, 
and under http://localhost:12434/engines/v1 for host processes (assuming you have enabled TCP host access on default port 12434)

Details of all the endpoints available is here: https://docs.docker.com/model-runner/#what-api-endpoints-are-available

## Getting the Logs 
docker model logs