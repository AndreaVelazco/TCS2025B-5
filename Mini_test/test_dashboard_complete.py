#!/usr/bin/env python3
"""
Test script para validar el flujo completo de ingresos/gastos en el dashboard.
Prueba: Login -> Obtener Dashboard -> Crear Ingreso -> Crear Gasto -> Verificar totales
"""

import urllib.request
import json
from datetime import datetime

print("\n" + "=" * 60)
print("TEST: FLUJO COMPLETO DE DASHBOARD")
print("=" * 60 + "\n")

# 1. LOGIN
print("[1] INICIANDO SESIÓN...")
try:
    url = 'http://127.0.0.1:8000/api/token/'
    data = json.dumps({'correo': 'test@test.com', 'password': '123'}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        token = result['access']
        print(f"✓ Login exitoso\n")
except Exception as e:
    print(f"✗ Error en login: {e}\n")
    exit(1)

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# 2. OBTENER DASHBOARD INICIAL
print("[2] OBTENIENDO DASHBOARD INICIAL...")
try:
    req = urllib.request.Request(
        'http://127.0.0.1:8000/api/finanzas/dashboard/',
        headers=headers
    )
    with urllib.request.urlopen(req) as resp:
        initial_dashboard = json.loads(resp.read().decode('utf-8'))
        print(f"✓ Dashboard obtenido")
        print(f"  Ingresos iniciales: S/. {initial_dashboard['total_ingresos']}")
        print(f"  Gastos iniciales: S/. {initial_dashboard['total_gastos']}")
        print(f"  Balance inicial: S/. {initial_dashboard['balance']}\n")
except Exception as e:
    print(f"✗ Error al obtener dashboard: {e}\n")
    exit(1)

# 3. CREAR INGRESO
print("[3] CREANDO INGRESO (S/. 2500)...")
try:
    ingreso_data = {
        'tipo': 'ingreso',
        'monto': 2500.00,
        'categoria': 'salario',
        'descripcion': 'Salario test'
    }
    req = urllib.request.Request(
        'http://127.0.0.1:8000/api/finanzas/dashboard/',
        data=json.dumps(ingreso_data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    with urllib.request.urlopen(req) as resp:
        created_ingreso = json.loads(resp.read().decode('utf-8'))
        print(f"✓ Ingreso creado (ID {created_ingreso['id_registro']})")
        print(f"  Monto: S/. {created_ingreso['monto']}\n")
except Exception as e:
    print(f"✗ Error al crear ingreso: {e}\n")
    exit(1)

# 4. CREAR GASTO
print("[4] CREANDO GASTO (S/. 800)...")
try:
    gasto_data = {
        'tipo': 'gasto',
        'monto': 800.00,
        'categoria': 'alimentacion',
        'descripcion': 'Comida test'
    }
    req = urllib.request.Request(
        'http://127.0.0.1:8000/api/finanzas/dashboard/',
        data=json.dumps(gasto_data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    with urllib.request.urlopen(req) as resp:
        created_gasto = json.loads(resp.read().decode('utf-8'))
        print(f"✓ Gasto creado (ID {created_gasto['id_registro']})")
        print(f"  Monto: S/. {created_gasto['monto']}\n")
except Exception as e:
    print(f"✗ Error al crear gasto: {e}\n")
    exit(1)

# 5. OBTENER DASHBOARD ACTUALIZADO
print("[5] OBTENIENDO DASHBOARD ACTUALIZADO...")
try:
    req = urllib.request.Request(
        'http://127.0.0.1:8000/api/finanzas/dashboard/',
        headers=headers
    )
    with urllib.request.urlopen(req) as resp:
        updated_dashboard = json.loads(resp.read().decode('utf-8'))
        print(f"✓ Dashboard actualizado")
        print(f"  Ingresos nuevos: S/. {updated_dashboard['total_ingresos']}")
        print(f"  Gastos nuevos: S/. {updated_dashboard['total_gastos']}")
        print(f"  Balance nuevo: S/. {updated_dashboard['balance']}\n")
except Exception as e:
    print(f"✗ Error al obtener dashboard actualizado: {e}\n")
    exit(1)

# 6. VALIDAR CAMBIOS
print("[6] VALIDANDO CAMBIOS...")
ingresos_diff = updated_dashboard['total_ingresos'] - initial_dashboard['total_ingresos']
gastos_diff = updated_dashboard['total_gastos'] - initial_dashboard['total_gastos']
balance_diff = updated_dashboard['balance'] - initial_dashboard['balance']

print(f"  Ingresos agregados: S/. {ingresos_diff} (esperado: 2500)")
print(f"  Gastos agregados: S/. {gastos_diff} (esperado: 800)")
print(f"  Balance cambió: S/. {balance_diff} (esperado: 1700)\n")

# Validar
if abs(ingresos_diff - 2500) < 0.01 and abs(gastos_diff - 800) < 0.01:
    print("✓ PRUEBA EXITOSA: Los totales se calcularon correctamente")
    print(f"  - Registros recientes: {len(updated_dashboard['registros_recientes'])} registros")
    print(f"  - Categorías: {len(updated_dashboard['resumen_por_categoria'])} categorías con movimiento")
else:
    print("✗ ERROR: Los totales no coinciden")

print("\n" + "=" * 60 + "\n")
