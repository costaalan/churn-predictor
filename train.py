import sqlite3, joblib, json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

db=sqlite3.connect('/opt/data/painel/churn.db')
cur=db.cursor()

# Feature engineering: junta clientes + uso
cur.execute('''
SELECT c.id,c.idade,c.churn,
       u.sessoes,u.mins,u.erros,u.tickets,u.satisfacao,
       CASE c.plano WHEN 'Basic' THEN 1 WHEN 'Pro' THEN 2 WHEN 'Enterprise' THEN 3 ELSE 1 END as plano_num,
       CASE c.cidade WHEN 'SP' THEN 1 WHEN 'RJ' THEN 2 WHEN 'BH' THEN 3 ELSE 4 END as cidade_num
FROM clientes c JOIN uso u ON c.id=u.cliente_id
''')
rows=cur.fetchall()
db.close()

X=np.array([[r[1],r[3],r[4],r[5],r[6],r[7],r[8],r[9]] for r in rows])
y=np.array([r[2] for r in rows])

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

model=RandomForestClassifier(n_estimators=100,max_depth=6,random_state=42)
model.fit(X_train,y_train)

# Métricas
y_pred=model.predict(X_test)
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
acc=accuracy_score(y_test,y_pred)
prec=precision_score(y_test,y_pred)
rec=recall_score(y_test,y_pred)
f1=f1_score(y_test,y_pred)

# Feature importance
features=['idade','sessoes','mins','erros','tickets','satisfacao','plano_num','cidade_num']
importances={features[i]:round(model.feature_importances_[i],3) for i in range(len(features))}

result={
    'modelo':'RandomForest',
    'clientes':len(rows),
    'churns':int(sum(y)),
    'taxa_churn':round(100*sum(y)/len(y),1),
    'metrics':{'accuracy':round(acc,3),'precision':round(prec,3),'recall':round(rec,3),'f1':round(f1,3)},
    'top_features':sorted(importances.items(),key=lambda x:x[1],reverse=True)[:5]
}

print(json.dumps(result,indent=2))
joblib.dump(model,'/opt/data/painel/churn_model.pkl')
print('\n✅ Modelo salvo: churn_model.pkl')
