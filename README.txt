ROUTE OPTIMIZATION BENCHMARK STORE - WEB APP

WHAT IS INCLUDED
- app.py: Python Flask backend and API
- templates/index.html: responsive blue dashboard
- schema.sql: MySQL database/table and the 12 sample records
- requirements.txt: Python packages

IMPORTANT
The dashboard uses the 12 supplied sample records if MySQL credentials are not configured. It reads from MySQL and saves new routes to MySQL only after the hosting environment variables are configured. No database password is included in these files.

RUN LOCALLY / ON A PYTHON HOST
1. Upload this folder to a Python hosting workspace (for example, Replit).
2. Install packages from requirements.txt.
3. Run schema.sql in your MySQL database ONLY if the table/data do not already exist. If the 12 rows are already inserted, do not run the INSERT statements again, or duplicate rows may be created.
4. Set environment variables in the host's Secrets/Environment settings:
   DB_HOST = your MySQL host
   DB_PORT = 3306 (or the port supplied by your provider)
   DB_USER = your MySQL username
   DB_PASSWORD = your MySQL password
   DB_NAME = RouteOptimization
5. Start command: python app.py
6. Open the web preview. The dashboard calls the Flask API at /api/data.

NOTE ABOUT SQL MASTER
A MySQL database inside a phone app may not be reachable from a hosted website. You need a MySQL server with remote/network access enabled and connection details from its provider. Do not publish your password or put it in frontend HTML/JavaScript.

ANALYSIS RULE
Best route uses a simple distance-first heuristic: sort by distance, then time, then penalty. It is not a road-network shortest-path algorithm. Algorithm names in the sample dataset are labels, not independently implemented algorithm engines. Penalty values are illustrative sample values.
