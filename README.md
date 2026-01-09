# Appwrite Membership Function

This repository contains an Appwrite Function that manages user memberships and database access.

## 📋 Overview

This function:
- Checks if a user has team memberships
- Validates if the user has joined teams
- Verifies which databases are active
- Returns appropriate database IDs for active memberships

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your Appwrite credentials:
```
ENDPOINT=https://cloud.appwrite.io/v1
PROJECT_ID=your-project-id
API_KEY=your-api-key
```

### 3. Run Local Tests

Test with a single user:
```bash
python test_function.py
```

Run comprehensive test suite:
```bash
python test_scenarios.py
```

## 📁 Project Structure

```
.
├── main.py              # Main Appwrite function
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .env                # Your actual credentials (gitignored)
├── test_function.py    # Basic testing script
├── test_scenarios.py   # Comprehensive test suite
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## 🔧 Function Details

### Input Format
```json
{
  "$id": "user-id-here"
}
```

### Response Formats

**No memberships:**
```json
{
  "success": "false"
}
```

**User hasn't joined:**
```json
{
  "success": "false",
  "joined": "false"
}
```

**Single active database:**
```json
{
  "success": "true",
  "DATABASE_ID": "database-id"
}
```

**Multiple active databases:**
```json
{
  "success": "true",
  "DATABASE_ID": ["db-id-1", "db-id-2"]
}
```

**No active databases:**
```json
{
  "success": "false",
  "IN_ACTIVE": 2
}
```

## 🐛 Known Issues & Fixes

### Bug in Line 76
The inactive counter increments for ALL databases, not just inactive ones. 

**Current code:**
```python
for database in databases:
    isActive = isDatabaseActive(tables, database)
    if isActive:
        active_databases.append(database)
    inactive += 1  # ❌ This always increments!
```

**Fixed code:**
```python
for database in databases:
    isActive = isDatabaseActive(tables, database)
    if isActive:
        active_databases.append(database)
    else:
        inactive += 1  # ✅ Only increment when NOT active
```

## 🚀 Deploy to Appwrite

### Using Appwrite CLI

1. Install CLI:
```bash
npm install -g appwrite-cli
```

2. Login:
```bash
appwrite login
```

3. Initialize function:
```bash
appwrite init function
```

4. Deploy:
```bash
appwrite deploy function
```

### Using Appwrite Console

1. Go to your Appwrite Console
2. Navigate to **Functions** → **Create Function**
3. Choose **Python** runtime
4. Upload `main.py` and `requirements.txt`
5. Set environment variables:
   - `ENDPOINT`
   - `PROJECT_ID`
   - `API_KEY`

## 📝 Testing in Appwrite Console

Execute with test data:
```json
{
  "$id": "your-test-user-id"
}
```

## 🔐 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------||
| `ENDPOINT` | Appwrite API endpoint | `https://cloud.appwrite.io/v1` |
| `PROJECT_ID` | Your Appwrite project ID | `abc123def456` |
| `API_KEY` | API key with Users and Tables permissions | `your-secret-key` |

## 📚 Dependencies

- `appwrite==5.0.0` - Appwrite Python SDK
- `python-dotenv==1.0.0` - Environment variable management

## 🤝 Contributing

Feel free to open issues or submit pull requests!

## 📄 License

MIT License