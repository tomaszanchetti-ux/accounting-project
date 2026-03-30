# Demo Seed Dataset

Seed inicial reproducible del dataset demo del MVP.

## Archivos generados

- `payroll.csv`
- `expected_totals.csv`
- `concept_master.csv`
- `employee_reference.csv`

## Regeneracion

```bash
cd /Users/tzanchetti/Documents/Proyectos\ Claudio/accounting-project
python3 data/demo_seed/generate_dataset.py
```

El script es determinista y vuelve a escribir los archivos CSV del seed.
