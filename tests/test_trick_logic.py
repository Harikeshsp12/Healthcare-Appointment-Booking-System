import pytest


def test_trick_logic_double_booking_prevention(client):
    """
    Trick Logic Requirement:
    - Dr. A has 10:00 slot free -> booking success.
    - Dr. A already booked 10:00 -> reject.
    """
    # 1. Add Dr. A (working 9:00 - 17:00)
    dr_a = client.post("/doctors/", json={
        "name": "Dr. A",
        "specialization": "General Medicine",
        "start_hour": 9,
        "end_hour": 17
    }).json()
    dr_a_id = dr_a["id"]

    slot = "2026-10-15T10:00:00"

    # Step 1: 10:00 slot free -> booking success
    res1 = client.post("/appointments/", json={
        "doctor_id": dr_a_id,
        "patient_name": "Patient One",
        "slot": slot
    })
    assert res1.status_code == 201
    assert res1.json()["id"] is not None

    # Step 2: Dr. A already booked 10:00 -> reject (Conflict 409)
    res2 = client.post("/appointments/", json={
        "doctor_id": dr_a_id,
        "patient_name": "Patient Two",
        "slot": slot
    })
    assert res2.status_code == 409
    assert "already has an appointment booked" in res2.json()["detail"]


def test_trick_logic_working_hours_enforcement(client):
    """
    Trick Logic Requirement:
    - Enforce appointments only within working hours.
    - Doctor works 09:00 to 17:00.
    - 08:00 -> reject (before working hours)
    - 17:00 -> reject (doctor shift ends at 17:00, last 1-hour slot starts at 16:00)
    - 18:00 -> reject (after working hours)
    - 09:00 -> success
    - 16:00 -> success
    """
    dr = client.post("/doctors/", json={
        "name": "Dr. Schedule Test",
        "specialization": "Pediatrics",
        "start_hour": 9,
        "end_hour": 17
    }).json()
    dr_id = dr["id"]

    # Slot before start_hour (08:00) -> should be rejected
    res_before = client.post("/appointments/", json={
        "doctor_id": dr_id,
        "patient_name": "Early Bird",
        "slot": "2026-10-15T08:00:00"
    })
    assert res_before.status_code == 400
    assert "outside doctor's working hours" in res_before.json()["detail"]

    # Slot at end_hour (17:00) -> should be rejected (shift ends at 17:00)
    res_at_end = client.post("/appointments/", json={
        "doctor_id": dr_id,
        "patient_name": "Late Comer",
        "slot": "2026-10-15T17:00:00"
    })
    assert res_at_end.status_code == 400
    assert "outside doctor's working hours" in res_at_end.json()["detail"]

    # Slot after end_hour (18:00) -> should be rejected
    res_after = client.post("/appointments/", json={
        "doctor_id": dr_id,
        "patient_name": "Night Owl",
        "slot": "2026-10-15T18:00:00"
    })
    assert res_after.status_code == 400
    assert "outside doctor's working hours" in res_after.json()["detail"]

    # Valid slot at start_hour (09:00) -> should succeed
    res_start = client.post("/appointments/", json={
        "doctor_id": dr_id,
        "patient_name": "Morning Patient",
        "slot": "2026-10-15T09:00:00"
    })
    assert res_start.status_code == 201

    # Valid slot at last available hour (16:00) -> should succeed
    res_last = client.post("/appointments/", json={
        "doctor_id": dr_id,
        "patient_name": "Evening Patient",
        "slot": "2026-10-15T16:00:00"
    })
    assert res_last.status_code == 201


def test_different_doctors_can_book_same_time_slot(client):
    """
    Ensure double-booking check is per doctor:
    Dr. A and Dr. B can both have appointments at 10:00 without conflict.
    """
    dr_a = client.post("/doctors/", json={"name": "Dr. A", "specialization": "General", "start_hour": 9, "end_hour": 17}).json()
    dr_b = client.post("/doctors/", json={"name": "Dr. B", "specialization": "Dental", "start_hour": 9, "end_hour": 17}).json()

    slot = "2026-10-15T10:00:00"

    res_a = client.post("/appointments/", json={"doctor_id": dr_a["id"], "patient_name": "Patient 1", "slot": slot})
    assert res_a.status_code == 201

    res_b = client.post("/appointments/", json={"doctor_id": dr_b["id"], "patient_name": "Patient 2", "slot": slot})
    assert res_b.status_code == 201


def test_booking_reusable_after_cancellation(client):
    """
    Verify that if an appointment at 10:00 is cancelled, that slot becomes available again.
    """
    dr = client.post("/doctors/", json={"name": "Dr. Rebook", "specialization": "Cardiology", "start_hour": 9, "end_hour": 17}).json()
    slot = "2026-10-15T10:00:00"

    appt = client.post("/appointments/", json={"doctor_id": dr["id"], "patient_name": "First Patient", "slot": slot}).json()
    appt_id = appt["id"]

    # Trying to book again fails
    res_fail = client.post("/appointments/", json={"doctor_id": dr["id"], "patient_name": "Second Patient", "slot": slot})
    assert res_fail.status_code == 409

    # Cancel first appointment
    client.delete(f"/appointments/{appt_id}")

    # Now booking the same slot succeeds
    res_retry = client.post("/appointments/", json={"doctor_id": dr["id"], "patient_name": "Second Patient", "slot": slot})
    assert res_retry.status_code == 201


def test_appointment_with_nonexistent_doctor(client):
    """Attempting to book with a non-existent doctor must return 404."""
    response = client.post("/appointments/", json={
        "doctor_id": 99999,
        "patient_name": "Ghost Patient",
        "slot": "2026-10-15T10:00:00"
    })
    assert response.status_code == 404
    assert "does not exist" in response.json()["detail"]
