#!/bin/bash
set -euo pipefail

if [ -v MIGRATE ]; then
    alembic upgrade head
fi

exec python -m parking_scraper
