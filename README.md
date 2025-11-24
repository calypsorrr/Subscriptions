# Subscription Manager

A modern, full-stack application to track and manage all your subscriptions in one place. Features automatic subscription discovery, beautiful UI, and comprehensive subscription management.

## Features

- 📊 **Dashboard Overview**: See all your subscriptions at a glance with statistics
- 🔍 **Auto-Discovery**: Automatically discover subscriptions from your emails
- ➕ **Manual Entry**: Add subscriptions manually with detailed information
- 💰 **Cost Tracking**: Track monthly and yearly costs with multiple currency support
- 🎨 **Modern UI**: Beautiful, responsive interface with glassmorphism design
- 🗑️ **Easy Cancellation**: Quick access to cancel subscriptions
- 🔎 **Search**: Search through your subscriptions quickly

## Tech Stack

### Backend
- **FastAPI**: Modern, fast Python web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Lightweight database (can be upgraded to PostgreSQL)

### Frontend
- **React 18**: Modern React with hooks
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icon library
- **Axios**: HTTP client

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- macOS/Linux:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

1. **Start both servers** (backend and frontend)
2. **Open your browser** to `http://localhost:3000`
3. **Add subscriptions** manually or use the "Auto-Discover" feature
4. **Manage subscriptions** by viewing, editing, or cancelling them

## Auto-Discovery Feature

The auto-discovery feature currently uses mock data for demonstration. To enable real email parsing:

1. **Gmail Integration**: 
   - Set up Google Cloud credentials
   - Enable Gmail API
   - Update `email_parser.py` with your credentials

2. **Outlook Integration**:
   - Set up Microsoft Azure credentials
   - Enable Microsoft Graph API
   - Update `email_parser.py` with your credentials

## API Endpoints

- `GET /api/subscriptions` - Get all subscriptions
- `GET /api/subscriptions/{id}` - Get a specific subscription
- `POST /api/subscriptions` - Create a new subscription
- `PUT /api/subscriptions/{id}` - Update a subscription
- `DELETE /api/subscriptions/{id}` - Delete a subscription
- `POST /api/subscriptions/discover` - Discover subscriptions from emails
- `GET /api/subscriptions/stats/summary` - Get subscription statistics

## Project Structure

```
Subscriptions/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py             # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas
│   ├── email_parser.py       # Email parsing logic
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main app component
│   │   ├── components/       # React components
│   │   └── index.css         # Global styles
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite configuration
└── README.md
```

## Future Enhancements

- [ ] Real email API integration (Gmail, Outlook)
- [ ] Browser extension for automatic detection
- [ ] Export to CSV/PDF
- [ ] Email notifications for upcoming renewals
- [ ] Category/tag system
- [ ] Dark mode toggle
- [ ] Multi-user support
- [ ] Mobile app

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

