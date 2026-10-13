-- ==============================================================================
-- Healthcare Appointment Booking System - Seed Data
-- ==============================================================================

-- Clear existing data if re-seeding
DELETE FROM appointments;
DELETE FROM doctors;

-- 1. Insert Sample Doctors
-- id, name, specialization, start_hour (24h), end_hour (24h)
INSERT INTO doctors (id, name, specialization, start_hour, end_hour) VALUES
(1, 'Dr. Alice Smith', 'Cardiology', 9, 17),
(2, 'Dr. Bob Johnson', 'Dermatology', 10, 16),
(3, 'Dr. Charlie Brown', 'Pediatrics', 8, 14),
(4, 'Dr. Diana Prince', 'Neurology', 9, 15),
(5, 'Dr. Edward Norton', 'Orthopedics', 11, 18);

-- 2. Insert Sample Appointments
-- id, doctor_id, patient_name, slot (TIMESTAMP)
INSERT INTO appointments (id, doctor_id, patient_name, slot) VALUES
(1, 1, 'John Doe', '2026-10-15 10:00:00'),
(2, 1, 'Jane Smith', '2026-10-15 14:00:00'),
(3, 2, 'Robert Taylor', '2026-10-15 11:00:00'),
(4, 3, 'Emily Davis', '2026-10-15 09:00:00'),
(5, 4, 'Michael Clark', '2026-10-15 13:00:00');
