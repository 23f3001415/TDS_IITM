# Q12: Function Calling

## ELI15 Step-by-Step (Beginner Friendly)

1. Open PowerShell in `ga3/q12`.
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Start API + tunnel:
   ```powershell
   .\start_all.ps1
   ```
4. It prints endpoint like:
   `https://something.trycloudflare.com/execute`
5. Submit that URL.

## What It Does

- Endpoint: `GET /execute?q=...`
- Matches query to one function:
  - `get_ticket_status(ticket_id: int)`
  - `schedule_meeting(date: str, time: str, meeting_room: str)`
  - `get_expense_balance(employee_id: int)`
  - `calculate_performance_bonus(employee_id: int, current_year: int)`
  - `report_office_issue(issue_code: int, department: str)`
- Returns:
  ```json
  {"name":"function_name","arguments":"{\"arg\": value}"}
  ```
- CORS enabled for GET requests from any origin.

## Final Answer (for grader)

Read from:

`endpoint_url.txt`

Current run endpoint:

`https://expenses-genius-highly-cape.trycloudflare.com/execute`
