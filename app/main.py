from fastapi import FastAPI
from pydantic import BaseModel
import uuid, json
from producer import send_to_queue

app = FastAPI()

class ScrapeRequest(BaseModel):
    urls: list[str]

@app.post("/scrape")
def create_scrape_job(request: ScrapeRequest):
    job_id = str(uuid.uuid4()) #generate a unique job id
    
    messages = []

    for idx, url in enumerate(request.urls):
        message = {
            "job_id": job_id,
            "url": url,
            "index": idx
        }
        messages.append(message)

        send_to_queue(json.dumps(messages))

    return {
        "job_id": job_id,
        "message": f"{len(request.urls)} URLs queued for scraping"
    }