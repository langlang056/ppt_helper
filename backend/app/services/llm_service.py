"""LLM service supporting multiple providers (Anthropic Claude and Google Gemini)."""
from typing import Optional
from enum import Enum
import anthropic
import google.generativeai as genai
from app.config import get_settings

settings = get_settings()


class LLMProvider(str, Enum):
    """Supported LLM providers."""
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"


class LLMService:
    """Unified LLM service interface."""

    def __init__(self, provider: Optional[LLMProvider] = None):
        """
        Initialize LLM service with specified provider.

        Args:
            provider: LLM provider to use. Defaults to settings.llm_provider
        """
        self.provider = provider or LLMProvider(settings.llm_provider)

        # Initialize clients based on provider
        if self.provider == LLMProvider.ANTHROPIC:
            self.anthropic_client = anthropic.Anthropic(
                api_key=settings.anthropic_api_key
            )
        elif self.provider == LLMProvider.GEMINI:
            genai.configure(api_key=settings.gemini_api_key)
            self.gemini_model = genai.GenerativeModel(settings.gemini_model)

    async def generate_text(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate text using configured LLM provider.

        Args:
            prompt: User prompt/query
            system_message: System instructions (optional)
            temperature: Sampling temperature (optional, uses settings default)
            max_tokens: Maximum tokens to generate (optional, uses settings default)

        Returns:
            Generated text response
        """
        temperature = temperature or settings.temperature
        max_tokens = max_tokens or settings.max_tokens

        if self.provider == LLMProvider.ANTHROPIC:
            return await self._generate_anthropic(
                prompt, system_message, temperature, max_tokens
            )
        elif self.provider == LLMProvider.GEMINI:
            return await self._generate_gemini(
                prompt, system_message, temperature, max_tokens
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    async def _generate_anthropic(
        self,
        prompt: str,
        system_message: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Generate text using Anthropic Claude."""
        messages = [{"role": "user", "content": prompt}]

        kwargs = {
            "model": settings.claude_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if system_message:
            kwargs["system"] = system_message

        response = self.anthropic_client.messages.create(**kwargs)
        return response.content[0].text

    async def _generate_gemini(
        self,
        prompt: str,
        system_message: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Generate text using Google Gemini."""
        # Combine system message with prompt if provided
        full_prompt = prompt
        if system_message:
            full_prompt = f"{system_message}\n\n{prompt}"

        # Configure generation settings
        generation_config = genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )

        # Generate response
        response = await self.gemini_model.generate_content_async(
            full_prompt,
            generation_config=generation_config,
        )

        return response.text

    def get_provider_info(self) -> dict:
        """Get information about current provider."""
        return {
            "provider": self.provider.value,
            "model": (
                settings.claude_model
                if self.provider == LLMProvider.ANTHROPIC
                else settings.gemini_model
            ),
            "temperature": settings.temperature,
            "max_tokens": settings.max_tokens,
        }


# Global instance (can be reconfigured)
llm_service = LLMService()
