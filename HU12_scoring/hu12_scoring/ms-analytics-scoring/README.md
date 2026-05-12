# ms-analytics-scoring - HU-12 Scoring Territorial

## Descripcion
Microservicio para calcular el score territorial y evaluar zonas.

## Estructura
- app/domain: Entidades e interfaces
- app/application: Casos de uso y calculadoras
- app/infrastructure: Repositorio JSON
- app/schemas: Contratos de entrada y salida
- app/routers: Endpoints del servicio

## Instalacion
pip install -r requirements.txt

## Ejecucion
python app/main.py

## Tests
python -m pytest app/tests/ -v

## Health Check
GET /health

## Endpoints
POST /scores/calculate
GET  /scores/executions
GET  /scores/{execution_id}
GET  /scores/{execution_id}/ranking

## Contrato API
{
  "success": true,
  "data": {},
  "error": null,
  "trace_id": ""
}
