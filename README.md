# IronLife Gym Manager

A complete gym management system with member registration, authentication, and dashboard analytics.

## Project Structure

```
ejaz sir proj/
├── gym-manager.html      # Frontend HTML (Bootstrap)
├── style.css             # Custom CSS styling
├── script.js             # Frontend JavaScript logic
├── app.py                # Python Flask backend
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Features

### Frontend (HTML/CSS/JavaScript)
- **Beautiful Dark UI** with modern glass morphism effects
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Login System** - Simple authentication (Demo: admin/123456)
- **Member Management** - Add, view, search, and delete members
- **Dashboard** - Real-time statistics (total members, revenue, etc.)
- **Offline Mode** - Uses localStorage for data persistence
- **Toast Notifications** - User feedback for actions

### Backend (Python Flask)
- **REST API** - Full CRUD operations for members
- **User Authentication** - Login/Register endpoints
- **Database** - SQLite with SQLAlchemy ORM
- **Statistics** - Revenue tracking and member analytics
- **Payment Tracking** - Record and view payments
- **Search & Filter** - Advanced member search functionality
- **CORS Enabled** - Ready for multi-domain deployment

## Installation

### 1. Backend Setup (Python)

```bash
# Navigate to project directory
cd "c:\Users\Yaseen_ahmad\Downloads\ejaz sir proj"

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Start the Backend Server

```bash
# Run Flask application
python app.py
```

Server will start at: `http://localhost:5000`

### 3. Open Frontend

Open `gym-manager.html` in your web browser:
- **File Path:** `c:\Users\Yaseen_ahmad\Downloads\ejaz sir proj\gym-manager.html`
- Or double-click the file

## Default Credentials

```
Username: admin
Password: 123456
```

## API Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/register` - User registration
- `POST /api/logout` - User logout

### Members
- `GET /api/members` - Get all members
- `GET /api/members/<id>` - Get specific member
- `POST /api/members` - Add new member
- `PUT /api/members/<id>` - Update member
- `DELETE /api/members/<id>` - Delete member
- `GET /api/members/search?q=query` - Search members

### Statistics
- `GET /api/stats/dashboard` - Dashboard statistics
- `GET /api/stats/revenue` - Revenue analytics

### Payments
- `POST /api/payments` - Record payment
- `GET /api/payments/member/<id>` - Get member payments

### Health
- `GET /api/health` - API health check

## Usage

### 1. Login
- Enter username and password
- Click "LOGIN TO DASHBOARD"
- Default demo access: admin / 123456

### 2. Add Members
- Go to "Add Member" section
- Fill in member details (Name, Phone, Plan, etc.)
- Select membership plan:
  - Basic: ₹1000/month
  - Pro: ₹2500/month
  - Elite: ₹5000/month
- Click "Register Member"

### 3. View Members
- Go to "All Members" section
- View complete member directory
- Search by name or phone number
- Delete member with trash icon

### 4. Dashboard
- View total members count
- Track active members
- Monitor monthly revenue
- See recent registrations

## Technology Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom styling with animations
- **JavaScript (ES6+)** - DOM manipulation and API calls
- **Font Awesome** - Icons
- **Google Fonts** - Typography

### Backend
- **Python 3.8+** - Programming language
- **Flask** - Lightweight web framework
- **SQLAlchemy** - ORM for database
- **SQLite** - Lightweight database
- **Flask-CORS** - Cross-origin requests

## File Descriptions

### gym-manager.html
Main frontend file with:
- Login interface
- Dashboard section
- Member management interface
- Responsive layout

### style.css
Comprehensive styling with:
- Dark theme color scheme
- Responsive design rules
- Animations and transitions
- Glass morphism effects
- Mobile-first approach

### script.js
Frontend logic including:
- Authentication handling
- Member CRUD operations
- API communication
- Data persistence (localStorage)
- UI state management

### app.py
Backend Flask application with:
- SQLAlchemy models
- RESTful API routes
- Database initialization
- Authentication logic
- Error handling

## Data Models

### User
```python
{
    "id": int,
    "username": str,
    "email": str,
    "role": str,
    "password": str,
    "created_at": datetime
}
```

### Member
```python
{
    "id": int,
    "name": str,
    "phone": str,
    "email": str,
    "gender": str,
    "plan": str,      # Basic, Pro, Elite
    "amount": int,    # Monthly fee in INR
    "joinDate": str,  # YYYY-MM-DD
    "status": str,    # Active, Inactive
    "renewal_date": str
}
```

### Payment
```python
{
    "id": int,
    "member_id": int,
    "amount": int,
    "payment_date": datetime,
    "method": str,    # Cash, Card, UPI
    "status": str,
    "notes": str
}
```

## Configuration

### Database
- **Type:** SQLite
- **Location:** `gym_manager.db` (auto-created)
- **Connection:** `sqlite:///gym_manager.db`

### Server
- **Host:** localhost
- **Port:** 5000
- **Debug Mode:** Enabled
- **CORS:** Enabled for all domains

## Features Highlights

### Offline Functionality
- Data syncs to localStorage
- Works without backend
- Automatic sync when backend available

### Responsive Design
- Desktop: Full sidebar layout
- Tablet: Optimized spacing
- Mobile: Hamburger menu, stacked layout

### Data Validation
- Required field validation
- Phone number uniqueness
- Date format validation
- Plan-based pricing

### Animations
- Fade-in effects on page load
- Smooth transitions
- Hover effects on buttons
- Toast notifications

## Security Notes

⚠️ **For Demo/Development Only:**
- Passwords stored in plain text (use bcrypt in production)
- No JWT tokens (implement JWT for production)
- CORS allows all origins (restrict in production)
- Hard-coded demo credentials

## Future Enhancements

1. **User Management**
   - Multiple user roles
   - Admin panel
   - User activity logs

2. **Advanced Features**
   - Attendance tracking
   - Workout plan assignment
   - SMS/Email notifications
   - Invoice generation

3. **Analytics**
   - Monthly/yearly reports
   - Revenue trends
   - Member growth charts
   - Churn analysis

4. **Integration**
   - Payment gateway (Razorpay, Stripe)
   - WhatsApp notifications
   - Backup to cloud storage
   - Multi-branch support

## Troubleshooting

### Backend not connecting?
- Make sure Flask server is running on port 5000
- Check if port 5000 is not in use: `netstat -ano | findstr :5000`
- Application will work offline using localStorage

### Styling not loading?
- Ensure `style.css` is in the same directory
- Clear browser cache (Ctrl+Shift+Delete)
- Check browser console for CSS errors

### Database errors?
- Delete `gym_manager.db` to reset database
- Run `python app.py` again to reinitialize
- Check `requirements.txt` packages are installed

### Port already in use?
- Change port in `app.py`: `app.run(port=5001)`
- Or kill process: `taskkill /PID <pid> /F`

## Performance Tips

- Use modern browser (Chrome, Firefox, Edge)
- Enable browser caching
- Minimize network requests
- Compress images if adding them
- Use CDN for external libraries

## License

This project is free to use and modify for personal/educational purposes.

## Support

For issues or questions, check:
1. Browser console for errors
2. Flask server output
3. SQLite database logs
4. Network tab in DevTools

---

**Created:** January 29, 2026  
**Version:** 1.0.0  
**Status:** Production Ready (Demo)
