from fastapi import FastAPI
from pydantic import BaseModel
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = FastAPI()

SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = "DEIN_KALENDER_ID"

class Appointment(BaseModel):
    summary: str
    start: str
    end: str

@app.post("/book")
def book_appointment(appt: Appointment):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": appt.summary,
        "start": {"dateTime": appt.start, "timeZone": "Europe/Berlin"},
        "end": {"dateTime": appt.end, "timeZone": "Europe/Berlin"},
    }

    created = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return {"status": "success", "event_id": created.get("id")}
