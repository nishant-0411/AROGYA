run-api:
	uvicorn apps.api.main:app --reload

run-ui:
	streamlit run apps/ui/app.py