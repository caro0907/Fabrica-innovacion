# Personal Wealth Architect · MVP v1

Aplicación web del arquitecto de patrimonio con datos ficticios: la primera reunión, el plan, la app como hogar del plan, la recomendación con transparencia, las reglas, el consultor y el motor por dentro. El traspaso completo está en `../HANDOFF.md`.

## Correrlo en local
```bash
cd ideas/personal-wealth-architect/app
pip install -r requirements-dev.txt
uvicorn pwa.app:app --reload --port 8000     # abre http://localhost:8000
python -m pytest                              # 41 pruebas
```
Revisión en navegador real (capturas y toques de 44 px):
```bash
python scripts/revisar_pantallas.py http://localhost:8000 capturas
```

## Variables de entorno
| Variable | Para qué | Obligatoria |
|---|---|---|
| `PWA_CLAVE_INTERNA` | Clave de las vistas del consultor y del motor | Sí en Railway |
| `PWA_COOKIE_SEGURA` | `1` para cookies solo por HTTPS | Sí en Railway |
| `PWA_DB` | Ruta del archivo SQLite (en Railway, dentro del volumen: `/data/pwa.sqlite`) | Sí en Railway |
| `ANTHROPIC_API_KEY` | Activa la redacción con Claude dentro del catálogo; sin ella usa plantillas | No |
| `PWA_MODELO` | Modelo de Claude (por defecto `claude-haiku-5-5`) | No |
| `PWA_TOKEN_AGENTES` | Token de la consulta de solo lectura para agentes externos (`GET /api/v1/plan`) | No |

## Estructura
```
pwa/
  motor/        cálculos, plan, perfil, escenarios, decisión con cinco campos, mandatos, supuestos versionados
  catalogo/     catálogo de lo que se puede decir (JSON versionado) y su control
  redactor.py   plantillas o Claude, siempre dentro del catálogo
  registro.py   SQLite: sesiones, registro de interacciones, mandatos, métricas del freno
  app.py        rutas web y API
  templates/    pantallas (sistema de diseño de empresa/activos/tokens.json)
tests/          motor, flujo completo y redactor
scripts/        revisión en navegador
```
