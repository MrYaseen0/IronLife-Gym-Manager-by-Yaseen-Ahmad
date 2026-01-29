# 🏋️ IronLife Gym Manager - Quick Start Guide

## ✅ System Status

- ✅ **Backend Server**: Running on `http://localhost:5000`
- ✅ **Database**: SQLite initialized
- ✅ **Admin Account**: Created (admin / 123456)
- ✅ **Sample Data**: 4 gym members loaded

---

## 🚀 How to Access the Application

### **Option 1: Direct File Access (Recommended)**
Simply open this file in your web browser:
```
C:\Users\Yaseen_ahmad\Downloads\ejaz sir proj\index.html
```

### **Option 2: Use Local Server**
Since backend is running, you can access:
```
http://localhost:5000/
```

---

## 📍 File Locations

All files are in: `C:\Users\Yaseen_ahmad\Downloads\ejaz sir proj\`

| File | Purpose |
|------|---------|
| `index.html` | 🏠 Start page with options |
| `gym-manager.html` | 💻 Main application |
| `api-test.html` | 🧪 API testing interface |
| `setup.html` | 🔧 System diagnostics |
| `style.css` | 🎨 Styling |
| `script.js` | ⚙️ Frontend logic |
| `app.py` | 🐍 Backend server |

---

## 🔐 Login Credentials

**Username:** `admin`  
**Password:** `123456`

---

## 📊 Available Features

### Dashboard
- Total members count
- Active members count
- Monthly revenue tracking
- Recent registrations

### Member Management
- Add new members
- View all members
- Search by name/phone
- Delete members
- Track membership plans

### Plans Available
- **Basic**: ₹1000/month
- **Pro**: ₹2500/month
- **Elite**: ₹5000/month

---

## 🔗 API Endpoints

The backend provides REST API endpoints:

### Authentication
- `POST /api/login` - User login
- `POST /api/register` - New user registration

### Members
- `GET /api/members` - Get all members
- `POST /api/members` - Add new member
- `DELETE /api/members/<id>` - Delete member
- `GET /api/members/search?q=query` - Search members

### Statistics
- `GET /api/stats/dashboard` - Dashboard stats
- `GET /api/stats/revenue` - Revenue analytics

### Health
- `GET /api/health` - Check if server is running

---

## ⚙️ System Configuration

### Backend (Flask)
- **Port**: 5000
- **Database**: SQLite (gym_manager.db)
- **Debug Mode**: Enabled
- **CORS**: Enabled for all origins

### Frontend
- **Framework**: HTML5 + CSS3 + JavaScript
- **API Base**: http://localhost:5000/api
- **Storage**: Browser LocalStorage (for offline mode)

---

## 🎯 Quick Navigation

1. **Open Application**
   - Go to: `index.html`
   - Click: "OPEN APP"

2. **Login**
   - Username: admin
   - Password: 123456

3. **Create Member**
   - Go to: "Add Member" section
   - Fill form and submit

4. **View Members**
   - Go to: "All Members" section
   - Use search to find members

---

## 🐛 Troubleshooting

### Backend Won't Start
```powershell
# Make sure you're in the project directory
cd "C:\Users\Yaseen_ahmad\Downloads\ejaz sir proj"

# Run the app
python app.py
```

### Port 5000 Already in Use
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

### Files Not Found
- Ensure all files are in: `C:\Users\Yaseen_ahmad\Downloads\ejaz sir proj\`
- Check file names are exactly: gym-manager.html, style.css, script.js, app.py

### Database Errors
```powershell
# Delete the old database
del gym_manager.db

# Restart the app to create fresh database
python app.py
```

---

## 📝 Sample Members

The system comes with 4 pre-loaded members:

1. **Rahul Sharma** - Pro Plan (₹2500)
2. **Priya Singh** - Elite Plan (₹5000)
3. **Amit Kumar** - Basic Plan (₹1000)
4. **Sneha Gupta** - Pro Plan (₹2500)

---

## 🎓 Learning Resources

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **Database**: SQLAlchemy ORM with SQLite
- **API**: REST principles

---

## 📞 Support

If you encounter issues:

1. Check terminal output for error messages
2. Test API using `api-test.html`
3. Check diagnostics using `setup.html`
4. Verify backend is running: `python app.py`

---

## ✨ Project Features

✅ Complete gym management system  
✅ Modern dark UI design  
✅ Responsive mobile layout  
✅ Real-time dashboard  
✅ Member search & filtering  
✅ Revenue tracking  
✅ Offline capability  
✅ REST API  
✅ SQLite database  
✅ Admin authentication  

---

**Created:** January 29, 2026  
**Version:** 1.0.0  
**Status:** ✅ Ready to Use
