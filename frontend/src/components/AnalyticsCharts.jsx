import React from 'react';

export default function AnalyticsCharts({ stats }) {
  if (!stats) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
        Gathering analytics metrics...
      </div>
    );
  }

  const { total_doctors, total_appointments, upcoming_appointments, doctor_stats } = stats;

  const maxAppointments = Math.max(1, ...(doctor_stats || []).map((d) => d.appointment_count));

  return (
    <div>
      <div className="section-header">
        <div>
          <h2 className="section-title">Healthcare System Analytics & Insights</h2>
          <p className="section-desc">
            Operational dashboard tracking clinician caseloads, appointment volume, and booking distribution.
          </p>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-icon-wrap" style={{ color: 'var(--accent-blue)' }}>👨‍⚕️</div>
          <div>
            <div className="kpi-value">{total_doctors}</div>
            <div className="kpi-label">Registered Doctors</div>
          </div>
        </div>

        <div className="kpi-card emerald">
          <div className="kpi-icon-wrap" style={{ color: 'var(--accent-emerald)' }}>📅</div>
          <div>
            <div className="kpi-value">{total_appointments}</div>
            <div className="kpi-label">Total Appointments</div>
          </div>
        </div>

        <div className="kpi-card amber">
          <div className="kpi-icon-wrap" style={{ color: 'var(--accent-amber)' }}>⏳</div>
          <div>
            <div className="kpi-value">{upcoming_appointments}</div>
            <div className="kpi-label">Upcoming Sessions</div>
          </div>
        </div>

        <div className="kpi-card violet">
          <div className="kpi-icon-wrap" style={{ color: 'var(--accent-violet)' }}>⚡</div>
          <div>
            <div className="kpi-value">
              {total_doctors > 0 ? (total_appointments / total_doctors).toFixed(1) : '0'}
            </div>
            <div className="kpi-label">Avg Caseload / Doctor</div>
          </div>
        </div>
      </div>

      {/* Doctor Caseload Chart */}
      <div
        style={{
          background: 'var(--bg-card)',
          border: '1px solid var(--border-color)',
          borderRadius: 'var(--radius-md)',
          padding: '24px',
          boxShadow: 'var(--shadow-sm)',
          marginTop: '20px',
        }}
      >
        <div style={{ marginBottom: '20px' }}>
          <h3 style={{ fontSize: '17px', fontWeight: '700', color: 'var(--text-primary)' }}>
            📊 Physician Appointment Distribution
          </h3>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
            Comparison of total bookings across healthcare providers.
          </p>
        </div>

        {doctor_stats && doctor_stats.length > 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {doctor_stats.map((doc) => {
              const percentage = Math.round((doc.appointment_count / maxAppointments) * 100);
              return (
                <div key={doc.doctor_id} style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px' }}>
                    <span style={{ fontWeight: '600', color: 'var(--text-primary)' }}>
                      {doc.doctor_name} <span style={{ color: 'var(--text-muted)', fontWeight: 'normal' }}>({doc.specialization})</span>
                    </span>
                    <span style={{ fontWeight: '700', color: 'var(--accent-teal)' }}>
                      {doc.appointment_count} {doc.appointment_count === 1 ? 'booking' : 'bookings'}
                    </span>
                  </div>

                  <div
                    style={{
                      width: '100%',
                      height: '10px',
                      background: 'rgba(255, 255, 255, 0.05)',
                      borderRadius: 'var(--radius-full)',
                      overflow: 'hidden',
                    }}
                  >
                    <div
                      style={{
                        width: `${Math.max(percentage, 4)}%`,
                        height: '100%',
                        background: 'linear-gradient(90deg, var(--accent-blue), var(--accent-teal))',
                        borderRadius: 'var(--radius-full)',
                        transition: 'width 0.6s cubic-bezier(0.16, 1, 0.3, 1)',
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '20px' }}>
            No doctor statistics available yet.
          </div>
        )}
      </div>
    </div>
  );
}
