import pytest


def test_create_doctor_success(client):
    """Test creating a doctor with valid details."""
    payload = {
        "name": "Dr. Sarah Connor",
        "specialization": "Neurology",
        "start_hour": 9,
        "end_hour": 17
    }
    response = client.post("/doctors/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Dr. Sarah Connor"
    assert data["specialization"] == "Neurology"
    assert data["start_hour"] == 9
    assert data["end_hour"] == 17


def test_create_doctor_invalid_hours(client):
    """Test start_hour >= end_hour is rejected."""
    payload = {
        "name": "Dr. Invalid Hours",
        "specialization": "General",
        "start_hour": 16,
        "end_hour": 9
    }
    response = client.post("/doctors/", json=payload)
    assert response.status_code in (400, 422)


def test_create_doctor_equal_hours(client):
    """Test start_hour == end_hour is rejected."""
    payload = {
        "name": "Dr. Zero Hours",
        "specialization": "General",
        "start_hour": 10,
        "end_hour": 10
    }
    response = client.post("/doctors/", json=payload)
    assert response.status_code in (400, 422)


def test_list_doctors(client):
    """Test listing all doctors."""
    client.post("/doctors/", json={"name": "Dr. Alpha", "specialization": "Cardiology", "start_hour": 8, "end_hour": 14})
    client.post("/doctors/", json={"name": "Dr. Beta", "specialization": "Dermatology", "start_hour": 10, "end_hour": 18})

    response = client.get("/doctors/")
    assert response.status_code == 200
    doctors = response.json()
    assert len(doctors) == 2
    assert doctors[0]["name"] == "Dr. Alpha"
    assert doctors[1]["name"] == "Dr. Beta"


def test_get_doctor_by_id_found(client):
    """Test retrieving existing doctor by ID."""
    created = client.post("/doctors/", json={"name": "Dr. Gamma", "specialization": "Pediatrics", "start_hour": 9, "end_hour": 15}).json()
    doc_id = created["id"]

    response = client.get(f"/doctors/{doc_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Dr. Gamma"


def test_get_doctor_by_id_not_found(client):
    """Test retrieving non-existent doctor returns 404."""
    response = client.get("/doctors/99999")
    assert response.status_code == 404


def test_doctor_availability_slots(client):
    """Test doctor availability returns correct working hour slots."""
    doc = client.post("/doctors/", json={"name": "Dr. Slot Test", "specialization": "ENT", "start_hour": 9, "end_hour": 12}).json()
    doc_id = doc["id"]

    # Check availability for date
    response = client.get(f"/doctors/{doc_id}/availability?query_date=2026-10-15")
    assert response.status_code == 200
    data = response.json()
    assert data["doctor_id"] == doc_id
    assert len(data["slots"]) == 3  # 9:00, 10:00, 11:00
    assert all(s["is_available"] is True for s in data["slots"])
    assert data["slots"][0]["time"] == "09:00"
    assert data["slots"][1]["time"] == "10:00"
    assert data["slots"][2]["time"] == "11:00"

    # Book slot at 10:00
    client.post("/appointments/", json={
        "doctor_id": doc_id,
        "patient_name": "Alice",
        "slot": "2026-10-15T10:00:00"
    })

    # Re-check availability
    response2 = client.get(f"/doctors/{doc_id}/availability?query_date=2026-10-15")
    slots = response2.json()["slots"]
    assert slots[0]["is_available"] is True   # 09:00
    assert slots[1]["is_available"] is False  # 10:00 is booked
    assert slots[2]["is_available"] is True   # 11:00


def test_update_doctor_success(client):
    """Test updating doctor name, specialty, and shift hours."""
    created = client.post("/doctors/", json={
        "name": "Dr. Original",
        "specialization": "General",
        "start_hour": 9,
        "end_hour": 17
    }).json()
    doc_id = created["id"]

    update_payload = {
        "name": "Dr. Updated",
        "specialization": "Cardiology",
        "start_hour": 10,
        "end_hour": 18
    }
    response = client.put(f"/doctors/{doc_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Dr. Updated"
    assert data["specialization"] == "Cardiology"
    assert data["start_hour"] == 10
    assert data["end_hour"] == 18


def test_delete_doctor_cascade(client):
    """Test deleting doctor removes doctor and their appointments."""
    doc = client.post("/doctors/", json={
        "name": "Dr. To Delete",
        "specialization": "Neurology",
        "start_hour": 9,
        "end_hour": 17
    }).json()
    doc_id = doc["id"]

    # Book an appointment
    appt = client.post("/appointments/", json={
        "doctor_id": doc_id,
        "patient_name": "Test Patient",
        "slot": "2026-10-15T10:00:00"
    }).json()
    appt_id = appt["id"]

    # Delete doctor
    del_res = client.delete(f"/doctors/{doc_id}")
    assert del_res.status_code == 200

    # Verify doctor is gone
    assert client.get(f"/doctors/{doc_id}").status_code == 404

    # Verify appointment was cascade deleted
    assert client.get(f"/appointments/{appt_id}").status_code == 404

