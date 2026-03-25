#!/usr/bin/env python3
"""
Script local para correr todos los scrapers y guardar los resultados en db.sqlite3.

Uso (desde la carpeta backend/):
    python scripts/scrape_to_db.py

El archivo db.sqlite3 generado debe commitearse para que Railway lo sirva.
"""

import os
import sys
import time
import logging

# Forzar SQLite y deshabilitar scheduler antes de importar módulos de la app
os.environ["DATABASE_URL"] = "sqlite:///db.sqlite3"
os.environ["SCHEDULER_INTERVAL_HOURS"] = "0"

# Permitir correr desde la raíz del proyecto o desde backend/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, init_db
from app.scheduler import SCRAPERS, _save_opportunities

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("scrape_to_db")


def main():
    print("\n=== EducaTYCs — Generando base de datos ===\n")

    logger.info("Inicializando db.sqlite3...")
    init_db()

    db = SessionLocal()
    total_new = 0
    total_updated = 0
    errors = []

    for name, scraper_class in SCRAPERS.items():
        t0 = time.time()
        try:
            logger.info("▶ Scraping %s...", name)
            with scraper_class() as scraper:
                opportunities = scraper.scrape()

            new_count, updated_count = _save_opportunities(db, opportunities, name)
            total_new += new_count
            total_updated += updated_count
            elapsed = time.time() - t0
            logger.info(
                "  ✓ %s: %d nuevos, %d actualizados  (%.1fs)",
                name, new_count, updated_count, elapsed,
            )
        except Exception as e:
            elapsed = time.time() - t0
            logger.error("  ✗ %s: ERROR — %s  (%.1fs)", name, e, elapsed)
            errors.append((name, str(e)))

    db.close()

    print("\n" + "=" * 50)
    print(f"  Total nuevos:      {total_new}")
    print(f"  Total actualizados:{total_updated}")
    if errors:
        print(f"\n  Errores ({len(errors)}):")
        for scraper_name, err in errors:
            print(f"    - {scraper_name}: {err}")
    print(f"\n  Base de datos: backend/db.sqlite3")
    print("=" * 50)
    print("\nPróximo paso:")
    print("  git add backend/db.sqlite3")
    print("  git commit -m 'data: actualizar cursos'")
    print("  git push\n")


if __name__ == "__main__":
    main()
