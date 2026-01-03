from icalendar import Calendar
from datetime import datetime
import pytz
from functions.events import create_event

def import_ics(file, user):
    cal = Calendar.from_ical(file.read())
    tz = pytz.timezone(user["timezone"])

    for comp in cal.walk():
        if comp.name == "VEVENT":
            start = comp.decoded("DTSTART")
            end = comp.decoded("DTEND")

            create_event({
                "title": str(comp.get("SUMMARY", "Imported Event")),
                "subject": "Other",
                "description": str(comp.get("DESCRIPTION", "")),
                "start": tz.localize(start).isoformat(),
                "end": tz.localize(end).isoformat(),
                "timezone": user["timezone"],
                "created_by": user["username"],
                "is_private": 0,
                "recurrence": None,
                "subject_color": "#7f7f7f",
            })
