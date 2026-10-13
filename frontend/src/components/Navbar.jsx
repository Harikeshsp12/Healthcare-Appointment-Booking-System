import React from 'react';

export default function Navbar({ activeTab, setActiveTab, onOpenAddDoctor, wsConnected }) {
  return (
    <header className="navbar">
      <div className="navbar-inner">
        <div className="brand-wrapper">
          <div className="brand-icon">⚕</div>
          <div>
            <h1 className="brand-title">CareSync</h1>
            <p className="brand-subtitle">Healthcare Appointments</p>
          </div>
        </div>

        <nav className="nav-tabs">
          <button
            className={`nav-tab-btn ${activeTab === 'doctors' ? 'active' : ''}`}
            onClick={() => setActiveTab('doctors')}
          >
            <span>👨‍⚕️</span> Doctors & Availability
          </button>
          <button
            className={`nav-tab-btn ${activeTab === 'appointments' ? 'active' : ''}`}
            onClick={() => setActiveTab('appointments')}
          >
            <span>📅</span> Appointments
          </button>
          <button
            className={`nav-tab-btn ${activeTab === 'analytics' ? 'active' : ''}`}
            onClick={() => setActiveTab('analytics')}
          >
            <span>📊</span> Analytics
          </button>
        </nav>

        <div className="nav-actions">
          <div
            className={`ws-status-badge ${wsConnected ? '' : 'disconnected'}`}
            title={wsConnected ? 'Real-Time Sync Active via WebSocket' : 'WebSocket Disconnected (Falling back to auto-poll)'}
          >
            <span className="pulse-dot"></span>
            {wsConnected ? 'Live Sync Active' : 'Offline Sync'}
          </div>

          <button className="btn btn-primary" onClick={onOpenAddDoctor}>
            <span>+</span> Add Doctor
          </button>
        </div>
      </div>
    </header>
  );
}
