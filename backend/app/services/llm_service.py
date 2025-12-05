"""LLM服务 - 使用 Google Gemini (与老项目相同的逻辑)"""
import google.generativeai as genai
from app.config import get_settings
from PIL import Image

settings = get_settings()


class GeminiService:
    """Google Gemini LLM服务 - 参考老项目的 GeminiHandler"""

    def __init__(self):
        """初始化 Gemini,使用 GOOGLE_API_KEY"""
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY 未配置,请在 .env 文件中设置")

        # 配置 Gemini API (与老项目逻辑相同)
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel(settings.google_model)
        print(f"✅ Gemini 已初始化: {settings.google_model}")

    async def generate_text(
        self,
        prompt: str,
        system_message: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """
        使用 Gemini 生成文本 (与老项目 analyze_image 逻辑相同,但用于文本)

        Args:
            prompt: 用户提示词
            system_message: 系统消息(将合并到提示词中)
            temperature: 温度参数
            max_tokens: 最大输出 token 数

        Returns:
            生成的文本
        """
        # Gemini 不支持单独的 system message,合并到 prompt (与老项目相同)
        full_prompt = prompt
        if system_message:
            full_prompt = f"{system_message}\n\n{prompt}"

        # 配置生成参数
        generation_config = genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )

        # 配置安全设置 - 放宽限制以避免学术内容被误判
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]

        # 生成响应 (与老项目相同的调用方式)
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config,
                safety_settings=safety_settings,
            )

            # 检查响应并强制提取内容（忽略安全过滤）
            if not response.candidates:
                print(f"⚠️ Gemini: 没有返回任何候选响应")
                print(f"⚠️ Prompt feedback: {response.prompt_feedback}")
                return "此页面内容无法生成解释(可能包含格式问题)"

            candidate = response.candidates[0]

            # 记录finish_reason但不阻止内容
            if candidate.finish_reason == 2:  # SAFETY
                print(f"⚠️ Gemini SAFETY标记（已忽略）: {candidate.safety_ratings}")
            elif candidate.finish_reason == 3:  # RECITATION
                print(f"⚠️ Gemini RECITATION标记（已忽略）")

            # 强制提取文本内容，无论finish_reason如何
            try:
                # 首先尝试 response.text
                if hasattr(response, 'text') and response.text:
                    return response.text
            except:
                pass

            # 直接从candidate提取内容
            try:
                if candidate.content and candidate.content.parts:
                    parts_text = []
                    for part in candidate.content.parts:
                        if hasattr(part, 'text') and part.text:
                            parts_text.append(part.text)
                    if parts_text:
                        return '\n'.join(parts_text)
            except Exception as e:
                print(f"⚠️ 提取candidate内容失败: {e}")

            return "无法从此页面提取解释内容"

        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ Gemini API 错误: {error_msg}")
            return f"生成解释时出错: {error_msg[:200]}"

    async def analyze_image(
        self,
        image: Image.Image,
        prompt: str,
        system_message: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """
        使用 Gemini Vision 分析图像

        Args:
            image: PIL Image对象
            prompt: 用户提示词
            system_message: 系统消息(将合并到提示词中)
            temperature: 温度参数
            max_tokens: 最大输出 token 数

        Returns:
            生成的文本
        """
        # 合并系统消息和用户提示
        full_prompt = prompt
        if system_message:
            full_prompt = f"{system_message}\n\n{prompt}"

        # 配置生成参数
        generation_config = genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )

        # 配置安全设置 - 放宽限制以避免学术内容被误判
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]

        # 生成响应 (传入图像和文本)
        try:
            response = self.model.generate_content(
                [full_prompt, image],  # 同时传入文本和图像
                generation_config=generation_config,
                safety_settings=safety_settings,
            )

            # 检查响应并强制提取内容（忽略安全过滤）
            if not response.candidates:
                print(f"⚠️ Gemini Vision: 没有返回任何候选响应")
                print(f"⚠️ Prompt feedback: {response.prompt_feedback}")
                return "此页面内容无法生成解释(可能包含格式问题)"

            candidate = response.candidates[0]

            # 记录finish_reason但不阻止内容
            if candidate.finish_reason == 2:  # SAFETY
                print(f"⚠️ Gemini Vision SAFETY标记（已忽略）: {candidate.safety_ratings}")
            elif candidate.finish_reason == 3:  # RECITATION
                print(f"⚠️ Gemini Vision RECITATION标记（已忽略）")

            # 强制提取文本内容，无论finish_reason如何
            try:
                # 首先尝试 response.text
                if hasattr(response, 'text') and response.text:
                    return response.text
            except:
                pass

            # 直接从candidate提取内容
            try:
                if candidate.content and candidate.content.parts:
                    parts_text = []
                    for part in candidate.content.parts:
                        if hasattr(part, 'text') and part.text:
                            parts_text.append(part.text)
                    if parts_text:
                        return '\n'.join(parts_text)
            except Exception as e:
                print(f"⚠️ 提取candidate内容失败: {e}")

            return "无法从此页面提取解释内容"

        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ Gemini Vision API 错误: {error_msg}")
            return f"生成解释时出错: {error_msg[:200]}"

    def get_provider_info(self) -> dict:
        """获取提供商信息"""
        return {
            "provider": "gemini",
            "model": settings.google_model,
            "temperature": settings.temperature,
            "max_tokens": settings.max_tokens,
        }


# 全局单例
llm_service = GeminiService()
