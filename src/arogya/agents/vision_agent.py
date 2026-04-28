"""
Vision Agent

Processes medical images provided by the user (like X-rays) to extract visual findings
and feeds them into the report generation pipeline as research support.
"""

from src.arogya.orchestrator.state import AgentState

def vision_node(state: AgentState):
    image_paths = state.get("image_paths", [])
    
    if not image_paths:
        return {
            "scratchpad": "\n[Vision] No images provided. Skipping vision analysis."
        }
    
    from src.arogya.models.vision_gateway import VisionGateway
    
    # Initialize gateway (in real setup, this would be injected or instantiated once)
    gateway = VisionGateway()
    
    findings = []
    for path in image_paths:
        try:
            # Query the vision model
            finding = gateway.analyze_medical_image(path)
            findings.append(f"- Analyzed {path}:\n  {finding}")
        except Exception as e:
            findings.append(f"- Failed to analyze {path}: {str(e)}")
    
    combined_findings = "\n".join(findings)
    
    return {
        "scratchpad": f"\n[Vision] Processed {len(image_paths)} images.\nVisual Findings:\n{combined_findings}"
    }
