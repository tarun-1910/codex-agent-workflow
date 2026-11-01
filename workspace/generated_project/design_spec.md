# Expense Tracker — Design Specification

## 1. Project Overview

The Expense Tracker is a single-user web application for recording daily expenses and reviewing spending over time. Users can add, view, edit, and delete expenses; assign each expense to a category; and see monthly totals and category breakdowns.

The MVP uses a browser-based frontend built with HTML, CSS, and JavaScript, a Python FastAPI backend, and SQLite for persistent storage. Backend behavior is verified with Pytest.

### Scope

- Manage expenses with an amount, date, category, and optional description.
- Show recorded expenses in a list.
- Calculate total spending for a selected month.
- Show spending grouped by category for that month.
- Validate inputs and provide clear success and error feedback.

### Out of scope

The requirements do not specify user accounts, multiple currencies, budgets, recurring transactions, data export, or shared access. These are excluded from the MVP.

## 2. Application Architecture

The application has three parts:

1. **Frontend:** HTML provides page structure, CSS provides layout and styling, and JavaScript handles interactions and API requests.
2. **Backend:** FastAPI exposes JSON endpoints, validates requests, applies expense and summary logic, and accesses the database.
3. **Database:** SQLite stores expense records persistently in a local database file.

```text
Browser
  ├── HTML and CSS: page structure and presentation
  └── JavaScript: form handling, rendering, API requests
          │ HTTP requests and JSON responses
          ▼
FastAPI
  ├── Routes: HTTP methods, paths, and status codes
  ├── Validation and application logic
  └── Database access
          │ SQL queries
          ▼
SQLite
  └── Expenses table
```

The browser never connects directly to SQLite. It sends requests to FastAPI, which reads or writes records and returns JSON. The frontend then updates the expense list and summaries.

For a small MVP, the frontend can be served as static files and the API can run as a local FastAPI application. The API base URL should be configurable in one frontend setting so it can be adjusted for development or deployment.

## 3. Frontend Design

### Structure

Use a single-page interface composed of:

- A page header with the application name.
- A month selector for filtering the list and summaries.
- A summary area showing the selected month's total and category spending.
- An expense form for adding or editing a record.
- An expense list with edit and delete actions.
- A status area for success, validation, and API error messages.

The interface should work at desktop and narrow mobile widths. Use semantic HTML elements and native form controls where practical, including date and number inputs.

### Interaction and state

JavaScript manages the selected month, loaded expenses, form mode (add or edit), and loading or error states. It calls the FastAPI endpoints with `fetch`, sends and receives JSON, and renders the returned data.

After a successful add, edit, or delete, refresh the affected expense list and monthly summary from the API. This keeps the displayed values aligned with persisted data. If a request fails, show a clear message and preserve the user's current form input.

### Validation and feedback

- Require amount, date, and category.
- Require the amount to be greater than zero.
- Validate the date before submitting.
- Show field-level or form-level validation messages.
- Disable or otherwise guard submission while a request is in progress to prevent accidental duplicate actions.
- Ask for confirmation before deleting an expense.
- Announce success and error messages in an accessible status region.

The backend remains authoritative for validation; frontend checks improve usability but do not replace API validation.

## 4. Backend Architecture

Organize the FastAPI backend into a small number of focused modules:

- **Routes:** Define expense and summary endpoints and their HTTP status codes.
- **Schemas:** Define request and response models, including validation constraints.
- **Services:** Implement summary calculations and any application logic that should not live in route handlers.
- **Database access:** Create connections and execute queries against SQLite.
- **Application setup:** Configure FastAPI, initialize the database schema, and mount or serve static frontend files if the project chooses to serve them from the same application.

Keep route handlers thin: validate input, call the relevant logic, and return a response. Use parameterized SQL statements for database operations. Return a consistent error format, including a human-readable message and, where useful, field details.

Suggested status codes:

- `200 OK` for successful reads and updates.
- `201 Created` for a successful expense creation.
- `204 No Content` for a successful deletion.
- `404 Not Found` when an expense ID does not exist.
- `422 Unprocessable Entity` for invalid request data.
- `500 Internal Server Error` for unexpected server failures.

