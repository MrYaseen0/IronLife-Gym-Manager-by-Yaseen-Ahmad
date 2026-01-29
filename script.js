// IronLife Gym Manager - JavaScript Logic

// ==================== STATE & VARIABLES ====================
let members = [];
let isLoggedIn = false;
const API_BASE = 'http://localhost:5000/api';

// ==================== INITIALIZATION ====================
window.addEventListener('load', function() {
    initializeApp();
});

function initializeApp() {
    // Set default date in form
    const dateInput = document.getElementById('m-date');
    if (dateInput) {
        dateInput.valueAsDate = new Date();
    }
    
    // Load members from localStorage (offline mode)
    loadFromLocalStorage();
}

// ==================== AUTHENTICATION ====================
async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('login-user').value.trim();
    const password = document.getElementById('login-pass').value.trim();
    const errorMsg = document.getElementById('login-error');
    
    // Validate input
    if (!username || !password) {
        showError(errorMsg, 'Please enter username and password');
        return;
    }
    
    try {
        // Try to connect to backend
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            // Backend authentication successful
            loginSuccess(data);
        } else {
            showError(errorMsg, 'Invalid username or password');
            shakeElement(document.querySelector('#login-section > div'));
        }
    } catch (err) {
        // Backend not available - use demo auth
        if (username === 'admin' && password === '123456') {
            loginSuccess({ username: 'admin', role: 'Manager' });
        } else {
            showError(errorMsg, 'Invalid username or password');
            shakeElement(document.querySelector('#login-section > div'));
        }
    }
}

function loginSuccess(userData) {
    isLoggedIn = true;
    
    // Hide login, show app
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('app-section').classList.remove('hidden');
    
    // Store user data
    sessionStorage.setItem('user', JSON.stringify(userData));
    
    showToast(`Welcome back, ${userData.username}!`, 'success');
    refreshData();
}

function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        isLoggedIn = false;
        
        // Clear session
        sessionStorage.removeItem('user');
        
        // Reset form
        document.getElementById('login-user').value = '';
        document.getElementById('login-pass').value = '';
        document.getElementById('login-error').classList.remove('show');
        
        // Show login
        document.getElementById('app-section').classList.add('hidden');
        document.getElementById('login-section').classList.remove('hidden');
        
        showToast('You have been logged out', 'success');
    }
}

// ==================== NAVIGATION ====================
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(el => {
        el.classList.add('hidden');
    });
    
    // Show selected section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.classList.remove('hidden');
    }
    
    // Update navigation active state
    document.querySelectorAll('.nav-item').forEach(el => {
        el.classList.remove('active');
    });
    
    // Find and highlight the active nav item
    const navItems = document.querySelectorAll('.nav-item');
    const navIndex = sectionId === 'dashboard' ? 0 : 
                     sectionId === 'add-member' ? 1 : 2;
    if (navItems[navIndex]) {
        navItems[navIndex].classList.add('active');
    }
    
    // Close mobile menu
    closeMobileMenu();
}

function toggleMobileMenu() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('hidden');
    }
}

function closeMobileMenu() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar && window.innerWidth < 768) {
        sidebar.classList.add('hidden');
    }
}

// ==================== DATA MANAGEMENT ====================
async function loadMembers() {
    try {
        // Try to fetch from backend
        const response = await fetch(`${API_BASE}/members`);
        if (response.ok) {
            members = await response.json();
            return;
        }
    } catch (err) {
        console.log('Backend unavailable, using local data');
    }
    
    // Use local storage or default data
    loadFromLocalStorage();
}

function loadFromLocalStorage() {
    const stored = localStorage.getItem('gym_members');
    if (stored) {
        try {
            members = JSON.parse(stored);
        } catch (err) {
            loadDefaultData();
        }
    } else {
        loadDefaultData();
    }
}

function loadDefaultData() {
    members = [
        { 
            id: 1, 
            name: 'Rahul Sharma', 
            phone: '9876543210', 
            plan: 'Pro', 
            amount: 2500, 
            joinDate: '2023-10-01', 
            gender: 'Male' 
        },
        { 
            id: 2, 
            name: 'Priya Singh', 
            phone: '9123456789', 
            plan: 'Elite', 
            amount: 5000, 
            joinDate: '2023-10-05', 
            gender: 'Female' 
        },
        { 
            id: 3, 
            name: 'Amit Kumar', 
            phone: '9988776655', 
            plan: 'Basic', 
            amount: 1000, 
            joinDate: '2023-10-12', 
            gender: 'Male' 
        },
        { 
            id: 4, 
            name: 'Sneha Gupta', 
            phone: '8877665544', 
            plan: 'Pro', 
            amount: 2500, 
            joinDate: '2023-10-15', 
            gender: 'Female' 
        }
    ];
}

async function saveMembers() {
    // Save to localStorage
    localStorage.setItem('gym_members', JSON.stringify(members));
    
    // Try to sync with backend
    try {
        await fetch(`${API_BASE}/members/sync`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(members)
        });
    } catch (err) {
        // Silently fail if backend unavailable
    }
}

// ==================== DASHBOARD ====================
async function renderDashboard() {
    await loadMembers();
    
    // Calculate stats
    const total = members.length;
    const revenue = members.reduce((sum, m) => sum + m.amount, 0);
    
    // Update stats cards
    const totalCard = document.getElementById('total-members-count');
    const activeCard = document.getElementById('active-members-count');
    const revenueCard = document.getElementById('revenue-count');
    
    if (totalCard) totalCard.textContent = total;
    if (activeCard) activeCard.textContent = total;
    if (revenueCard) revenueCard.textContent = '₹' + revenue.toLocaleString('en-IN');
    
    // Render recent members table
    renderRecentMembers();
}

