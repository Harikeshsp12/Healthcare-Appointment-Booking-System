from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict


class DoctorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Doctor's full name", examples=["Dr. Alice Smith"])
    specialization: str = Field(..., min_length=1, max_length=100, description="Medical specialization", examples=["Cardiology"])
    start_hour: int = Field(..., ge=0, le=23, description="Shift start hour (0-23)", examples=[9])
    end_hour: int = Field(..., ge=1, le=24, description="Shift end hour (1-24)", examples=[17])

    @field_validator("end_hour")
    @classmethod
    def validate_hours(cls, v: int, info) -> int:
        start = info.data.get("start_hour")
        if start is not None and v <= start:
            raise ValueError("end_hour must be strictly greater than start_hour")
        return v


class DoctorCreate(DoctorBase):
    pass


class DoctorResponse(DoctorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AppointmentBase(BaseModel):
    doctor_id: int = Field(..., description="ID of the doctor", examples=[1])
    patient_name: str = Field(..., min_length=1, max_length=100, description="Patient's full name", examples=["John Doe"])
    slot: datetime = Field(..., description="Appointment slot timestamp in ISO format", examples=["2026-10-15T10:00:00"])


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    patient_name: str
    slot: datetime

    model_config = ConfigDict(from_attributes=True)


class SlotAvailability(BaseModel):
    time: str = Field(..., description="Time string formatted as HH:00", examples=["10:00"])
    slot_datetime: datetime = Field(..., description="Full datetime timestamp of slot")
    is_available: bool = Field(..., description="True if slot is free for booking, False if booked")


class DoctorAvailabilityResponse(BaseModel):
    doctor_id: int
    doctor_name: str
    specialization: str
    date: str
    working_hours: str
    slots: List[SlotAvailability]


class MessageResponse(BaseModel):
    message: str
    id: Optional[int] = None


class DoctorStats(BaseModel):
    doctor_id: int
    doctor_name: str
    specialization: str
    appointment_count: int


class DashboardStatsResponse(BaseModel):
    total_doctors: int
    total_appointments: int
    upcoming_appointments: int
    doctor_stats: List[DoctorStats]
