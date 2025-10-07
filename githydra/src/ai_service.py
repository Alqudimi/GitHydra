import os
import logging
from typing import Optional, Dict, Any
from google import genai

logger = logging.getLogger(__name__)


class AIService:
    """
    AI Service for GitHydra with optional Gemini API integration.
    If API key is not available or connection fails, features work without AI.
    """
    
    def __init__(self):
        self.model = None
        self.enabled = False
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Gemini client if API key is available."""
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if api_key:
            try:
                

                 
                    
                
                    
                self.client = genai.Client(api_key=api_key)
                self.model = "gemini-1.5-flash",
                self.enabled = True
                logger.info("AI Service initialized with Gemini API")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}")
                logger.info("AI features will be disabled")
        else:
            logger.info("GEMINI_API_KEY not found - AI features disabled")
    
    def is_enabled(self) -> bool:
        """Check if AI service is enabled."""
        return self.enabled
    
    def generate_commit_message_internal(self, diff: str, files_changed: list = []) -> Optional[str]:
        """Generate commit message based on diff. Returns None if AI disabled."""
        if not self.enabled:
            return None
        
        try:
            prompt = f"""Analyze the following git diff and generate a concise, meaningful commit message.
Follow conventional commit format (feat/fix/docs/style/refactor/test/chore).

Files changed: {', '.join(files_changed) if files_changed else 'Multiple files'}

Diff:
{diff[:2000]}  

Generate a commit message with:
- A clear, concise subject line (max 50 chars)
- Optional detailed body if needed
"""
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
                )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error generating commit message: {e}")
            return None
    
    def review_code_internal(self, code: str) -> Optional[Dict[str, Any]]:
        """Review code for quality, bugs, and improvements. Returns None if AI disabled."""
        if not self.enabled:
            return None
        
        try:
            prompt = f"""Review the following code and provide:
1. Quality score (1-10)
2. Potential bugs or issues
3. Suggestions for improvement
4. Security concerns

Code:
{code[:3000]}

Respond in JSON format with keys: score, bugs, suggestions, security.
"""
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
                )
            return {'review': response.text.strip(), 'score': 7}
        except Exception as e:
            logger.error(f"Error reviewing code: {e}")
            return None
    
    def detect_bugs_internal(self, code: str) -> Optional[Dict[str, Any]]:
        """Detect potential bugs in code. Returns None if AI disabled."""
        if not self.enabled:
            return None
        
        try:
            prompt = f"""Analyze this code for bugs and issues:

{code[:3000]}

List all potential bugs with severity (high/medium/low) and description.
"""
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
                )

            return {'bugs': response.text.strip()}
        except Exception as e:
            logger.error(f"Error detecting bugs: {e}")
            return None


# Global AI service instance
ai_service = AIService()


# Wrapper functions for easy import
def generate_commit_message(diff: str, files_changed: list = []) -> str:
    """Generate commit message from diff."""
    result = ai_service.generate_commit_message_internal(diff, files_changed)
    if result:
        return result
    return "Update: Changes made to codebase"


def review_code(code: str) -> Dict[str, Any]:
    """Review code for quality and issues."""
    result = ai_service.review_code_internal(code)
    if result:
        return result
    return {'review': 'AI service not available', 'score': 0}


def detect_bugs(code: str) -> Dict[str, Any]:
    """Detect bugs in code."""
    result = ai_service.detect_bugs_internal(code)
    if result:
        return result
    return {'bugs': 'AI service not available'}


def is_ai_enabled() -> bool:
    """Check if AI features are enabled."""
    return ai_service.is_enabled()
