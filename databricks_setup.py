"""
Churn Predictor — Setup Databricks
Cria tabelas e popula dados simulados no Databricks.
"""
import random, os
random.seed(42)

# ⚠️ SUBSTITUA pelo seu token ou use dbutils.secrets.get()
TOKEN="dapi_seu_token_aqui"
HOST='dbc-75ba99ea-3667.cloud.databricks.com'
HTTP_PATH='/sql/1.0/warehouses/d2d0a2c550cdaf76'

from databricks import sql
conn = sql.connect(server_hostname=HOST, http_path=HTTP_PATH, access_token=TOKEN)
cur = conn.cursor()

cur.execute('CREATE DATABASE IF NOT EXISTS churn_predictor')
cur.execute('USE churn_predictor')

for t in ['uso','clientes']:
    try: cur.execute(f'DROP TABLE IF EXISTS {t}')
    except: pass

cur.execute('''CREATE TABLE clientes(
    id INT, nome STRING, plano STRING, cidade STRING, 
    segmento STRING, idade INT, churn INT
) USING DELTA''')

cur.execute('''CREATE TABLE uso(
    id INT, sessoes DOUBLE, mins DOUBLE, 
    erros INT, tickets INT, satisfacao DOUBLE
) USING DELTA''')

N=80
planos=['Basic','Pro','Enterprise','Starter']
print(f'Gerando {N} clientes...')

for i in range(N):
    c=1 if random.random()<0.22 else 0
    cur.execute('INSERT INTO clientes VALUES(?,?,?,?,?,?,?)',
        (i+1,f'Cliente_{i+1}',random.choice(planos),
         random.choice(['SP','RJ','BH']),
         random.choice(['Tech','Finance','Saude']),
         random.randint(22,65),c))
    cur.execute('INSERT INTO uso VALUES(?,?,?,?,?,?)',
        (i+1,
         round(random.gauss(5 if c==0 else 1.8,2),2),
         round(random.gauss(42 if c==0 else 9,15),1),
         random.randint(0,2)if c==0 else random.randint(3,7),
         random.randint(0,2)if c==0 else random.randint(3,6),
         round(random.gauss(4.1 if c==0 else 2.3,1),1)))

cur.execute('SELECT COUNT(*),SUM(churn)FROM clientes')
r=cur.fetchone()
print(f'✅ Databricks: {r[0]} clientes | {r[1]} churns | {round(100*r[1]/r[0],1)}%')
cur.close()
conn.close()
