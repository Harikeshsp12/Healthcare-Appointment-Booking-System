import React, { useState } from 'react';
import { api } from '../api';

export default function AddDoctorModal({ isOpen, onClose, onDoctorAdded }) {
  const [name, setName] = useState('');
  const [specialization, setSpecialization] = useState('');
  const [startHour, setStartHour] = useState(9);
  const [endHour, setEndHour] = useState(17);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const start = Number(startHour);
    const end = Number(endHour);

    if (!name.trim()) {
      setError('Please provide the doctor’s name.');
      return;
    }
    if (!specialization.trim()) {
      setError('Please enter the doctor’s specialization.');
      return;
    }
    if (start >= end) {
      setError('Shift start hour must be strictly earlier than end hour.');
      return;
    }
    if (start < 0 || start > 23 || end < 1 || end > 24) {
      setError('Hours must be within 0 to 24.');
      return;
    }

    try {
      setSubmitting(true);
      const doctorData = {
        name: name.trim(),
        specialization: specialization.trim(),
        start_hour: start,
        end_hour: end,
      };
      const res = await api.addDoctor(doctorData);
      onDoctorAdded(res);
      onClose();
      // Reset form
      setName('');
      setSpecialization('');
      setStartHour(9);
      setEndHour(17);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add doctor. Check input values.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3 className="modal-title">👨‍⚕️ Add New Doctor</h3>
          <button className="modal-close" onClick={onClose}>
            ✕
          </button>
        </div>

        {error && (
          <div style={{ marginBottom: '16px', padding: '12px', background: 'rgba(244, 63, 94, 0.15)', borderRadius: 'var(--radius-sm)', color: '#fb7185', fontSize: '13px' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group" style={{ marginBottom: '14px' }}>
            <label className="form-label">Full Name</label>
            <input
              type="text"
              className="form-input"
              placeholder="e.g. Dr. Emily Thorne"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>

          <div className="form-group" style={{ marginBottom: '14px' }}>
            <label className="form-label">Specialization</label>
            <input
              type="text"
              className="form-input"
              placeholder="e.g. Cardiology, Pediatrics"
              value={specialization}
              onChange={(e) => setSpecialization(e.target.value)}
              required
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '20px' }}>
            <div className="form-group">
              <label className="form-label">Shift Start Hour (24h)</label>
              <select
                className="form-select"
                value={startHour}
                onChange={(e) => setStartHour(Number(e.target.value))}
              >
                {Array.from({ length: 24 }).map((_, i) => (
                  <option key={i} value={i}>
                    {String(i).padStart(2, '0')}:00
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Shift End Hour (24h)</label>
              <select
                className="form-select"
                value={endHour}
                onChange={(e) => setEndHour(Number(e.target.value))}
              >
                {Array.from({ length: 24 }).map((_, i) => {
                  const hour = i + 1;
                  return (
                    <option key={hour} value={hour}>
                      {String(hour).padStart(2, '0')}:00
                    </option>
                  );
                })}
              </select>
            </div>
          </div>

          <div className="modal-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose} disabled={submitting}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Registering...' : 'Register Doctor'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
