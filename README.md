# Travel Deal Management API

A Flask-based REST API for managing travel deals, supporting creation, retrieval, update, deletion, search, filtering, sorting, popularity tracking, and API usage statistics.

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
│   ├── system_routes.py       # Health check and stats routes
│   └── deal_routes.py         # Travel deal routes
├── services/
│   ├── deal_service.py        # Business logic for travel deals
│   └── system_service.py      # Business logic for API analytics
├── utils/
│   └── validators.py          # Request payload and query validation
├── database/
│   ├── __init__.py            # Database exports
│   └── models.py              # SQLAlchemy models
├── constants/
│   ├── __init__.py            # Constants exports
│   └── validation.py          # Validation rules and constraints
├── postman/
│   └── TravelDealManagementPostmanCollection.json  # Postman collection
├── requirements.txt           # Python dependencies
├── .env.example               # Sample environment variables
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

### API Usage Statistics

```
GET /stats
```

```bash
curl http://localhost:5000/stats
```

Returns total requests, successful requests, failed requests, most searched destination, and most viewed deal.

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

### Update a Travel Deal

```
PUT /deals/<id>
```

```bash
curl -X PUT http://localhost:5000/deals/1 -H "Content-Type: application/json" -d '{"destination":"Bangkok","price":3000,"platform":"Agoda","rating":4.0,"travel_type":"Budget"}'
```

Applies the same validation rules as creating a deal.

### Delete a Travel Deal

```
DELETE /deals/<id>
```

```bash
curl -X DELETE http://localhost:5000/deals/1
```

### Search Deals

```
GET /deals/search
```

Query Parameters: `destination`, `platform`, `travel_type` (at least one required, case-insensitive partial match)

```bash
curl "http://localhost:5000/deals/search?destination=dubai"
curl "http://localhost:5000/deals/search?platform=booking&travel_type=Luxury"
```

### Filter Deals by Budget

```
GET /deals/filter
```

Query Parameters: `min_price`, `max_price`

```bash
curl "http://localhost:5000/deals/filter?min_price=1000&max_price=5000"
```

**Validation Rules**

- `min_price` cannot be negative
- `max_price` cannot be smaller than `min_price`

### Sort Deals

```
GET /deals/sort
```

Query Parameters: `sort_by` (required), `order` (`asc` or `desc`, default `asc`)

```bash
curl "http://localhost:5000/deals/sort?sort_by=price&order=asc"
curl "http://localhost:5000/deals/sort?sort_by=price&order=desc"
```

**Validation Rules**

- `sort_by` is required; only `price` is supported
- `order` must be `asc` or `desc`

### Recently Viewed Deals

```
GET /deals/recent
```

```bash
curl http://localhost:5000/deals/recent
```

Returns the last 10 unique deals viewed via `GET /deals/<id>`.

### Popular Deals

```
GET /deals/popular
```

```bash
curl http://localhost:5000/deals/popular
```

Returns the top 5 most viewed deals, ranked by view count.

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

## Logging

API activity is logged to `app.log` in the project root.

| Level     | Tracked Events                                |
| --------- | --------------------------------------------- |
| `INFO`    | Successful operations, incoming requests      |
| `WARNING` | Validation failures, invalid query parameters |
| `ERROR`   | Internal server errors, failed API requests   |

## Postman Collection

A Postman collection is included at `postman/TravelDealManagementPostmanCollection.json`.

To use it:

1. Open Postman
2. Click **Import**
3. Select the JSON file from the `postman` folder
