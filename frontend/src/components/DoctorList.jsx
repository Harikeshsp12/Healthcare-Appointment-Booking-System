import React from 'react';

export default function DoctorList({ doctors, onSelectDoctor, onOpenBookModal }) {
  return (
    <div style={{ marginTop: '20px' }}>
      <div className="section-header">
        <div>
          <h2 className="section-title">Directory of Medical Specialists</h2>
          <p className="section-desc">
            Browse our licensed physicians, their medical specialties, and designated daily consulting hours.
          </p>
        </div>
      </div>

      <div className="doctors-grid">
        {doctors.map((doctor) => {
          const initials = doctor.name
            .replace(/^Dr\.\s*/i, '')
            .split(' ')
            .map((n) => n[0])
            .join('')
            .toUpperCase()
            .slice(0, 2);

          const startStr = String(doctor.start_hour).padStart(2, '0') + ':00';
          const endStr = String(doctor.end_hour).padStart(2, '0') + ':00';

          return (
            <div key={doctor.id} className="doctor-card">
              <div>
                <div className="doctor-card-header">
                  <div className="doctor-avatar">{initials || 'DR'}</div>
                  <div>
                    <h3 className="doctor-name">{doctor.name}</h3>
                    <span className="doctor-specialty">{doctor.specialization}</span>
                  </div>
                </div>

                <div className="doctor-meta">
                  <div>
                    <div className="meta-label">Working Hours</div>
                    <div className="meta-value">{startStr} – {endStr}</div>
                  </div>
                  <div>
                    <div className="meta-label">Shift Duration</div>
                    <div className="meta-value">{doctor.end_hour - doctor.start_hour} hrs/day</div>
                  </div>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '10px' }}>
                <button
                  className="btn btn-secondary btn-sm"
                  style={{ flex: 1 }}
                  onClick={() => onSelectDoctor(doctor.id)}
                >
                  📅 View Slots
                </button>
                <button
                  className="btn btn-primary btn-sm"
                  style={{ flex: 1 }}
                  onClick={() => onOpenBookModal(doctor.id)}
                >
                  ⚡ Book Now
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
