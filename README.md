
# Schedulo

Schedulo is a scheduling platform that allows **freelancers** to manage their availability and lets **clients** book meetings based on available time slots. It automatically creates Zoom meeting links and sends confirmation emails to both users.

---

## 🚀 Features

### 👤 Freelancers
- Register/login
- Define available time slots
- View and manage booking requests
- Accept or reject meetings

### 👥 Clients
- Browse freelancers
- View availability
- Request bookings

### ⚙️ System
- Automatically generates Zoom meetings
- Sends email confirmations using SendGrid

---

## 🧱 Tech Stack

- **Backend:** FastAPI, PostgreSQL, SQLAlchemy
- **Frontend:** React (Vite)
- **Auth:** JWT
- **Email:** SendGrid SMTP
- **Meetings:** Zoom API
- **Containerization:** Docker & Docker Compose

---

## 🐳 Docker Setup

### Requirements:
- Docker & Docker Compose installed

### Run the app:

```bash
docker-compose up --build
```

### Ports:
- Frontend: http://localhost:3000
- API: http://localhost:8000

---

## 🔐 Environment Variables

Create the following `.env` files:

### `backend/.env` (based on `.env.example`):

```env
DATABASE_URL=postgresql://schedulo_user:schedulo_password@123@db/schedulo_db
SENDGRID_API_KEY=your-sendgrid-api-key
JWT_SECRET=your-jwt-secret
ZOOM_CLIENT_ID=your-zoom-client-id
ZOOM_CLIENT_SECRET=your-zoom-client-secret
ZOOM_ACCOUNT_ID=your-zoom-account-id
```

> ⚠️ **Important:** Do not commit `.env` files. Add them to `.gitignore`.

---

## 🧪 API Endpoints

### 📌 Auth
- `POST /api/v1/auth/register` – Register new user  
- `POST /api/v1/auth/login` – Login  
- `GET /api/v1/auth/me` – Get current user  

### 📌 Availability
- `POST /api/v1/availability` – Create Availability 
- `GET /api/v1/availability/freelancer/{freelancer_id}/` – Get all availability by freelancer id
- `GET /api/v1/availability/{id}` – Get single availability
- `PUT /api/v1/availability/{id}` – Update availability
- `DELETE /api/v1/availability/{id}` – Delete availability

### 📌 Bookings
- `GET /api/v1/bookings/` – Get user bookings  
- `POST /api/v1/bookings/create/{availability_id}` – Request new booking 
- `PUT /api/v1/bookings/{id}` – Accept/Reject/Complete  
- `GET /api/v1/bookings/{id}` – Get booking detail  
- `DELETE /bookings/{id}` – Cancel booking

---

## 🗂️ Project Structure

### 📁 Backend

```
backend/
├── app/
│   ├── api/         # Routers
│   ├── models/      # SQLAlchemy Models
│   ├── schemas/     # Pydantic Schemas
│   ├── services/    # Zoom, Email, Bookings
│   ├── auth/        # JWT Logic
│   ├── db/          # Database Session
│   └── main.py      # FastAPI entrypoint
├── Dockerfile
├── alembic/         # Migrations
└── .env
```

### 📁 Frontend (Planned)

- `Home`
- `Set or edit available time`
- `Browse freelancers`
- `Accept or reject meetings`

#### Components
- `Header`, `SearchBar`, `DatePicker`, `AvailableSlots`, `BookingRequest`

---

## 📦 Deployment

This project uses Docker Compose with three services:

- **frontend** (port `3000`)
- **api** (port `8000`)
- **db** (PostgreSQL container)

To deploy in production, consider:
- Using a reverse proxy like NGINX
- Setting environment secrets via Docker secrets
- Running containers with `restart: always` (already enabled)

---

## 🤝 Contributing

1. Fork the repo
2. Clone it locally
3. Create a new branch
4. Make your changes
5. Submit a Pull Request


---

## 🙏 Credits

Developed by Safayat Khan Rohan. Zoom integration powered by the Zoom API. Email functionality uses SendGrid.
