import React, { useState, useEffect, useCallback, useRef } from 'react';
import { api } from './api';
import './index.css';

// Helper function to format 24h hours to 12h format with AM/PM
function formatHour12(hour24) {
  const h = Number(hour24);
  if (h === 24) return '12:00 AM';
  const period = h >= 12 ? 'PM' : 'AM';
  const displayH = h % 12 === 0 ? 12 : h % 12;
  return `${displayH}:00 ${period}`;
}

export default function App() {
  const todayStr = new Date().toISOString().split('T')[0];

  // Core Data
  const [doctors, setDoctors] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [availability, setAvailability] = useState(null);

  // Availability & Booking State
  const [selectedDoctorId, setSelectedDoctorId] = useState('');
  const [selectedDate, setSelectedDate] = useState(todayStr);
  const [patientName, setPatientName] = useState('');
  const [selectedHour, setSelectedHour] = useState(10);

  // Add Doctor Form State
  const [newDocName, setNewDocName] = useState('');
  const [newDocSpec, setNewDocSpec] = useState('');
  const [newDocStart, setNewDocStart] = useState(9);
  const [newDocEnd, setNewDocEnd] = useState(17);
  const [showAddDoctor, setShowAddDoctor] = useState(false);

  // Edit Doctor Form State
  const [editingDoctor, setEditingDoctor] = useState(null);
  const [editDocName, setEditDocName] = useState('');
  const [editDocSpec, setEditDocSpec] = useState('');
  const [editDocStart, setEditDocStart] = useState(9);
  const [editDocEnd, setEditDocEnd] = useState(17);

  // Status & Feedback
  const [statusMessage, setStatusMessage] = useState({ text: '', type: '' });
  const [wsConnected, setWsConnected] = useState(false);
  const [loading, setLoading] = useState(false);
  const wsRef = useRef(null);

  const showFeedback = (text, type = 'success') => {
    setStatusMessage({ text, type });
    setTimeout(() => {
      setStatusMessage({ text: '', type: '' });
    }, 4500);
  };

  // Fetch Doctors and Appointments
  const loadInitialData = useCallback(async () => {
    try {
      setLoading(true);
      const [docs, appts] = await Promise.all([
        api.getDoctors(),
        api.getAppointments()
      ]);
      setDoctors(docs);
      setAppointments(appts);
      if (docs.length > 0 && !selectedDoctorId) {
        setSelectedDoctorId(docs[0].id);
      }
    } catch (err) {
      showFeedback('Failed to connect to backend server.', 'error');
    } finally {
      setLoading(false);
    }
  }, [selectedDoctorId]);

  // Fetch slot availability whenever doctor or date changes
  const fetchSlots = useCallback(async (docId, date) => {
    if (!docId) return;
    try {
      const data = await api.getDoctorAvailability(docId, date);
      setAvailability(data);
    } catch (err) {
      setAvailability(null);
    }
  }, []);

  useEffect(() => {
    loadInitialData();
  }, [loadInitialData]);

  useEffect(() => {
    if (selectedDoctorId && selectedDate) {
      fetchSlots(selectedDoctorId, selectedDate);
    }
  }, [selectedDoctorId, selectedDate, fetchSlots]);

  // Real-Time WebSocket for Live Updates
  useEffect(() => {
    let reconnectTimer = null;
    const connectWs = () => {
      try {
        const wsUrl = `ws://${window.location.hostname || 'localhost'}:8000/ws`;
        const socket = new WebSocket(wsUrl);
        wsRef.current = socket;

        socket.onopen = () => setWsConnected(true);
        socket.onmessage = (e) => {
          try {
            const data = JSON.parse(e.data);
            if (data.event === 'appointment_booked') {
              showFeedback(`Live update: New appointment booked!`, 'info');
              loadInitialData();
              if (selectedDoctorId) fetchSlots(selectedDoctorId, selectedDate);
            } else if (data.event === 'appointment_cancelled') {
              showFeedback(`Live update: Appointment #${data.appointment_id} cancelled.`, 'info');
              loadInitialData();
              if (selectedDoctorId) fetchSlots(selectedDoctorId, selectedDate);
            } else if (data.event === 'doctor_added') {
              showFeedback(`Live update: Dr. ${data.doctor?.name} was added.`, 'info');
              loadInitialData();
            } else if (data.event === 'doctor_updated') {
              showFeedback(`Live update: Dr. ${data.doctor?.name} was updated.`, 'info');
              loadInitialData();
              if (selectedDoctorId) fetchSlots(selectedDoctorId, selectedDate);
            } else if (data.event === 'doctor_deleted') {
              showFeedback(`Live update: Doctor #${data.doctor_id} was removed.`, 'info');
              loadInitialData();
            }
          } catch (err) {}
        };
        socket.onclose = () => {
          setWsConnected(false);
          reconnectTimer = setTimeout(connectWs, 3000);
        };
        socket.onerror = () => socket.close();
      } catch (err) {
        setWsConnected(false);
      }
    };

    connectWs();
    return () => {
      if (wsRef.current) wsRef.current.close();
      if (reconnectTimer) clearTimeout(reconnectTimer);
    };
  }, [loadInitialData, fetchSlots, selectedDoctorId, selectedDate]);

  // Handle Book Appointment
  const handleBook = async (e) => {
    e.preventDefault();
    if (!patientName.trim()) {
      showFeedback('Please enter the patient name.', 'error');
      return;
    }
    if (!selectedDoctorId) {
      showFeedback('Please select a doctor.', 'error');
      return;
    }

    const padHour = String(selectedHour).padStart(2, '0');
    const slotIso = `${selectedDate}T${padHour}:00:00`;

    try {
      await api.bookAppointment({
        doctor_id: Number(selectedDoctorId),
        patient_name: patientName.trim(),
        slot: slotIso
      });
      showFeedback(`Appointment booked for ${patientName} at ${formatHour12(selectedHour)}!`, 'success');
      setPatientName('');
      loadInitialData();
      fetchSlots(selectedDoctorId, selectedDate);
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to book appointment.';
      showFeedback(msg, 'error');
    }
  };

  // Handle Cancel Appointment
  const handleCancel = async (id) => {
    if (!window.confirm(`Cancel appointment #${id}?`)) return;
    try {
      await api.cancelAppointment(id);
      showFeedback(`Appointment #${id} cancelled.`, 'success');
      loadInitialData();
      if (selectedDoctorId) fetchSlots(selectedDoctorId, selectedDate);
    } catch (err) {
      showFeedback(err.response?.data?.detail || 'Cancellation failed.', 'error');
    }
  };

  // Handle Add Doctor
  const handleAddDoctor = async (e) => {
    e.preventDefault();
    if (!newDocName.trim() || !newDocSpec.trim()) {
      showFeedback('Please fill in doctor name and specialization.', 'error');
      return;
    }
    const start = Number(newDocStart);
    const end = Number(newDocEnd);
    if (start >= end) {
      showFeedback('Start hour must be earlier than end hour.', 'error');
      return;
    }

    try {
      await api.addDoctor({
        name: newDocName.trim(),
        specialization: newDocSpec.trim(),
        start_hour: start,
        end_hour: end
      });
      showFeedback(`Doctor ${newDocName} added successfully!`, 'success');
      setNewDocName('');
      setNewDocSpec('');
      setShowAddDoctor(false);
      loadInitialData();
    } catch (err) {
      showFeedback(err.response?.data?.detail || 'Failed to add doctor.', 'error');
    }
  };

  // Handle Start Edit Doctor
  const handleStartEdit = (doc) => {
    setEditingDoctor(doc);
    setEditDocName(doc.name);
    setEditDocSpec(doc.specialization);
    setEditDocStart(doc.start_hour);
    setEditDocEnd(doc.end_hour);
  };

  // Handle Save Edit Doctor
  const handleSaveEditDoctor = async (e) => {
    e.preventDefault();
    if (!editDocName.trim() || !editDocSpec.trim()) {
      showFeedback('Doctor name and specialization cannot be empty.', 'error');
      return;
    }
    const start = Number(editDocStart);
    const end = Number(editDocEnd);
    if (start >= end) {
      showFeedback('Shift start hour must be earlier than end hour.', 'error');
      return;
    }

    try {
      await api.updateDoctor(editingDoctor.id, {
        name: editDocName.trim(),
        specialization: editDocSpec.trim(),
        start_hour: start,
        end_hour: end
      });
      showFeedback(`Doctor ${editDocName} updated successfully!`, 'success');
      setEditingDoctor(null);
      loadInitialData();
      fetchSlots(editingDoctor.id, selectedDate);
    } catch (err) {
      showFeedback(err.response?.data?.detail || 'Failed to update doctor.', 'error');
    }
  };

  // Handle Delete Doctor
  const handleDeleteDoctor = async (id, name) => {
    if (!window.confirm(`Are you sure you want to remove ${name}?\n\nNote: All scheduled appointments for this doctor will also be removed.`)) {
      return;
    }
    try {
      await api.deleteDoctor(id);
      showFeedback(`Doctor ${name} removed successfully.`, 'success');
      setEditingDoctor(null);
      const remaining = doctors.filter((d) => d.id !== id);
      if (remaining.length > 0) {
        setSelectedDoctorId(remaining[0].id);
      } else {
        setSelectedDoctorId('');
        setAvailability(null);
      }
      loadInitialData();
    } catch (err) {
      showFeedback(err.response?.data?.detail || 'Failed to delete doctor.', 'error');
    }
  };

  const currentDoctor = doctors.find((d) => d.id === Number(selectedDoctorId));

  return (
    <div className="simple-app">
      {/* Top Header */}
      <header className="simple-header">
        <div className="header-left">
          <h1>🏥 Healthcare Appointment System</h1>
          <p>Book and manage patient appointments with doctors</p>
        </div>
        <div className="header-right">
          <span className={`sync-pill ${wsConnected ? 'active' : ''}`}>
            ● {wsConnected ? 'Live Real-Time Active' : 'Offline'}
          </span>
          <button
            className="btn-toggle"
            onClick={() => setShowAddDoctor(!showAddDoctor)}
          >
            {showAddDoctor ? '✕ Close Add Doctor' : '+ Add New Doctor'}
          </button>
        </div>
      </header>

      {/* Global Status Message */}
      {statusMessage.text && (
        <div className={`simple-banner ${statusMessage.type}`}>
          {statusMessage.type === 'error' ? '⚠️ ' : '✅ '}
          {statusMessage.text}
        </div>
      )}

      {/* Add Doctor Collapsible Form */}
      {showAddDoctor && (
        <div className="panel add-doctor-panel">
          <h2>👨‍⚕️ Add New Doctor</h2>
          <form onSubmit={handleAddDoctor} className="form-inline">
            <input
              type="text"
              placeholder="Doctor Name (e.g. Dr. Jane Smith)"
              value={newDocName}
              onChange={(e) => setNewDocName(e.target.value)}
              required
            />
            <input
              type="text"
              placeholder="Specialization (e.g. Cardiology)"
              value={newDocSpec}
              onChange={(e) => setNewDocSpec(e.target.value)}
              required
            />
            <div className="hour-selects">
              <label>Shift:</label>
              <select value={newDocStart} onChange={(e) => setNewDocStart(e.target.value)}>
                {Array.from({ length: 24 }).map((_, i) => (
                  <option key={i} value={i}>{formatHour12(i)}</option>
                ))}
              </select>
              <span>to</span>
              <select value={newDocEnd} onChange={(e) => setNewDocEnd(e.target.value)}>
                {Array.from({ length: 24 }).map((_, i) => {
                  const h = i + 1;
                  return <option key={h} value={h}>{formatHour12(h)}</option>;
                })}
              </select>
            </div>
            <button type="submit" className="btn-save">Save Doctor</button>
          </form>
        </div>
      )}

      {/* Main Two-Column Layout */}
      <main className="simple-grid">
        {/* LEFT COLUMN: Doctor Availability & Booking */}
        <section className="panel">
          <h2>1. Select Doctor & View Available Slots</h2>

          <div className="row-controls">
            <div className="control-group">
              <label>Doctor:</label>
              <select
                value={selectedDoctorId}
                onChange={(e) => setSelectedDoctorId(e.target.value)}
              >
                {doctors.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.name} ({d.specialization}) — [{formatHour12(d.start_hour)} to {formatHour12(d.end_hour)}]
                  </option>
                ))}
              </select>
            </div>

            <div className="control-group">
              <label>Date:</label>
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
              />
            </div>
          </div>

          {currentDoctor && (
            <div className="doc-info-badge">
              <div>
                Working Shift: <strong>{formatHour12(currentDoctor.start_hour)} to {formatHour12(currentDoctor.end_hour)}</strong>
              </div>
              <div className="doc-actions-wrap">
                <button
                  type="button"
                  className="btn-action-sm btn-edit"
                  onClick={() => handleStartEdit(currentDoctor)}
                  title="Edit doctor name, specialty, or hours"
                >
                  ✏️ Edit
                </button>
                <button
                  type="button"
                  className="btn-action-sm btn-del"
                  onClick={() => handleDeleteDoctor(currentDoctor.id, currentDoctor.name)}
                  title="Delete doctor"
                >
                  🗑️ Delete
                </button>
              </div>
            </div>
          )}

          {/* Edit Doctor Inline Box */}
          {editingDoctor && (
            <div className="edit-doctor-box">
              <div className="edit-box-header">
                <strong>✏️ Editing: {editingDoctor.name}</strong>
                <button type="button" className="btn-close-edit" onClick={() => setEditingDoctor(null)}>✕ Cancel</button>
              </div>
              <form onSubmit={handleSaveEditDoctor} className="edit-form-grid">
                <input
                  type="text"
                  placeholder="Doctor Name"
                  value={editDocName}
                  onChange={(e) => setEditDocName(e.target.value)}
                  required
                />
                <input
                  type="text"
                  placeholder="Specialization"
                  value={editDocSpec}
                  onChange={(e) => setEditDocSpec(e.target.value)}
                  required
                />
                <div className="hour-selects">
                  <label>Shift:</label>
                  <select value={editDocStart} onChange={(e) => setEditDocStart(e.target.value)}>
                    {Array.from({ length: 24 }).map((_, i) => (
                      <option key={i} value={i}>{formatHour12(i)}</option>
                    ))}
                  </select>
                  <span>to</span>
                  <select value={editDocEnd} onChange={(e) => setEditDocEnd(e.target.value)}>
                    {Array.from({ length: 24 }).map((_, i) => {
                      const h = i + 1;
                      return <option key={h} value={h}>{formatHour12(h)}</option>;
                    })}
                  </select>
                </div>
                <button type="submit" className="btn-save">Save Changes</button>
              </form>
            </div>
          )}

          {/* Slots display */}
          <div className="slots-section">
            <p className="slots-hint">
              Click any green <strong>Free</strong> slot below to select it for booking:
            </p>
            {availability && availability.slots && (
              <div className="simple-slots-grid">
                {availability.slots.map((s, idx) => {
                  const hourNum = new Date(s.slot_datetime).getHours();
                  const isSelected = selectedHour === hourNum;
                  return (
                    <button
                      key={idx}
                      type="button"
                      disabled={!s.is_available}
                      className={`slot-box ${s.is_available ? 'free' : 'booked'} ${isSelected && s.is_available ? 'selected' : ''}`}
                      onClick={() => {
                        if (s.is_available) {
                          setSelectedHour(hourNum);
                        }
                      }}
                    >
                      <span className="slot-time">{formatHour12(hourNum)}</span>
                      <span className="slot-tag">{s.is_available ? 'Free' : 'Booked'}</span>
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          {/* Inline Booking Form */}
          <div className="booking-box">
            <h3>2. Book Appointment</h3>
            <form onSubmit={handleBook}>
              <div className="booking-fields">
                <input
                  type="text"
                  placeholder="Patient Full Name"
                  value={patientName}
                  onChange={(e) => setPatientName(e.target.value)}
                  required
                />
                <div className="selected-slot-preview">
                  Selected Time: <strong>{selectedDate} at {formatHour12(selectedHour)}</strong>
                </div>
                <button type="submit" className="btn-book">
                  Book Appointment Now
                </button>
              </div>
            </form>
          </div>
        </section>

        {/* RIGHT COLUMN: Appointments List */}
        <section className="panel">
          <h2>3. Booked Appointments ({appointments.length})</h2>
          <p className="panel-sub">All active appointments. Click "Cancel" to delete an appointment.</p>

          {appointments.length === 0 ? (
            <div className="empty-state">No appointments booked yet.</div>
          ) : (
            <div className="table-wrapper">
              <table className="simple-table">
                <thead>
                  <tr>
                    <th>Patient</th>
                    <th>Doctor</th>
                    <th>Slot (12-Hr Time)</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {appointments.map((a) => {
                    const doc = doctors.find((d) => d.id === a.doctor_id);
                    const formattedDate = new Date(a.slot).toLocaleString([], {
                      month: 'short',
                      day: 'numeric',
                      hour: 'numeric',
                      minute: '2-digit',
                      hour12: true
                    });
                    return (
                      <tr key={a.id}>
                        <td><strong>{a.patient_name}</strong></td>
                        <td>{doc ? doc.name : `Doctor #${a.doctor_id}`}</td>
                        <td><strong>{formattedDate}</strong></td>
                        <td>
                          <button
                            type="button"
                            className="btn-cancel"
                            onClick={() => handleCancel(a.id)}
                          >
                            Cancel
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
