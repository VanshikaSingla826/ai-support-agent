import os
import csv
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crew import kickoff_support_crew

app = FastAPI()

# Enable CORS (Allows your frontend to talk to this backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA MODEL ---
class Ticket(BaseModel):
    customer_name: str
    customer_email: str  # Added Email field
    priority: str
    issue_title: str
    ticket_details: str

# --- LOGGING FUNCTION ---
def log_ticket_to_csv(ticket_data: dict, solution: str):
    file_exists = os.path.isfile('ticket_logs.csv')
    with open('ticket_logs.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "customer", "email", "priority", "title", "details", "solution_preview"
        ])
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer": ticket_data['customer_name'],
            "email": ticket_data['customer_email'],
            "priority": ticket_data['priority'],
            "title": ticket_data['issue_title'],
            "details": ticket_data['ticket_details'],
            "solution_preview": solution[:100] + "..." # Save first 100 chars
        })

# --- ENDPOINTS ---
@app.post("/solve")
def solve_ticket(ticket: Ticket):
    # 1. Run the AI Crew
    inputs = {
        "customer_name": ticket.customer_name,
        "ticket_priority": ticket.priority,
        "ticket_issue": ticket.issue_title,
        "ticket_details": ticket.ticket_details
    }
    
    try:
        # Run AI
        result = kickoff_support_crew(inputs)
        final_answer = str(result)

        # 2. Log the data for analytics
        log_ticket_to_csv(ticket.dict(), final_answer)
        
        # 3. Create a downloadable file for the user
        filename = f"solution_{datetime.now().strftime('%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"SUPPORT TICKET SOLUTION\n")
            f.write(f"-----------------------\n")
            f.write(f"Issue: {ticket.issue_title}\n")
            f.write(f"Date: {datetime.now()}\n\n")
            f.write(final_answer)

        return {
            "solution": final_answer,
            "download_url": f"/download/{filename}"
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = f"./{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/octet-stream', filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/logs")
def get_logs():
    # Endpoint to view the CSV logs directly in browser
    if os.path.exists('ticket_logs.csv'):
        return FileResponse('ticket_logs.csv', media_type='text/csv', filename='analytics.csv')
    return {"message": "No logs yet."}