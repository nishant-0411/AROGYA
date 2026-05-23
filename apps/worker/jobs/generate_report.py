from apps.worker.queues.celery_app import celery_app

@celery_app.task(name="apps.worker.jobs.generate_report")
def generate_report_task(payload: dict):
    query = payload.get("user_query", "")
    summary = payload.get("case_summary", "")
    docs = payload.get("retrieved_docs", [])
    image_paths = payload.get("image_paths", [])
    verification = payload.get("verification_score", 0.0)
    final_answer = payload.get("final_report", "")
    
    docs_text = "\n".join(docs) if docs else "No evidence retrieved."
    images_text = "\n".join(image_paths) if image_paths else "No images provided."
    
    report_content = f"""Medical Report

        User Query: {query}
        Input Summary: {summary}
        Retrieved Evidence:
        {docs_text}
        Image Findings:
        {images_text}
        Cross-check and Verification: Score {verification}
        Final Synthesized Answer: {final_answer}
        Confidence Level: Pending Assessment
        Limitations and Disclaimer: This is an AI-generated research summary, not clinical advice.
        Citations: Pending
        """

    return {
        "status": "success",
        "report_content": report_content
    }
