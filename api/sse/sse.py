import psutil 
import json 
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

# Configure Jinja2 templates
# Assumes you have a 'templates' directory in the same directory as your Python file
templates = Jinja2Templates(directory="templates")

# Root endpoint to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serves the index.html template.
    """
    return templates.TemplateResponse("index.html", {"request": request})

# SSE endpoint to stream metrics 
@app.get("/events/metrics")
async def message_stream(request: Request):
    """
    Streams CPU, memory, and disk utilization data to the client using Server-Sent Events.
    Data is sent as a JSON string.
    """
    async def event_generator():
        """
        Generates events (system metrics) to be sent to the client.
        """
        # Check if client is still connected
        while True:
            if await request.is_disconnected():
                break

            try:
                # Get system utilization percentages
                cpu_percent = psutil.cpu_percent(interval=1) # interval=1 blocks for 1 second
                memory_info = psutil.virtual_memory()
                disk_info = psutil.disk_usage('/') # Use '/' for root partition on Unix-like systems, adjust as needed for Windows (e.g., 'C:\\')

                # Create a dictionary with the system metrics
                system_metrics = {
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory_info.percent,
                    "disk_percent": disk_info.percent
                }

                # Serialize the dictionary to a JSON string
                json_data = json.dumps(system_metrics)

                # Format the data as an SSE data message
                # The 'data:' line should contain the JSON string
                yield f"{json_data}\n\n"

            except Exception as e:
                # Log any errors but keep the generator running
                print(f"Error getting system utilization: {e}")
                # Send an error message to the client if needed
                yield f"data: {json.dumps({'error': str(e)})}\n\n"


    # Return an EventSourceResponse which handles the SSE protocol
    return EventSourceResponse(event_generator())