# Travel Deal Management API

A Flask-based REST API for managing travel deals, supporting creation and retrieval of deals with validation and error handling.

## Tech Stack

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite

## Project Structure

```
travel-deal-management-api-moynul/
├── app.py                     # Application entry point and app factory
├── routes/
│   ├── __init__.py            # Blueprint exports
│   ├── system_routes.py       # Health check route
│   └── deal_routes.py          # Travel deal routes
├── services/
│   └── deal_service.py        # Business logic for travel deals
├── utils/
│   └── validators.py          # Request payload validation
├── database/
│   ├── __init__.py            # Database exports
│   └── models.py              # SQLAlchemy models
├── constants/
│   ├── __init__.py            # Constants exports
│   └── validation.py          # Validation rules and constraints
├── postman/
│   └── TravelDealManagementPostmanCollection.json  # Postman collection
├── requirements.txt           # Python dependencies
├── .env.example                # Sample environment variables
└── README.md
```

## Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/200215-Moynul-Islam/travel-deal-management-api-moynul.git
cd travel-deal-management-api-moynul
```

2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure environment variables

Copy `.env.example` to `.env` and adjust values if needed.

```bash
cp .env.example .env
```

5. Run the application

```bash
python3 app.py
```

The server will start at `http://localhost:5000`.

## API Endpoints

### Health Check

```
GET /health
```

```bash
curl http://localhost:5000/health
```

### Add a Travel Deal

```
POST /deals
```

```bash
curl -X POST http://localhost:5000/deals -H "Content-Type: application/json" -d '{"destination":"Dubai","price":5000,"platform":"Booking","rating":4.5,"travel_type":"Luxury"}'
```

**Request Body**

```json
{
  "destination": "Dubai",
  "price": 5000,
  "platform": "Booking",
  "rating": 4.5,
  "travel_type": "Luxury"
}
```

**Validation Rules**

- `destination` cannot be empty
- `price` must be a positive number
- `rating` must be between 1 and 5
- `travel_type` must be one of: `Budget`, `Luxury`, `Adventure`, `Family`

### Get All Deals

```
GET /deals
```

```bash
curl http://localhost:5000/deals
```

### Get a Single Deal

```
GET /deals/<id>
```

```bash
curl http://localhost:5000/deals/1
```

## Response Format

```json
{
  "status": "success",
  "data": {}
}
```

```json
{
  "status": "error",
  "message": "Error description"
}
```

## Postman Collection

A Postman collection is included at `postman/TravelDealManagementPostmanCollection.json`.

To use it:

1. Open Postman
2. Click **Import**
3. Select the JSON file from the `postman` folder
