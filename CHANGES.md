
# CHANGES.md

## ✅ Major Issues Identified in the Initial Code

1. **SQL Injection Vulnerability**  
   - Raw SQL queries were constructed using f-strings, which opened the application to SQL injection attacks.

2. **No Input Validation**  
   - User input (e.g., name, email, password) was accepted without any checks for format or emptiness.

3. **Passwords Stored in Plain Text**  
   - User passwords were stored without hashing, making user data insecure.

4. **Inconsistent and Insecure JSON Parsing**  
   - `request.get_data()` was used with `json.loads()`, making the code error-prone and less readable.

5. **Lack of Proper Error Handling**  
   - Functions lacked `try-except` blocks, meaning that any error could crash the server.

6. **Missing or Poor HTTP Status Codes**  
   - Responses lacked appropriate status codes, which is bad practice for APIs.

7. **Duplicate Email Handling Ignored**  
   - No check was performed to ensure that duplicate emails weren't registered.

8. **Hardcoded and Unsafe String Comparisons**  
   - Email comparisons didn't account for case differences, and data was not normalized.

---

## 🔧 Changes Made and Why

1. **Used Parameterized Queries**
   - Replaced raw SQL queries with parameterized ones using `?` to prevent SQL injection.

2. **Implemented Field Validation Utility**
   - Added `field_validation()` to ensure all user fields are non-empty and trimmed.

3. **Hashed Passwords Using `werkzeug.security`**
   - Passwords are now stored securely using `generate_password_hash()` and verified using `check_password_hash()`.

4. **Used `request.get_json(force=True)`**
   - Replaced `request.get_data()` with a safer and cleaner JSON parsing method.

5. **Standardized API Responses**
   - Every endpoint now returns a JSON response with `status`, `status_code`, and helpful messages.

6. **Improved Duplicate Email Handling**
   - Added checks to prevent the use of an existing email address during both creation and update.

7. **Handled All Errors Gracefully**
   - Added `try-except` blocks to every route to return consistent error messages and avoid crashes.

8. **Normalized Emails to Lowercase**
   - Converted emails to lowercase before saving and comparing for consistency and to prevent duplicate entries.

---

## ⚖️ Assumptions and Trade-Offs

- Assumed email case-insensitivity while checking for duplicates.
- Did not add pagination or filtering to the `/users` endpoint due to time constraints.
- Assumed SQLite for simplicity; in production, PostgreSQL or MySQL would be preferred.
- Did not implement authentication tokens or sessions, assuming the scope was limited to basic CRUD and login.

---

## ⏳ If More Time Was Available

1. **Implement Token-Based Authentication**
   - Use JWT (JSON Web Tokens) or Flask-Login for secure session management.

2. **Input Format Validation**
   - Use regex or libraries (e.g., `email_validator`) to validate email format, password strength, etc.

3. **Rate Limiting and Throttling**
   - Prevent brute-force login attempts by adding rate limiting (e.g., using `Flask-Limiter`).

4. **Modularization and Blueprints**
   - Break the code into smaller modules using Flask Blueprints for better maintainability.

5. **Unit Tests**
   - Add test cases for all endpoints using `unittest` or `pytest`.

6. **Database Indexing and Migrations**
   - Implement indexes on frequently searched fields and use `Flask-Migrate` for schema evolution.

---

## 🤖 AI Assistance Disclosure

- **Tools Used**: ChatGPT (by OpenAI)
- **Purpose**: 
  - To generate secure password hashing and verification logic using `werkzeug.security`.
  - To document the project updates and summarize major changes in a professional format for the `CHANGES.md` file.

- **Modifications**:
  - The AI-generated code was reviewed and integrated into the project.
  - Minor adjustments were made for consistency and alignment with the project structure.
