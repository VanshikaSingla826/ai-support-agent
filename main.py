from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from crew import kickoff_support_crew
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/solve")
async def solve(
    request: Request, 
    customer_name: str = Form(...),
    ticket_priority: str = Form(...),
    ticket_issue: str = Form(...),
    ticket_details: str = Form(...)
):
    if not os.getenv("GEMINI_API_KEY"):
         return templates.TemplateResponse("index.html", {"request": request, "result": "Error: API Keys missing."})
    
    # Bundle inputs for the Crew
    inputs = {
        "customer_name": customer_name,
        "ticket_priority": ticket_priority,
        "ticket_issue": ticket_issue,
        "ticket_details": ticket_details
    }
    
    result = kickoff_support_crew(inputs)
    return templates.TemplateResponse("index.html", {"request": request, "result": result})