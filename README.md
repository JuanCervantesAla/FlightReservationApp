# ✈️ Fault-Tolerant Flight Reservation System

This project is a simple **flight booking system** designed to demonstrate **fault tolerance** using modern backend technologies and design patterns.

![image](https://github.com/user-attachments/assets/338a41bc-a25a-4063-b3ed-2de456371015)

## 🔧 Technologies Used

### 🖥️ Backend
- **FastAPI** – For building the REST API
- **MongoDB** – As the main database
- **Uvicorn** – ASGI server to run FastAPI
- **AsyncIO** – For background task execution
- **Custom Circuit Breaker & Retry Queue** – To handle fault tolerance

### 📱 Frontend (Mobile)
- **React Native with Expo** – Cross-platform mobile UI
- **Axios** – For API communication

## 🧠 Features

### ✅ Functional
- Users can view available flights
- Users can book flights (with real-time or pending status)
- Users can check their reservations
- Failed reservations are retried automatically in the background

### ⚙️ Fault-Tolerant Design
- **Circuit Breaker:** Temporarily disables a service after repeated failures
- **Retry Queue:** Failed reservations are enqueued and reattempted later
- **Background Processing:** Tasks like retrying are handled asynchronously
- **Pending State:** Users get a `"pending"` status while the system tries again in the background

## 📂 Project Structure
backend/ ├── main.py ├── database.py ├── models/ ├── services/ └── utils/

frontend/ ├── App.js ├── screens/ ├── components/ └── api/

## 📸 UI Screenshots

![image](https://github.com/user-attachments/assets/1e654eee-9c49-4122-b56f-413fed98f2a5)
![image](https://github.com/user-attachments/assets/2de5647e-1f7d-48c7-824d-e8c2b99bf255)


## 🚀 How to Run

### Backend
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

### FrontEnd
cd frontend
npm install
npx expo start
