import random, sqlite3, json
random.seed(42)

db=sqlite3.connect('/opt/data/painel/churn.db')
cur=db.cursor()
cur.execute('DROP TABLE IF EXISTS clientes')
cur.execute('DROP TABLE IF EXISTS uso')
cur.execute('CREATE TABLE clientes(id INTEGER PRIMARY KEY,nome TEXT,plano TEXT,cidade TEXT,segmento TEXT,idade INTEGER,churn INTEGER)')
cur.execute('CREATE TABLE uso(id INTEGER PRIMARY KEY,cliente_id INTEGER,sessoes REAL,mins REAL,erros INTEGER,tickets INTEGER,satisfacao REAL)')

N=1000
planos=['Basic','Pro','Enterprise','Starter']
cidades=['SP','RJ','BH','Curitiba','POA','Recife','Fortaleza']
segs=['Tecnologia','Financas','Saude','Educacao','Varejo']

print(f'Gerando {N} clientes...')
for i in range(N):
    c=1 if random.random()<0.22 else 0
    cur.execute('INSERT INTO clientes VALUES(?,?,?,?,?,?,?)',
        (i+1,f'Cliente_{i+1}',random.choice(planos),random.choice(cidades),random.choice(segs),random.randint(22,65),c))
    s=max(0,round(random.gauss(5 if c==0 else 1.8,2),2))
    m=max(0,round(random.gauss(42 if c==0 else 9,15),1))
    e=random.randint(0,2)if c==0 else random.randint(3,7)
    t=random.randint(0,2)if c==0 else random.randint(3,6)
    st=min(5,max(1,round(random.gauss(4.1 if c==0 else 2.3,1),1)))
    cur.execute('INSERT INTO uso VALUES(?,?,?,?,?,?,?)',(i+1,i+1,s,m,e,t,st))

cur.execute('SELECT COUNT(*),SUM(churn),ROUND(100.0*SUM(churn)/COUNT(*),1) FROM clientes')
r=cur.fetchone()
db.commit()
db.close()
print(f'✅ {r[0]} clientes | {r[1]} churns ({r[2]}%) | churn.db criado')
