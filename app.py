import os
from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

SAMPLE_ROWS = [
    ('Normal','R1',5,20,2,'Nearest Route'),('Normal','R2',7,15,1,'Greedy'),('Normal','R3',9,25,5,'Nearest Route'),('Normal','R4',6,22,3,'Greedy'),
    ('Heavy Traffic','R1',5,35,4,'Nearest Route'),('Heavy Traffic','R2',7,22,2,'Greedy'),('Heavy Traffic','R3',9,40,6,'Nearest Route'),('Heavy Traffic','R4',6,30,3,'Greedy'),
    ('Rainy Weather','R1',5,28,3,'Nearest Route'),('Rainy Weather','R2',7,24,2,'Greedy'),('Rainy Weather','R3',9,32,5,'Nearest Route'),('Rainy Weather','R4',6,27,2,'Greedy')
]

def db_configured():
    return all(os.getenv(k) for k in ['DB_HOST','DB_USER','DB_PASSWORD','DB_NAME'])

def get_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'), database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT','3306'))
    )

def get_rows():
    if not db_configured():
        return SAMPLE_ROWS, 'Sample dataset (MySQL connection not configured)'
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT scenario, route_id, distance_km, time_min, penalty, algorithm FROM route_benchmarks ORDER BY FIELD(scenario, \'Normal\', \'Heavy Traffic\', \'Rainy Weather\'), route_id')
        rows = cur.fetchall()
        cur.close(); conn.close()
        return (rows if rows else SAMPLE_ROWS), ('MySQL database' if rows else 'MySQL connected; table is empty, showing sample dataset')
    except Error as e:
        return SAMPLE_ROWS, 'Sample dataset (MySQL connection error: ' + str(e) + ')'

def pareto(rows):
    result=[]
    for r in rows:
        dominated=False
        for other in rows:
            if other is r: continue
            if other[2] <= r[2] and other[3] <= r[3] and (other[2] < r[2] or other[3] < r[3]):
                dominated=True; break
        if not dominated: result.append(r)
    return result

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data')
def api_data():
    rows, source = get_rows()
    scenario=request.args.get('scenario','All')
    filtered=[r for r in rows if scenario=='All' or r[0]==scenario]
    avg=lambda i: round(sum(float(r[i]) for r in filtered)/len(filtered),2) if filtered else 0
    best=sorted(filtered,key=lambda r:(r[2],r[3],r[4]))
    pareto_rows=[]
    for s in ['Normal','Heavy Traffic','Rainy Weather']:
        group=[r for r in rows if r[0]==s]
        pareto_rows += pareto(group)
    return jsonify({
        'rows':[dict(scenario=r[0],route_id=r[1],distance_km=float(r[2]),time_min=float(r[3]),penalty=float(r[4]),algorithm=r[5]) for r in filtered],
        'source':source,'count':len(filtered),'avg_distance':avg(2),'avg_time':avg(3),'avg_penalty':avg(4),
        'best':dict(scenario=best[0][0],route_id=best[0][1],distance_km=float(best[0][2]),time_min=float(best[0][3]),penalty=float(best[0][4]),algorithm=best[0][5]) if best else None,
        'pareto':[dict(scenario=r[0],route_id=r[1],distance_km=float(r[2]),time_min=float(r[3])) for r in pareto_rows if scenario=='All' or r[0]==scenario]
    })

@app.route('/api/routes', methods=['POST'])
def add_route():
    if not db_configured():
        return jsonify(error='MySQL is not configured yet. Add DB_HOST, DB_USER, DB_PASSWORD and DB_NAME environment variables first.'), 400
    data=request.get_json(force=True)
    required=['scenario','route_id','distance_km','time_min','penalty','algorithm']
    if any(k not in data for k in required): return jsonify(error='Please provide all six fields.'),400
    try:
        conn=get_connection(); cur=conn.cursor()
        cur.execute('INSERT INTO route_benchmarks (scenario, route_id, distance_km, time_min, penalty, algorithm) VALUES (%s,%s,%s,%s,%s,%s)', tuple(data[k] for k in required))
        conn.commit(); cur.close(); conn.close()
        return jsonify(message='Route saved to MySQL successfully.'),201
    except (Error, ValueError) as e:
        return jsonify(error=str(e)),400

@app.route('/health')
def health():
    return jsonify(status='ok', mysql_configured=db_configured())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT','5000')), debug=False)
