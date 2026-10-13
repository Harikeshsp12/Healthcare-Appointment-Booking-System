import pytest


def test_book_appointment_success(client):
    """Test booking an appointment within working hours."""
    doc = client.post("/doctors/", json={
        "name": "Dr. Appt Test",
        "specialization": "Oncology",
        "start_hour": 9,
        "end_hour": 17
    }).json()

    appt_payload = {
        "doctor_id": doc["id"],
        "patient_name": "John Doe",
        "slot": "2026-10-20T10:00:00"
    }
    response = client.post("/appointments/", json=appt_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["doctor_id"] == doc["id"]
    assert data["patient_name"] == "John Doe"
    assert "2026-10-20T10:00:00" in data["slot"]


def test_cancel_appointment_success(client):
    """Test cancelling an existing appointment."""
    doc = client.post("/doctors/", json={
        "name": "Dr. Cancel Test",
        "specialization": "Urology",
        "start_hour": 8,
        "end_hour": 14
    }).json()

    appt = client.post("/appointments/", json={
        "doctor_id": doc["id"],
        "patient_name": "Bob Smith",
        "slot": "2026-10-20T09:00:00"
    }).json()

    appt_id = appt["id"]
    del_response = client.delete(f"/appointments/{appt_id}")
    assert del_response.status_code == 200
    assert del_response.json()["id"] == appt_id

    # Verify appointment is deleted
    get_res = client.get(f"/appointments/{appt_id}")
    assert get_res.status_code == 404


def test_cancel_nonexistent_appointment(client):
    """Test cancelling non-existent appointment returns 404."""
    response = client.delete("/appointments/99999")
    assert response.status_code == 404


def test_list_appointments(client):
    """Test listing and filtering appointments."""
    doc = client.post("/doctors/", json={
        "name": "Dr. Filter Test",
        "specialization": "Radiology",
        "start_hour": 9,
        "end_hour": 17
    }).json()

    client.post("/appointments/", json={"doctor_id": doc["id"], "patient_name": "Charlie", "slot": "2026-10-20T10:00:00"})
    client.post("/appointments/", json={"doctor_id": doc["id"], "patient_name": "Daisy", "slot": "2026-10-20T11:00:00"})

    response = client.get("/appointments/")
    assert response.status_code == 200
    assert len(response.json()) == 2

    filtered = client.get(f"/appointments/?patient_name=Charlie")
    assert filtered.status_code == 200
    assert len(filtered.json()) == 1
    assert filtered.json()[0]["patient_name"] == "Charlie"
