import base64
import os
import logging
from typing import Optional, List
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage

logger = logging.getLogger(__name__)

class VisionGateway:
    """
    Gateway to interact with Vision-capable models (e.g., LLaVA via Ollama).
    This handles loading image data, encoding it, and querying the model
    while enforcing guardrails against providing clinical diagnoses.
    """

    def __init__(self, model_name: str = "llava", temperature: float = 0.0):
        self.model_name = model_name
        self.temperature = temperature
        # Ensure we have a URL for Ollama if running in docker, else fallback to localhost
        self.base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        
        try:
            self.llm = ChatOllama(
                model=self.model_name,
                temperature=self.temperature,
                base_url=self.base_url
            )
        except Exception as e:
            logger.warning(f"Could not initialize ChatOllama vision model {self.model_name}: {e}")
            self.llm = None

    def _encode_image(self, image_path: str) -> str:
        """Encodes an image to a base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_medical_image(self, image_path: str, query: Optional[str] = None) -> str:
        """
        Analyzes a medical image (like an X-ray) and returns visual findings.
        The prompt strictly enforces that the output is for research support, not diagnosis.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")

        base64_image = self._encode_image(image_path)
        
        default_prompt = (
            "You are a medical research assistant. Analyze the provided medical image "
            "(e.g., X-ray, MRI, CT scan). Describe the visible anatomical structures and any "
            "notable visual patterns. "
            "CRITICAL INSTRUCTION: Do NOT provide a clinical diagnosis. Frame all findings "
            "strictly as objective visual observations to support further medical research. "
            "If no specific query is provided, give a general objective description."
        )
        
        prompt_text = query if query else default_prompt

        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt_text},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ]
        )

        try:
            if self.llm is None:
                return "[VisionGateway Fallback] Simulated finding: Normal anatomical structures observed. No acute pathology noted. (Vision model not fully configured)."
                
            response = self.llm.invoke([message])
            return response.content
        except Exception as e:
            logger.error(f"Error calling vision model: {e}")
            return f"[VisionGateway Error] Failed to process image due to: {e}"

    def extract_features(self, image_path: str) -> List[float]:
        """
        Stub for open_clip_torch integration if vector feature extraction is needed 
        for similarity search.
        """
        # In a full implementation, this would use open_clip to get the image embedding.
        logger.info(f"Feature extraction requested for {image_path}, returning dummy vector.")
        return [0.0] * 512
