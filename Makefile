.PHONY: check check-frontend check-backend

check: check-frontend check-backend

check-frontend:
	cd frontend && npm run lint

check-backend:
	cd backend && .venv/bin/ruff check app

