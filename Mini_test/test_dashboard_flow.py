import urllib.request
import json
from datetime import datetime

# 1. Login
print("=" * 50)
print("1. LOGIN")
print("=" * 50)

url = 'http://127.0.0.1:8000/api/token/'
data = json.dumps({'correo': 'test@test.com', 'password': '123'}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode('utf-8'))
    token = result['access']
    print(f'✓ Token obtenido: {token[:40]}...\n')

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# 2. Ver dashboard actual
print("=" * 50)
print("2. DASHBOARD INICIAL")
print("=" * 50)

req_dashboard = urllib.request.Request(
    'http://127.0.0.1:8000/api/finanzas/dashboard/',
    headers=headers
)

with urllib.request.urlopen(req_dashboard) as resp:
    dashboard = json.loads(resp.read().decode('utf-8'))
    print(f"Total Ingresos: S/. {dashboard['total_ingresos']}")
    print(f"Total Gastos: S/. {dashboard['total_gastos']}")
    print(f"Balance: S/. {dashboard['balance']}\n")

# 3. Agregar un ingreso
print("=" * 50)
print("3. AGREGAR INGRESO (S/. 1000)")
print("=" * 50)

ingreso_data = {
    'tipo': 'ingreso',
    'monto': 1000.00,
    'categoria': 'salario',
    'descripcion': 'Salario mensual'
}

req_ingreso = urllib.request.Request(
    'http://127.0.0.1:8000/api/finanzas/dashboard/',
    data=json.dumps(ingreso_data).encode('utf-8'),
    headers=headers,
    method='POST'
)

try:
    with urllib.request.urlopen(req_ingreso) as resp:
        created = json.loads(resp.read().decode('utf-8'))
        print(f"✓ Ingreso creado (ID {created['id_registro']})")
        print(f"  Tipo: {created['tipo']}")
        print(f"  Monto: S/. {created['monto']}")
        print(f"  Categoría: {created['categoria']}\n")
except urllib.error.HTTPError as e:
    print(f"✗ Error: {e.code}")
    print(f"  Response: {e.read().decode('utf-8')}\n")

# 4. Agregar un gasto
print("=" * 50)
print("4. AGREGAR GASTO (S/. 300)")
print("=" * 50)

gasto_data = {
    'tipo': 'gasto',
    'monto': 300.00,
    'categoria': 'alimentacion',
    'descripcion': 'Comida del mes'
}

req_gasto = urllib.request.Request(
    'http://127.0.0.1:8000/api/finanzas/dashboard/',
    data=json.dumps(gasto_data).encode('utf-8'),
    headers=headers,
    method='POST'
)

try:
    with urllib.request.urlopen(req_gasto) as resp:
        created = json.loads(resp.read().decode('utf-8'))
        print(f"✓ Gasto creado (ID {created['id_registro']})")
        print(f"  Tipo: {created['tipo']}")
        print(f"  Monto: S/. {created['monto']}")
        print(f"  Categoría: {created['categoria']}\n")
except urllib.error.HTTPError as e:
    print(f"✗ Error: {e.code}")
    print(f"  Response: {e.read().decode('utf-8')}\n")

# 5. Ver dashboard actualizado
print("=" * 50)
print("5. DASHBOARD ACTUALIZADO")
print("=" * 50)

req_dashboard2 = urllib.request.Request(
    'http://127.0.0.1:8000/api/finanzas/dashboard/',
    headers=headers
)

with urllib.request.urlopen(req_dashboard2) as resp:
    dashboard = json.loads(resp.read().decode('utf-8'))
    print(f"Total Ingresos: S/. {dashboard['total_ingresos']}")
    print(f"Total Gastos: S/. {dashboard['total_gastos']}")
    print(f"Balance: S/. {dashboard['balance']}")
    print(f"Registros recientes: {len(dashboard['registros_recientes'])}")
    
    if dashboard['resumen_por_categoria']:
        print(f"\nResumen por categoría (últimos 30 días):")
        for cat in dashboard['resumen_por_categoria']:
            print(f"  - {cat['categoria']}: S/. {cat['total']}")
    
    print(f"\n✓ PRUEBA COMPLETADA EXITOSAMENTE")