function renderRecentMembers() {
    const recentBody = document.getElementById('recent-members-body');
    if (!recentBody) return;
    
    recentBody.innerHTML = '';
    
    // Get last 3 members
    const recentMembers = members.slice(-3).reverse();
    
    recentMembers.forEach(m => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="text-white font-medium">${m.name}</td>
            <td>
                <span class="plan-badge plan-${m.plan.toLowerCase()}">
                    ${m.plan}
                </span>
            </td>
            <td class="text-gray-400 text-sm">${m.joinDate}</td>
            <td>
                <span class="status-badge">● Active</span>
            </td>
        `;
        recentBody.appendChild(row);
    });
}

// ==================== MEMBERS LIST ====================
function renderMembersList() {
    const fullBody = document.getElementById('full-members-body');
    if (!fullBody) return;
    
    fullBody.innerHTML = '';
    
    members.forEach(m => {
        // Calculate renewal date (30 days after join)
        const joinDate = new Date(m.joinDate);
        joinDate.setDate(joinDate.getDate() + 30);
        const renewal = joinDate.toISOString().split('T')[0];
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="text-gray-500">#${m.id}</td>
            <td>
                <div class="font-bold text-white">${m.name}</div>
                <div class="text-xs text-gray-500">${m.phone}</div>
            </td>
            <td>
                <span class="plan-badge plan-${m.plan.toLowerCase()}">
                    ${m.plan}
                </span>
            </td>
            <td class="text-gray-400">${m.joinDate}</td>
            <td class="text-gray-400">${renewal}</td>
            <td>
                <button onclick="deleteMember(${m.id})" class="action-btn" title="Delete member">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </td>
        `;
        fullBody.appendChild(row);
    });
}

// ==================== MEMBER OPERATIONS ====================
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const name = document.getElementById('m-name').value.trim();
    const phone = document.getElementById('m-phone').value.trim();
    const date = document.getElementById('m-date').value;
    const plan = document.getElementById('m-plan').value;
    const gender = document.getElementById('m-gender').value;
    
    // Validate
    if (!name || !phone || !date) {
        showToast('Please fill all required fields', 'error');
        return;
    }
    
    // Calculate amount
    let amount = 1000;
    if (plan === 'Pro') amount = 2500;
    if (plan === 'Elite') amount = 5000;
    
    const newMember = {
        id: members.length > 0 ? Math.max(...members.map(m => m.id)) + 1 : 1,
        name,
        phone,
        plan,
        amount,
        joinDate: date,
        gender
    };
    
    try {
        // Try to add via backend
        const response = await fetch(`${API_BASE}/members`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newMember)
        });
        
        if (response.ok) {
            const savedMember = await response.json();
            members.push(savedMember);
        } else {
            // Add locally if backend fails
            members.push(newMember);
        }
    } catch (err) {
        // Add to local state if backend unavailable
        members.push(newMember);
    }
    
    // Save and refresh
    await saveMembers();
    
    // Reset form
    event.target.reset();
    document.getElementById('m-date').valueAsDate = new Date();
    
    showToast('Member registered successfully!', 'success');
    refreshData();
    showSection('dashboard');
}

async function deleteMember(id) {
    if (!confirm('Are you sure you want to delete this member?')) {
        return;
    }
    
    try {
        // Try to delete via backend
        await fetch(`${API_BASE}/members/${id}`, {
            method: 'DELETE'
        });
    } catch (err) {
        // Silently continue if backend unavailable
    }
    
    // Remove from local state
    members = members.filter(m => m.id !== id);
    
    await saveMembers();
    refreshData();
    showToast('Member deleted', 'success');
}

// ==================== SEARCH ====================
function searchMembers() {
    const searchInput = document.getElementById('search-input');
    const tableBody = document.getElementById('full-members-body');
    
    if (!searchInput || !tableBody) return;
    
    const searchTerm = searchInput.value.toLowerCase();
    const rows = tableBody.getElementsByTagName('tr');
    let hasVisible = false;
    
    Array.from(rows).forEach(row => {
        const nameCell = row.getElementsByTagName('td')[1];
        if (nameCell) {
            const textContent = nameCell.textContent.toLowerCase();
            if (textContent.includes(searchTerm)) {
                row.style.display = '';
                hasVisible = true;
            } else {
                row.style.display = 'none';
            }
        }
    });
    
    // Show/hide no results message
    const noResult = document.getElementById('no-result');
    if (noResult) {
        if (hasVisible) {
            noResult.classList.remove('show');
        } else {
            noResult.classList.add('show');
        }
    }
}

// ==================== NOTIFICATIONS ====================
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    if (!toast) return;
    
    const toastMsg = document.getElementById('toast-msg');
    if (toastMsg) {
        toastMsg.textContent = message;
    }
    
    toast.classList.remove('hide', 'error');
    if (type === 'error') {
        toast.classList.add('error');
    }
    
    // Auto hide after 3 seconds
    setTimeout(() => {
        toast.classList.add('hide');
    }, 3000);
}

function showError(element, message) {
    if (!element) return;
    const errorMsg = element.querySelector('span') || element;
    if (errorMsg) {
        errorMsg.textContent = message;
    }
    element.classList.add('show');
}

function shakeElement(element) {
    if (!element) return;
    element.classList.add('animate-pulse');
    setTimeout(() => {
        element.classList.remove('animate-pulse');
    }, 500);
}

// ==================== REFRESH ====================
function refreshData() {
    renderDashboard();
    renderMembersList();
}

// ==================== UTILITIES ====================
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-IN', options);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

// Handle window resize for responsive sidebar
window.addEventListener('resize', () => {
    if (window.innerWidth >= 768) {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.remove('hidden');
        }
    }
});