## 5. Database Design

The MVP needs one table for expenses. Categories can be stored as text values on each record because the requirements do not call for user-managed categories or category metadata.

### `expenses`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | Primary key, auto-increment | Unique expense identifier |
| `amount` | NUMERIC | Not null, greater than zero | Expense amount |
| `date` | TEXT | Not null, ISO `YYYY-MM-DD` | Date the expense occurred |
| `category` | TEXT | Not null | Expense category |
| `description` | TEXT | Nullable | Optional user-provided details |
| `created_at` | TEXT | Not null | Record creation timestamp |
| `updated_at` | TEXT | Not null | Most recent update timestamp |

Use a consistent numeric representation for amounts. The implementation should avoid floating-point rounding errors in calculations; storing amounts as integer minor units (such as cents or paise) is a suitable SQLite option if the application adopts a fixed currency. Since the requirements do not specify currency, the MVP should display amounts without assuming a currency symbol until one is chosen.

Add an index on `date` to support month-filtered queries. Monthly totals and category breakdowns can be calculated with SQL aggregation over the selected date range; they do not need to be stored separately.

## 6. API Endpoint Design

All endpoints use JSON unless otherwise stated. The API is versioned under `/api` to leave room for future changes.

### Expense endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/expenses` | List expenses. Accept optional `month=YYYY-MM` to filter by month. Return records ordered by date descending, then ID descending. |
| `POST` | `/api/expenses` | Create an expense. Requires amount, date, and category; description is optional. Returns the created record with `201 Created`. |
| `GET` | `/api/expenses/{expense_id}` | Fetch one expense by ID. Returns `404` if it does not exist. |
| `PUT` | `/api/expenses/{expense_id}` | Replace an expense's editable fields. Returns the updated record or `404` if missing. |
| `DELETE` | `/api/expenses/{expense_id}` | Delete an expense. Returns `204 No Content` or `404` if missing. |

Example create request:

```json
{
  "amount": 24.5,
  "date": "2026-11-01",
  "category": "Food",
  "description": "Lunch"
}
```

Example expense response:

```json
{
  "id": 1,
  "amount": 24.5,
  "date": "2026-11-01",
  "category": "Food",
  "description": "Lunch",
  "created_at": "2026-11-01T10:30:00",
  "updated_at": "2026-11-01T10:30:00"
}
```

