from datetime import datetime
from pydantic import BaseModel



class Reminder(BaseModel):
    time: datetime
    message: str

class ScanInput(BaseModel):
    barcode: str
