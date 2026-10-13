from datetime import datetime, date, time
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Doctor, Appointment
from app.schemas import (
    DoctorCreate,
    DoctorResponse,
    DoctorAvailabilityResponse,
    SlotAvailability,
    MessageResponse,
)
from app.websocket import ws_manager

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED, operation_id="add_doctor")
async def add_doctor(doctor_in: DoctorCreate, db: Session = Depends(get_db)):
    """Add a new doctor with their working hours."""
    if doctor_in.start_hour >= doctor_in.end_hour:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_hour must be strictly less than end_hour."
        )
    if not (0 <= doctor_in.start_hour < 24 and 1 <= doctor_in.end_hour <= 24):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hours must be within 0-24 range."
        )

    doctor = Doctor(
        name=doctor_in.name.strip(),
        specialization=doctor_in.specialization.strip(),
        start_hour=doctor_in.start_hour,
        end_hour=doctor_in.end_hour,
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    # Real-time event notification
    await ws_manager.broadcast({
        "event": "doctor_added",
        "doctor": {
            "id": doctor.id,
            "name": doctor.name,
            "specialization": doctor.specialization,
            "start_hour": doctor.start_hour,
            "end_hour": doctor.end_hour,
        }
    })

    return doctor


@router.get("/", response_model=List[DoctorResponse], operation_id="list_doctors")
def list_doctors(db: Session = Depends(get_db)):
    """List all registered doctors."""
    return db.query(Doctor).order_by(Doctor.id).all()


@router.get("/{id}", response_model=DoctorResponse, operation_id="get_doctor_by_id")
def get_doctor_by_id(id: int, db: Session = Depends(get_db)):
    """Get doctor details by ID."""
    doctor = db.query(Doctor).filter(Doctor.id == id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor with ID {id} not found."
        )
    return doctor


@router.put("/{id}", response_model=DoctorResponse, operation_id="update_doctor")
async def update_doctor(id: int, doctor_in: DoctorCreate, db: Session = Depends(get_db)):
    """Update doctor details and shift working hours."""
    doctor = db.query(Doctor).filter(Doctor.id == id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor with ID {id} not found."
        )
    if doctor_in.start_hour >= doctor_in.end_hour:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_hour must be strictly less than end_hour."
        )

    doctor.name = doctor_in.name.strip()
    doctor.specialization = doctor_in.specialization.strip()
    doctor.start_hour = doctor_in.start_hour
    doctor.end_hour = doctor_in.end_hour

    db.commit()
    db.refresh(doctor)

    await ws_manager.broadcast({
        "event": "doctor_updated",
        "doctor": {
            "id": doctor.id,
            "name": doctor.name,
            "specialization": doctor.specialization,
            "start_hour": doctor.start_hour,
            "end_hour": doctor.end_hour,
        }
    })
    return doctor


@router.delete("/{id}", response_model=MessageResponse, operation_id="delete_doctor")
async def delete_doctor(id: int, db: Session = Depends(get_db)):
    """Delete a doctor and their scheduled appointments."""
    doctor = db.query(Doctor).filter(Doctor.id == id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor with ID {id} not found."
        )

    doc_name = doctor.name
    db.delete(doctor)
    db.commit()

    await ws_manager.broadcast({
        "event": "doctor_deleted",
        "doctor_id": id,
        "doctor_name": doc_name
    })

    return MessageResponse(
        message=f"Doctor '{doc_name}' (ID: {id}) and associated appointments removed successfully.",
        id=id
    )


@router.get("/{id}/availability", response_model=DoctorAvailabilityResponse, operation_id="get_doctor_availability")
def get_doctor_availability(
    id: int,
    query_date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format, defaults to today"),
    db: Session = Depends(get_db)
):
    """Get all 1-hour time slots and their availability for a specific doctor on a chosen date."""
    doctor = db.query(Doctor).filter(Doctor.id == id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor with ID {id} not found."
        )

    # Parse date
    if query_date:
        try:
            target_date = datetime.strptime(query_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Expected YYYY-MM-DD."
            )
    else:
        target_date = date.today()

    # Query all appointments for this doctor on the selected date
    day_start = datetime.combine(target_date, time.min)
    day_end = datetime.combine(target_date, time.max)
    existing_appointments = db.query(Appointment).filter(
        Appointment.doctor_id == id,
        Appointment.slot >= day_start,
        Appointment.slot <= day_end
    ).all()

    booked_hours = {appt.slot.hour for appt in existing_appointments}

    slots: List[SlotAvailability] = []
    for hour in range(doctor.start_hour, doctor.end_hour):
        slot_dt = datetime.combine(target_date, time(hour=hour, minute=0, second=0))
        is_free = hour not in booked_hours
        slots.append(
            SlotAvailability(
                time=f"{hour:02d}:00",
                slot_datetime=slot_dt,
                is_available=is_free
            )
        )

    return DoctorAvailabilityResponse(
        doctor_id=doctor.id,
        doctor_name=doctor.name,
        specialization=doctor.specialization,
        date=target_date.strftime("%Y-%m-%d"),
        working_hours=f"{doctor.start_hour:02d}:00 - {doctor.end_hour:02d}:00",
        slots=slots
    )