### Summary endpoint

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/summary?month=YYYY-MM` | Return the total and category breakdown for the requested month. The month parameter is required and must use `YYYY-MM`. |

Example response:

```json
{
  "month": "2026-11",
  "total": 124.5,
  "by_category": [
    {
      "category": "Food",
      "total": 80.0
    },
    {
      "category": "Transport",
      "total": 44.5
    }
  ]
}
```

For a month with no expenses, return a zero total and an empty `by_category` array. Both the list filter and summary calculation should use the same inclusive start and exclusive end date boundaries for the selected month.

### Validation and error response

Expense creation and update must reject missing required fields, invalid dates, and amounts that are not greater than zero. Category should not be blank after trimming whitespace. Description may be empty or omitted.

Use FastAPI's validation responses consistently. Where an application-level error response is needed, return a stable JSON shape such as:

```json
{
  "detail": "Expense not found"
}
```

## 7. UI Pages and Components

The MVP can be implemented as one page with reusable sections rather than a multi-page application.

### Main page

- **Header:** Application title and brief context.
- **Month selector:** Selects the month used for the list and summaries. Default to the current month.
- **Monthly total:** Displays the total for the selected month.
- **Category breakdown:** Displays each category and its total for the selected month.
- **Expense form:** Captures amount, date, category, and optional description. The submit button label changes between add and save when editing. Provide a cancel action while editing.
- **Expense list:** Displays date, category, description, amount, and actions for editing or deleting.
- **Feedback region:** Displays loading, success, validation, and API error messages.
- **Empty state:** Explains when the selected month has no expenses and offers a way to add one.

Categories should be consistent across entries. For the MVP, use a small predefined set in the frontend (for example, Food, Transport, Housing, Bills, Health, and Other) unless product decisions require free-text categories. The backend should still validate that the category is present and non-blank.

## 8. User Flow

### Add an expense

1. The user enters an amount, date, category, and optional description.
2. The frontend validates required values and the positive amount.
3. The frontend sends `POST /api/expenses`.
4. The backend validates the request and stores the record in SQLite.
5. The frontend shows success feedback, clears the form, and refreshes the list and summary for the relevant month.

### Edit an expense

1. The user selects Edit on an expense.
2. The frontend loads the expense values into the form and indicates edit mode.
3. The user changes values and submits the form.
4. The frontend sends `PUT /api/expenses/{expense_id}`.
5. On success, the frontend exits edit mode and refreshes the list and summary.

### Delete an expense

1. The user selects Delete on an expense and confirms the action.
2. The frontend sends `DELETE /api/expenses/{expense_id}`.
3. On success, the frontend removes the record from the displayed list and refreshes the summary.

### Review monthly spending

1. The user selects a month.
2. The frontend requests `GET /api/expenses?month=YYYY-MM` and `GET /api/summary?month=YYYY-MM`.
3. The backend returns matching expenses and aggregated totals.
4. The frontend displays the list, monthly total, and category breakdown for that month.

## 9. Folder Structure

```text
expense-tracker/
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── api.js
│       └── app.js
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── expenses.py
│   │   │   └── summary.py
│   │   └── services/
│   │       ├── __init__.py
│   │       └── summaries.py
│   └── tests/
│       ├── conftest.py
│       ├── test_expenses.py
│       └── test_summary.py
├── requirements.txt
└── README.md
```

The database file should be created at runtime in a configured, documented location and excluded from version control. Tests should use a temporary SQLite database so they do not modify the development database.

## 10. Technology Decisions

- **HTML, CSS, and JavaScript:** Satisfy the specified frontend stack and are sufficient for the MVP's form-based interactions and summaries.
- **FastAPI:** Provides typed request and response validation, JSON APIs, and generated API documentation without adding another backend framework.
- **SQLite:** Provides local persistent storage without requiring a separate database server. It is appropriate for a small, single-user MVP.
- **Pytest:** Supports focused API and database tests, including use of a temporary database for test isolation.
- **Plain JavaScript API module:** Keep HTTP request code in one place so error handling and the API base URL are consistent.
- **SQL aggregation:** Calculate monthly totals and category totals from stored records so summaries reflect additions, edits, and deletions immediately.

## 11. Design Considerations and Risks

- **Currency is unspecified:** Amounts need a consistent storage and display convention. Decide the currency before release; avoid implying a currency in the UI until then.
- **Category behavior is unspecified:** A predefined list keeps spelling consistent and simplifies summaries. Confirm the category set and whether users should be allowed to add categories before implementation.
- **Date handling:** Store dates in ISO format and use month boundaries consistently. Treat expense dates as calendar dates, avoiding timezone conversions that could shift an entry into a neighboring day.
- **SQLite concurrency and scale:** SQLite is suitable for the expected MVP use. If the application later needs many concurrent writers or multiple application instances, reassess the database choice.
- **Data backup:** A local SQLite file is persistent but can be lost with the host machine. Backup and recovery are deployment concerns if users rely on the data.
- **Input and SQL safety:** Validate values at the API boundary and use parameterized SQL. Do not build queries by concatenating user input.
- **Deletion is irreversible in the MVP:** Confirmation reduces accidental deletion. Undo or soft deletion can be considered later if users need recovery.
- **API and frontend origin:** If served from different origins during development, configure FastAPI CORS for the frontend origin. Avoid permissive production settings.
- **Testing boundaries:** Pytest should cover CRUD, validation, missing IDs, monthly boundaries, category aggregation, and persistence. Frontend flows should also be manually checked against the running API as part of integration verification.