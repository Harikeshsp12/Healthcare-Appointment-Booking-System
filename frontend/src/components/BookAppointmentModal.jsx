import React, { useState, useEffect } from 'react';
import { api } from '../api';

export default function BookAppointmentModal({
  isOpen,
  onClose,
  doctors,
  prefilledSlot,
  initialDoctorId,
  onAppointmentBooked
}) {
  const [doctorId, setDoctorId] = useState('');
  const [patientName, setPatientName] = useState('');
  const [slotDate, setSlotDate] = useState('');
  const [slotHour, setSlotHour] = useState(10);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const todayStr = new Date().toISOString().split('T')[0];

  useEffect(() => {
    if (prefilledSlot) {
      setDoctorId(prefilledSlot.doctorId);
      const dt = new Date(prefilledSlot.slotDatetime);
      setSlotDate(dt.toISOString().split('T')[0]);
      setSlotHour(dt.getHours());
    } else {
      if (initialDoctorId) {
        setDoctorId(initialDoctorId);
      } else if (doctors.length > 0 && !doctorId) {
        setDoctorId(doctors[0].id);
      }
      setSlotDate(todayStr);
      setSlotHour(10);
    }
  }, [prefilledSlot, initialDoctorId, doctors, isOpen]);

  if (!isOpen) return null;

  const currentDoctor = doctors.find((d) => d.id === Number(doctorId));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!patientName.trim()) {
      setError('Please provide the patient’s full name.');
      return;
    }
    if (!doctorId) {
      setError('Please select a doctor.');
      return;
    }
    if (!slotDate) {
      setError('Please choose a consultation date.');
      return;
    }

    // Format ISO string with exact hour:00:00
    const padHour = String(slotHour).padStart(2, '0');
    const isoString = `${slotDate}T${padHour}:00:00`;

    try {
      setSubmitting(true);
      const payload = {
        doctor_id: Number(doctorId),
        patient_name: patientName.trim(),
        slot: isoString,
      };

      const result = await api.bookAppointment(payload);
      onAppointmentBooked(result);
      onClose();
      setPatientName('');
    } catch (err) {
      const detail = err.response?.data?.detail;
      if (typeof detail === 'string') {
        setError(detail);
      } else if (Array.isArray(detail)) {
        setError(detail.map((d) => d.msg).join(', '));
      } else {
        setError('Failed to book appointment. Please verify details.');
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3 className="modal-title">⚡ Book Appointment</h3>
          <button className="modal-close" onClick={onClose}>
            ✕
          </button>
        </div>

        {error && (
          <div
            style={{
              marginBottom: '16px',
              padding: '12px 14px',
              background: 'rgba(244, 63, 94, 0.15)',
              border: '1px solid rgba(244, 63, 94, 0.3)',
              borderRadius: 'var(--radius-sm)',
              color: '#fb7185',
              fontSize: '13px',
              lineHeight: 1.4,
            }}
          >
            <strong>Booking Notice:</strong> {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group" style={{ marginBottom: '14px' }}>
            <label className="form-label">Doctor / Specialist</label>
            <select
              className="form-select"
              value={doctorId}
              onChange={(e) => setDoctorId(Number(e.target.value))}
              required
            >
              {doctors.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.name} ({d.specialization}) — [{d.start_hour}:00 to {d.end_hour}:00]
                </option>
              ))}
            </select>
            {currentDoctor && (
              <div style={{ fontSize: '11.5px', color: 'var(--accent-teal)', marginTop: '4px' }}>
                ✓ Working hours: {currentDoctor.start_hour}:00 – {currentDoctor.end_hour}:00
              </div>
            )}
          </div>

          <div className="form-group" style={{ marginBottom: '14px' }}>
            <label className="form-label">Patient Name</label>
            <input
              type="text"
              className="form-input"
              placeholder="e.g. John Doe"
              value={patientName}
              onChange={(e) => setPatientName(e.target.value)}
              required
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 0.8fr', gap: '14px', marginBottom: '20px' }}>
            <div className="form-group">
              <label className="form-label">Consultation Date</label>
              <input
                type="date"
                className="form-input"
                value={slotDate}
                onChange={(e) => setSlotDate(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Time Slot (Hour)</label>
              <select
                className="form-select"
                value={slotHour}
                onChange={(e) => setSlotHour(Number(e.target.value))}
              >
                {Array.from({ length: 24 }).map((_, i) => (
                  <option key={i} value={i}>
                    {String(i).padStart(2, '0')}:00
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="modal-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose} disabled={submitting}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Confirming Slot...' : 'Confirm Appointment'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
