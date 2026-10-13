from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Doctor, Appointment
from app.schemas import (
    AppointmentCreate,
    AppointmentResponse,
    MessageResponse,
    DashboardStatsResponse,
    DoctorStats,
)
from app.websocket import ws_manager

router = APIRouter(tags=["appointments"])


@router.post(
    "/appointments/",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="book_appointment"
)
async def book_appointment(appt_in: AppointmentCreate, db: Session = Depends(get_db)):
    """
    Book an appointment with a doctor.
    Enforces:
    1. Doctor must exist.
    2. Appointment slot must be within the doctor's working hours.
    3. Doctor cannot be double-booked for the same time slot.
    """
    # 1. Verify doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == appt_in.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor with ID {appt_in.doctor_id} does not exist."
        )

    # Normalize slot datetime (strip seconds and microseconds)
    slot_time = appt_in.slot.replace(second=0, microsecond=0)

    # 2. Trick Logic: Enforce appointments only within doctor's working hours
    slot_hour = slot_time.hour
    if slot_hour < doctor.start_hour or slot_hour >= doctor.end_hour:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Appointment slot {slot_hour:02d}:00 is outside doctor's working hours "
                f"({doctor.start_hour:02d}:00 - {doctor.end_hour:02d}:00)."
            )
        )

    # 3. Trick Logic: Prevent double-booking of same doctor/time slot
    existing = db.query(Appointment).filter(
        Appointment.doctor_id == appt_in.doctor_id,
        Appointment.slot == slot_time
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Dr. {doctor.name} already has an appointment booked at "
                f"{slot_time.strftime('%Y-%m-%d %H:%M')}."
            )
        )

    # Create new appointment
    appointment = Appointment(
        doctor_id=appt_in.doctor_id,
        patient_name=appt_in.patient_name.strip(),
        slot=slot_time
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    # Real-time event broadcast
    await ws_manager.broadcast({
        "event": "appointment_booked",
        "appointment": {
            "id": appointment.id,
            "doctor_id": appointment.doctor_id,
            "patient_name": appointment.patient_name,
            "slot": appointment.slot.isoformat(),
        }
    })

    return appointment


@router.delete(
    "/appointments/{id}",
    response_model=MessageResponse,
    operation_id="cancel_appointment"
)
async def cancel_appointment(id: int, db: Session = Depends(get_db)):
    """Cancel an existing appointment by ID."""
    appointment = db.query(Appointment).filter(Appointment.id == id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with ID {id} not found."
        )

    doctor_id = appointment.doctor_id
    slot_iso = appointment.slot.isoformat()
    db.delete(appointment)
    db.commit()

    # Real-time event broadcast
    await ws_manager.broadcast({
        "event": "appointment_cancelled",
        "appointment_id": id,
        "doctor_id": doctor_id,
        "slot": slot_iso
    })

    return MessageResponse(
        message=f"Appointment {id} cancelled successfully.",
        id=id
    )


@router.get(
    "/appointments/",
    response_model=List[AppointmentResponse],
    operation_id="list_appointments"
)
def list_appointments(
    doctor_id: Optional[int] = Query(None, description="Filter by doctor ID"),
    patient_name: Optional[str] = Query(None, description="Filter by patient name"),
    db: Session = Depends(get_db)
):
    """List all appointments with optional filters."""
    query = db.query(Appointment)
    if doctor_id is not None:
        query = query.filter(Appointment.doctor_id == doctor_id)
    if patient_name:
        query = query.filter(Appointment.patient_name.ilike(f"%{patient_name.strip()}%"))
    return query.order_by(Appointment.slot.asc()).all()


@router.get(
    "/appointments/{id}",
    response_model=AppointmentResponse,
    operation_id="get_appointment_by_id"
)
def get_appointment_by_id(id: int, db: Session = Depends(get_db)):
    """Get appointment by ID."""
    appointment = db.query(Appointment).filter(Appointment.id == id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with ID {id} not found."
        )
    return appointment


@router.get(
    "/stats",
    response_model=DashboardStatsResponse,
    tags=["analytics"],
    operation_id="get_dashboard_stats"
)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard analytics for doctors and appointments."""
    doctors = db.query(Doctor).all()
    appointments = db.query(Appointment).all()
    now = datetime.now()

    upcoming_count = sum(1 for a in appointments if a.slot >= now)

    doctor_stats_list = []
    for d in doctors:
        count = sum(1 for a in appointments if a.doctor_id == d.id)
        doctor_stats_list.append(DoctorStats(
            doctor_id=d.id,
            doctor_name=d.name,
            specialization=d.specialization,
            appointment_count=count
        ))

    return DashboardStatsResponse(
        total_doctors=len(doctors),
        total_appointments=len(appointments),
        upcoming_appointments=upcoming_count,
        doctor_stats=doctor_stats_list
    )
