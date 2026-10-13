import React, { useState, useEffect } from 'react';
import { api } from '../api';

export default function DoctorAvailability({
  doctors,
  selectedDoctorId,
  onSelectDoctor,
  onSelectSlotToBook,
  refreshTrigger
}) {
  const todayStr = new Date().toISOString().split('T')[0];
  const [selectedDate, setSelectedDate] = useState(todayStr);
  const [availability, setAvailability] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!selectedDoctorId && doctors.length > 0) {
      onSelectDoctor(doctors[0].id);
    }
  }, [doctors, selectedDoctorId]);

  useEffect(() => {
    if (selectedDoctorId) {
      fetchAvailability(selectedDoctorId, selectedDate);
    }
  }, [selectedDoctorId, selectedDate, refreshTrigger]);

  const fetchAvailability = async (docId, date) => {
    try {
      setLoading(true);
      setError('');
      const data = await api.getDoctorAvailability(docId, date);
      setAvailability(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch doctor availability.');
      setAvailability(null);
    } finally {
      setLoading(false);
    }
  };

  const currentDoctor = doctors.find((d) => d.id === Number(selectedDoctorId));

  return (
    <div className="availability-container">
      <div className="section-header">
        <div>
          <h2 className="section-title">Doctor Schedule & Slot Availability</h2>
          <p className="section-desc">
            Select a specialist and date to inspect available consultation slots in real-time.
          </p>
        </div>
      </div>

      <div className="availability-controls">
        <div className="form-group" style={{ minWidth: '240px' }}>
          <label className="form-label">Select Doctor</label>
          <select
            className="form-select"
            value={selectedDoctorId || ''}
            onChange={(e) => onSelectDoctor(Number(e.target.value))}
          >
            {doctors.map((d) => (
              <option key={d.id} value={d.id}>
                {d.name} ({d.specialization}) — {d.start_hour}:00 to {d.end_hour}:00
              </option>
            ))}
          </select>
        </div>

        <div className="form-group" style={{ minWidth: '180px' }}>
          <label className="form-label">Consultation Date</label>
          <input
            type="date"
            className="form-input"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
          />
        </div>

        {currentDoctor && (
          <div style={{ marginLeft: 'auto', display: 'flex', gap: '20px', alignItems: 'center' }}>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Working Shift</div>
              <div style={{ fontSize: '14px', fontWeight: '700', color: 'var(--accent-teal)' }}>
                {String(currentDoctor.start_hour).padStart(2, '0')}:00 – {String(currentDoctor.end_hour).padStart(2, '0')}:00
              </div>
            </div>
          </div>
        )}
      </div>

      {loading && (
        <div style={{ padding: '30px', textAlign: 'center', color: 'var(--text-muted)' }}>
          Checking calendar slots...
        </div>
      )}

      {error && (
        <div style={{ padding: '16px', background: 'rgba(244, 63, 94, 0.15)', borderRadius: 'var(--radius-sm)', color: '#fb7185' }}>
          {error}
        </div>
      )}

      {!loading && availability && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
            <div style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text-secondary)' }}>
              Slots for <span style={{ color: 'var(--text-primary)' }}>{availability.date}</span>:
            </div>
            <div style={{ display: 'flex', gap: '14px', fontSize: '12px' }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#34d399' }}>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#34d399' }}></span> Available (Click to book)
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#fb7185' }}>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#fb7185' }}></span> Booked
              </span>
            </div>
          </div>

          <div className="slots-grid">
            {availability.slots.map((s, idx) => (
              <div
                key={idx}
                className={`slot-pill ${s.is_available ? 'available' : 'booked'}`}
                onClick={() => {
                  if (s.is_available) {
                    onSelectSlotToBook({
                      doctorId: availability.doctor_id,
                      doctorName: availability.doctor_name,
                      slotDatetime: s.slot_datetime,
                      timeStr: s.time
                    });
                  }
                }}
                title={s.is_available ? `Book slot at ${s.time}` : `Slot ${s.time} is already booked`}
              >
                <span className="slot-time">{s.time}</span>
                <span className="slot-badge">{s.is_available ? 'Free' : 'Booked'}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
