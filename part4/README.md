# HBnB Part 4


## Project Structure

```
part4/
├── index.html          # Main landing page / places listing
├── login.html          # User authentication page
├── place.html          # Individual place details page
├── add_review.html     # Review submission page
├── styles.css          # Global stylesheet
├── scripts.js          # Main JavaScript functionality
├── images/             # Image assets
└── README.md          
```

---

### Backend Setup

```bash
# Navigate to part3
cd ../part3

# Activate virtual environment
source venv/bin/activate

# Run the backend
python3 run.py
```

The backend should be running at: `http://127.0.0.1:5000`

### Frontend Setup

#### Option 1: Using Python HTTP Server

```bash
# Navigate to part4
cd part4

# Start a local server on port 8000
python3 -m http.server 8000
```

Then open: `http://localhost:8000`

#### Option 2: Using VS Code Live Server

1. Install "Live Server" extension in VS Code
2. Right-click `index.html`
3. Select "Open with Live Server"

---

### Pages

1. **Home/Places Listing** (`index.html`)
   - Display all available places
   - Filter by price range

2. **Login** (`login.html`)
   - User authentication
   - JWT token management

3. **Place Details** (`place.html`)
   - Detailed place information
   - Amenities list
   - Reviews section
   - Add review functionality (authenticated users)

4. **Add Review** (`add_review.html`)
   - Review form
   - Star rating system
   - Form validation
   - Authentication required
