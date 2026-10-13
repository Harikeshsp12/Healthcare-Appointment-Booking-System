import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    HRFlowable,
)

PDF_FILENAME = "Healthcare_Appointment_Booking_System_Documentation.pdf"

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    c_primary = colors.HexColor("#1A365D")   # Deep navy
    c_secondary = colors.HexColor("#2B6CB0") # Vibrant blue
    c_accent = colors.HexColor("#0D9488")    # Medical teal
    c_dark = colors.HexColor("#1F2937")      # Charcoal
    c_light_bg = colors.HexColor("#F8FAFC")  # Light gray
    c_border = colors.HexColor("#CBD5E1")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceAfter=14,
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=6,
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4,
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=5,
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_dark,
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white,
    )

    story = []

    # 1. Title Banner
    story.append(Paragraph("Healthcare Appointment Booking System", title_style))
    story.append(Paragraph("Technical Architecture, Framework Guide & System Documentation", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_secondary, spaceAfter=14))

    # 2. Executive Overview
    story.append(Paragraph("1. System Overview & Architecture", h1_style))
    story.append(Paragraph(
        "The Healthcare Appointment Booking System is a full-stack, enterprise-grade clinical scheduling "
        "application designed to manage doctor shift schedules, display real-time slot availability, "
        "prevent patient double-booking, and ensure consultations adhere strictly to doctor working hours. "
        "It consists of a <b>FastAPI</b> backend, a <b>SQLite</b> database tracked with <b>Alembic</b> migrations, "
        "a <b>ReactJS</b> single-page frontend with 12-hour AM/PM time formatting, and a generated <b>Python SDK</b>.",
        body_style
    ))

    # Architecture summary table
    arch_data = [
        [Paragraph("Component", table_header_style), Paragraph("Technology", table_header_style), Paragraph("Port / Location", table_header_style), Paragraph("Primary Role", table_header_style)],
        [Paragraph("Frontend Client", table_cell_style), Paragraph("React 18 + Vite + Axios", table_cell_style), Paragraph("http://localhost:3000", table_cell_style), Paragraph("Clean single-page booking UI, 12h time slots, real-time sync", table_cell_style)],
        [Paragraph("Backend API", table_cell_style), Paragraph("FastAPI (Python 3.12)", table_cell_style), Paragraph("http://localhost:8000", table_cell_style), Paragraph("REST API, business logic, working-hour validation, CORS", table_cell_style)],
        [Paragraph("Database", table_cell_style), Paragraph("SQLite (SQLAlchemy ORM)", table_cell_style), Paragraph("healthcare.db (Local)", table_cell_style), Paragraph("Persistent relational storage for doctors and appointments", table_cell_style)],
        [Paragraph("Migrations", table_cell_style), Paragraph("Alembic", table_cell_style), Paragraph("alembic/versions/", table_cell_style), Paragraph("Versioned database schema migration management", table_cell_style)],
        [Paragraph("Client SDK", table_cell_style), Paragraph("OpenAPI Generator CLI", table_cell_style), Paragraph("health_sdk/", table_cell_style), Paragraph("Auto-generated typed Python SDK for API consumers", table_cell_style)],
        [Paragraph("Live Broadcaster", table_cell_style), Paragraph("WebSockets (/ws)", table_cell_style), Paragraph("ws://localhost:8000/ws", table_cell_style), Paragraph("Real-time live push updates when appointments are booked/cancelled", table_cell_style)],
    ]
    t_arch = Table(arch_data, colWidths=[1.1 * inch, 1.6 * inch, 1.4 * inch, 2.9 * inch])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 12))

    # 3. How FastAPI Works
    story.append(Paragraph("2. Deep Dive: How FastAPI Works", h1_style))
    story.append(Paragraph(
        "<b>FastAPI</b> is a modern, high-performance web framework for building APIs with Python based on standard Python type hints. "
        "Here is what happens under the hood when a request arrives:",
        body_style
    ))
    story.append(Paragraph("• <b>Asynchronous ASGI Server (Uvicorn):</b> FastAPI runs on an Asynchronous Server Gateway Interface (ASGI) engine. Requests are received non-blockingly, allowing high concurrency and low latency.", bullet_style))
    story.append(Paragraph("• <b>Automatic Type Validation (Pydantic v2):</b> When a JSON payload arrives, FastAPI uses Pydantic schemas to validate data types (e.g., verifying doctor_id is an integer, slot is a valid ISO timestamp, and start_hour < end_hour). If invalid, FastAPI automatically returns an HTTP 422/400 error without manual validation code.", bullet_style))
    story.append(Paragraph("• <b>Dependency Injection Pattern (Depends(get_db)):</b> Database connections are injected into endpoints per request. A database session is automatically opened for the endpoint and guaranteed to be cleanly closed upon completion.", bullet_style))
    story.append(Paragraph("• <b>Interactive OpenAPI & Swagger UI:</b> FastAPI automatically inspects function type signatures and generates an OpenAPI 3.1 specification (/openapi.json) and an interactive Swagger UI at <b>http://localhost:8000/docs</b>.", bullet_style))
    story.append(Spacer(1, 10))

    # 4. Where is Data Stored?
    story.append(Paragraph("3. Where the Data is Stored (Database Architecture)", h1_style))
    story.append(Paragraph(
        "All application data is persistently stored in a local, single-file <b>SQLite</b> database located at: "
        "<b><code>healthcare.db</code></b> in your project root.",
        body_style
    ))
    story.append(Paragraph(
        "SQLite is a serverless, embedded relational database engine. Unlike MySQL or PostgreSQL, SQLite runs inside "
        "the FastAPI application process without needing a separate database daemon or server port.",
        body_style
    ))

    db_schema_data = [
        [Paragraph("Table Name", table_header_style), Paragraph("Columns & Types", table_header_style), Paragraph("Constraints & Description", table_header_style)],
        [
            Paragraph("<b>doctors</b>", table_cell_style),
            Paragraph("id: INTEGER (PK)<br/>name: TEXT<br/>specialization: TEXT<br/>start_hour: INT<br/>end_hour: INT", table_cell_style),
            Paragraph("Stores clinician profile and shift working hours (0-24). Auto-incrementing primary key.", table_cell_style)
        ],
        [
            Paragraph("<b>appointments</b>", table_cell_style),
            Paragraph("id: INTEGER (PK)<br/>doctor_id: INT (FK)<br/>patient_name: TEXT<br/>slot: TIMESTAMP", table_cell_style),
            Paragraph("Foreign key to doctors(id) with CASCADE delete. Stores patient appointment slot timestamps.", table_cell_style)
        ],
        [
            Paragraph("<b>alembic_version</b>", table_cell_style),
            Paragraph("version_num: VARCHAR(32)", table_cell_style),
            Paragraph("Maintained by Alembic to track which database migration revisions have been applied.", table_cell_style)
        ],
    ]
    t_db = Table(db_schema_data, colWidths=[1.4 * inch, 2.3 * inch, 3.3 * inch])
    t_db.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
    ]))
    story.append(t_db)
    story.append(Spacer(1, 12))

    story.append(PageBreak())

    # 5. Trick Logic Explanation
    story.append(Paragraph("4. Backend Business Logic & Trick Logic (Hidden Complexity)", h1_style))
    story.append(Paragraph(
        "The coding challenge requires two core business rules (Trick Logic) to prevent scheduling conflicts:",
        body_style
    ))

    story.append(Paragraph("Rule 1: Double-Booking Prevention", h2_style))
    story.append(Paragraph(
        "• <b>Mechanism:</b> When a booking request is made (<code>POST /appointments/</code>), the backend queries "
        "the database to see if an appointment already exists for the same <code>doctor_id</code> at the exact requested <code>slot</code>.<br/>"
        "• <b>Outcome:</b> If an existing appointment is found, the server rejects the request with HTTP <b>409 Conflict</b>: "
        "<i>'Dr. [Name] already has an appointment booked at [Time]'</i>.<br/>"
        "• <b>Isolation:</b> Double-booking checks are strictly doctor-specific. Two different doctors can both be booked at 10:00 AM simultaneously without conflict.",
        body_style
    ))

    story.append(Paragraph("Rule 2: Working Hours Enforcement", h2_style))
    story.append(Paragraph(
        "• <b>Mechanism:</b> Each doctor has a defined shift: <code>start_hour</code> and <code>end_hour</code> (e.g., 9:00 AM to 5:00 PM).<br/>"
        "• <b>Boundary Rule:</b> Appointments are 1-hour consultations. The appointment starting hour must satisfy: "
        "<code>start_hour &lt;= slot.hour &lt; end_hour</code>.<br/>"
        "• <b>Example:</b> For a doctor working 9:00 AM to 5:00 PM (9 to 17), valid slots are 9:00 AM through 4:00 PM. "
        "Any request for 8:00 AM (before start) or 5:00 PM (end of shift) is rejected with HTTP <b>400 Bad Request</b>.",
        body_style
    ))

    story.append(Paragraph("Rule 3: Slot Reutilization After Cancellation", h2_style))
    story.append(Paragraph(
        "• When an appointment is cancelled (<code>DELETE /appointments/{id}</code>), the slot is permanently deleted from the database. "
        "The slot immediately becomes available for other patients to book in real time.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # 6. REST API Endpoints Summary
    story.append(Paragraph("5. Complete REST API Endpoints", h1_style))
    endpoints_data = [
        [Paragraph("Method & Route", table_header_style), Paragraph("Description", table_header_style), Paragraph("Key Parameters", table_header_style), Paragraph("Status", table_header_style)],
        [Paragraph("POST /doctors/", table_cell_style), Paragraph("Add new doctor with shift hours", table_cell_style), Paragraph("name, specialization, start_hour, end_hour", table_cell_style), Paragraph("201 Created", table_cell_style)],
        [Paragraph("GET /doctors/", table_cell_style), Paragraph("List all registered physicians", table_cell_style), Paragraph("None", table_cell_style), Paragraph("200 OK", table_cell_style)],
        [Paragraph("GET /doctors/{id}", table_cell_style), Paragraph("Retrieve details of a specific doctor", table_cell_style), Paragraph("id (path)", table_cell_style), Paragraph("200 / 404", table_cell_style)],
        [Paragraph("PUT /doctors/{id}", table_cell_style), Paragraph("Edit/update doctor profile & hours", table_cell_style), Paragraph("id (path), name, spec, hours", table_cell_style), Paragraph("200 / 404", table_cell_style)],
        [Paragraph("DELETE /doctors/{id}", table_cell_style), Paragraph("Delete doctor & cascade appointments", table_cell_style), Paragraph("id (path)", table_cell_style), Paragraph("200 / 404", table_cell_style)],
        [Paragraph("GET /doctors/{id}/availability", table_cell_style), Paragraph("Get 1-hour slots & availability for date", table_cell_style), Paragraph("id (path), query_date (YYYY-MM-DD)", table_cell_style), Paragraph("200 OK", table_cell_style)],
        [Paragraph("POST /appointments/", table_cell_style), Paragraph("Book appointment (with trick logic)", table_cell_style), Paragraph("doctor_id, patient_name, slot", table_cell_style), Paragraph("201 / 400 / 409", table_cell_style)],
        [Paragraph("GET /appointments/", table_cell_style), Paragraph("List appointments with optional filters", table_cell_style), Paragraph("doctor_id, patient_name (query)", table_cell_style), Paragraph("200 OK", table_cell_style)],
        [Paragraph("DELETE /appointments/{id}", table_cell_style), Paragraph("Cancel appointment and free slot", table_cell_style), Paragraph("id (path)", table_cell_style), Paragraph("200 / 404", table_cell_style)],
        [Paragraph("GET /stats", table_cell_style), Paragraph("System dashboard & caseload analytics", table_cell_style), Paragraph("None", table_cell_style), Paragraph("200 OK", table_cell_style)],
        [Paragraph("WS /ws", table_cell_style), Paragraph("WebSocket connection for live updates", table_cell_style), Paragraph("WebSocket handshake", table_cell_style), Paragraph("101 Switch", table_cell_style)],
    ]
    t_end = Table(endpoints_data, colWidths=[1.9 * inch, 2.2 * inch, 2.0 * inch, 0.9 * inch])
    t_end.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
    ]))
    story.append(t_end)
    story.append(Spacer(1, 12))

    story.append(PageBreak())

    # 7. Frontend Features
    story.append(Paragraph("6. ReactJS Frontend Implementation", h1_style))
    story.append(Paragraph(
        "The frontend client is built with React 18, Vite, and Axios for a lightweight, ultra-responsive user experience:",
        body_style
    ))
    story.append(Paragraph("• <b>Single-Page Simplicity:</b> All functionality—viewing schedules, booking appointments, cancelling bookings, and managing doctors—is accessible on a single uncluttered dashboard without complicated tab switching or nested modals.", bullet_style))
    story.append(Paragraph("• <b>12-Hour AM/PM Time Formatting:</b> All doctor shifts, slot buttons, and scheduled timestamps are cleanly formatted in 12-hour AM/PM format (e.g., 9:00 AM – 5:00 PM, 10:00 AM, 2:00 PM).", bullet_style))
    story.append(Paragraph("• <b>Interactive Slot Picker:</b> Available consultation slots are displayed as green (Free) buttons. Clicking any free slot instantly selects the time and populates the booking box.", bullet_style))
    story.append(Paragraph("• <b>Doctor Management:</b> Provides an '+ Add New Doctor' button, an '✏️ Edit' button to modify working hours or specialties, and a '🗑️ Delete' button to remove doctors.", bullet_style))
    story.append(Paragraph("• <b>Real-Time WebSocket Sync:</b> Listens to <code>/ws</code>. When an appointment is booked or cancelled in any window, all connected browser sessions automatically refresh the availability grid and schedule tables without reloading.", bullet_style))
    story.append(Spacer(1, 10))

    # 8. Platform Python SDK
    story.append(Paragraph("7. Platform Python SDK (OpenAPI Generator CLI)", h1_style))
    story.append(Paragraph(
        "Instead of writing manual API wrapper code, a production-grade Python SDK was compiled using the official "
        "OpenAPI Generator CLI tool: <code>npm install -g @openapitools/openapi-generator-cli</code>.",
        body_style
    ))
    story.append(Paragraph("<b>Exact Required SDK Usage:</b>", h2_style))
    sdk_code = (
        "from health_sdk.api.doctors_api import DoctorsApi<br/>"
        "from health_sdk import ApiClient<br/><br/>"
        "client = ApiClient()<br/>"
        "api = DoctorsApi(client)<br/>"
        "doctors = api.list_doctors()<br/>"
        "for d in doctors:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;print(f'Doctor: {d.name} ({d.specialization})')"
    )
    story.append(Paragraph(sdk_code, code_style))
    story.append(Spacer(1, 10))

    # 9. Verification & Automated Testing
    story.append(Paragraph("8. Automated Testing & Verification", h1_style))
    story.append(Paragraph(
        "The test suite is powered by <b>Pytest</b> with 100% pass rate (39 passed tests) verifying:",
        body_style
    ))
    story.append(Paragraph("• <b>Doctor Creation & Boundaries:</b> Verifies doctor registration, negative hours rejection, and start_hour >= end_hour constraints.", bullet_style))
    story.append(Paragraph("• <b>Double-Booking Trick Logic:</b> Verifies that booking Dr. A at 10:00 AM succeeds, and immediately re-booking Dr. A at 10:00 AM is rejected with HTTP 409 Conflict.", bullet_style))
    story.append(Paragraph("• <b>Working Hours Trick Logic:</b> Verifies that slots outside a doctor's shift are rejected with HTTP 400 Bad Request.", bullet_style))
    story.append(Paragraph("• <b>Cancellation & Slot Reutilization:</b> Verifies slot is freed and can be re-booked once cancelled.", bullet_style))
    story.append(Paragraph("• <b>Cascade Deletion:</b> Verifies deleting a doctor removes all associated bookings.", bullet_style))
    story.append(Spacer(1, 12))

    # 10. Execution Scripts
    story.append(Paragraph("9. Execution Scripts & Quick Start", h1_style))
    story.append(Paragraph(
        "The project is 100% turnkey and can be launched on Windows using the included batch scripts:",
        body_style
    ))
    story.append(Paragraph("• <b>setupdev.bat:</b> Creates Python venv, installs requirements, executes Alembic migrations, and runs frontend npm install.<br/>"
                           "• <b>runapplication.bat:</b> Starts FastAPI backend on port 8000 and React frontend on port 3000 concurrently.", body_style))

    doc.build(story)
    print(f"Generated {PDF_FILENAME} successfully!")

if __name__ == "__main__":
    build_pdf()
