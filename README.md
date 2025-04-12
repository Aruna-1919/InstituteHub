# 🎓 Academic Role-Based Web Portal – Flask Project

## 🚀 Project Overview

This project is a **Role-Based Academic Web Portal** built using **Flask**. It allows **Students**, **Faculty**, and **Admin** users to interact within a unified system. Each role is provided with access to different dashboards and functionalities, making this a practical solution for managing academic tasks, announcements, and events.

## 👥 User Roles

1. **Student**
   - Can log in to view:
     - Announcements
     - Events
     - Tasks assigned by faculty

2. **Faculty**
   - Can log in to:
     - Post announcements
     - Create and manage events
     - Assign tasks to specific students
     - View registered students for events

3. **Admin**
   - Observational role
   - Placeholder for future extension (e.g., analytics, system-wide settings)

---

## 🧰 Tech Stack

| Layer         | Technology          |
|---------------|---------------------|
| Backend       | Flask (Python)      |
| Frontend      | HTML5, Bootstrap    |
| Database      | SQLite              |
| Templating    | Jinja2              |

---

## 📁 Folder Structure

```bash
├── app.py                     # Main Flask application              # HTML templates
│── login.html
├── register.html
├── student_dashboard.html
├── faculty_dashboard.html
├── schema.sql                 # SQL script for DB schema
├── screenshots             # Screenshots of the app (login, dashboards)
├── README.md                  # You are here!
└── institute_doc.pdf          # Full project documentation
