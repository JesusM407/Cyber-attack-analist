import pandas as pd
import sqlite3
from pathlib import Path

ruta_proyecto = Path.cwd()

# Buscar el CSV
csv_files = list(ruta_proyecto.rglob("*.csv"))
if csv_files:
    ruta_csv = csv_files[0]
    print(f"✅ Usando: {ruta_csv}")
    df = pd.read_csv(ruta_csv)
else:
    raise FileNotFoundError("No se encontró archivo CSV")

# Crear base de datos
db_path = ruta_proyecto / "cyber_attacks.db"
conn = sqlite3.connect(db_path)
df.to_sql('attacks', conn, if_exists='replace', index=False)
conn.close()  # Cerramos después de guardar

print("✅ Base de datos creada")

# Ahora hacemos las consultas (abriendo una nueva conexión cada vez)
def ejecutar_consulta(sql):
    conn = sqlite3.connect(db_path)
    result = pd.read_sql(sql, conn)
    conn.close()
    return result

# Distribución de ataques
df_dist = ejecutar_consulta("""
    SELECT attack_type, COUNT(*) as total, 
           ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM attacks), 2) as porcentaje
    FROM attacks
    GROUP BY attack_type
    ORDER BY total DESC
""")
print("\n📈 Distribución de ataques:")
print(df_dist)