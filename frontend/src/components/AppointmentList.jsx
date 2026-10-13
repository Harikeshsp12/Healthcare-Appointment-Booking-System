import React, { useState } from 'react';

export default function AppointmentList({
  appointments,
  doctors,
  onCancelAppointment,
  onOpenBookModal,
  loading
}) {
  const [filterText, setFilterText] = useState('');
  const [selectedDoctorFilter, setSelectedDoctorFilter] = useState('');

  const doctorMap = React.useMemo(() => {
    const map = {};
    doctors.forEach((d) => {
      map[d.id] = d;
    });
    return map;
  }, [doctors]);

  const filteredAppointments = appointments.filter((appt) => {
    const matchesPatient = appt.patient_name
      .toLowerCase()
      .includes(filterText.toLowerCase());

    const matchesDoctor = selectedDoctorFilter
      ? appt.doctor_id === Number(selectedDoctorFilter)
      : true;

    return matchesPatient && matchesDoctor;
  });

  const formatSlot = (isoString) => {
    try {
      const dt = new Date(isoString);
      return dt.toLocaleString('en-US', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false,
      });
    } catch {
      return isoString;
    }
  };

  return (
    <div>
      <div className="section-header">
        <div>
          <h2 className="section-title">Patient Appointments Schedule</h2>
          <p className="section-desc">
            Overview of confirmed consultations. Filter by patient or doctor, or cancel existing appointments.
          </p>
        </div>
        <button className="btn btn-primary" onClick={() => onOpenBookModal()}>
          <span>+</span> New Appointment
        </button>
      </div>

      <div style={{ display: 'flex', gap: '16px', marginBottom: '20px', flexWrap: 'wrap' }}>
        <input
          type="text"
          className="form-input"
          style={{ minWidth: '240px' }}
          placeholder="🔍 Search by patient name..."
          value={filterText}
          onChange={(e) => setFilterText(e.target.value)}
        />

        <select
          className="form-select"
          style={{ minWidth: '200px' }}
          value={selectedDoctorFilter}
          onChange={(e) => setSelectedDoctorFilter(e.target.value)}
        >
          <option value="">All Doctors</option>
          {doctors.map((d) => (
            <option key={d.id} value={d.id}>
              {d.name} ({d.specialization})
            </option>
          ))}
        </select>
      </div>

      <div className="table-card">
        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
            Loading appointments...
          </div>
        ) : filteredAppointments.length === 0 ? (
          <div style={{ padding: '50px 20px', textAlign: 'center' }}>
            <div style={{ fontSize: '32px', marginBottom: '10px' }}>🗓️</div>
            <h3 style={{ fontSize: '16px', color: 'var(--text-primary)', marginBottom: '6px' }}>
              No appointments found
            </h3>
            <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
              {filterText || selectedDoctorFilter
                ? 'Try adjusting your search criteria.'
                : 'No appointments have been booked yet. Click "New Appointment" to schedule one.'}
            </p>
          </div>
        ) : (
          <table className="custom-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Patient Name</th>
                <th>Doctor</th>
                <th>Specialization</th>
                <th>Scheduled Slot</th>
                <th>Status</th>
                <th style={{ textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredAppointments.map((appt) => {
                const doctor = doctorMap[appt.doctor_id] || {
                  name: `Doctor #${appt.doctor_id}`,
                  specialization: 'General',
                };
                return (
                  <tr key={appt.id}>
                    <td>#{appt.id}</td>
                    <td className="patient-highlight">👤 {appt.patient_name}</td>
                    <td>{doctor.name}</td>
                    <td>
                      <span className="doctor-specialty">{doctor.specialization}</span>
                    </td>
                    <td style={{ fontWeight: '600', color: 'var(--accent-teal)' }}>
                      🕒 {formatSlot(appt.slot)}
                    </td>
                    <td>
                      <span
                        style={{
                          fontSize: '11px',
                          fontWeight: '700',
                          padding: '3px 8px',
                          borderRadius: 'var(--radius-full)',
                          background: 'rgba(16, 185, 129, 0.15)',
                          color: '#34d399',
                        }}
                      >
                        CONFIRMED
                      </span>
                    </td>
                    <td style={{ textAlign: 'right' }}>
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={() => onCancelAppointment(appt.id)}
                        title="Cancel this appointment"
                      >
                        Cancel
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
