from openai import OpenAI
import os
from dotenv import load_dotenv
import random

load_dotenv()

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Mock 모드 활성화 (API 크레딧이 없을 때)
        self.use_mock = True
    
    async def chat_with_gpt(
        self,
        user_message: str,
        target_language: str = "영어",
        user_level: str = "A1"
    ) -> dict:
        """
        GPT-3.5와 대화하고 언어 학습 도움 받기
        """
        
        # Mock 모드 (테스트용)
        if self.use_mock:
            return self._get_mock_response(user_message, target_language)
        
        # 실제 GPT API 호출
        try:
            system_prompt = f"""
당신은 {target_language} 학습을 돕는 친절한 AI 튜터입니다.
학생의 레벨: {user_level}
역할:
1. 학생의 질문에 친절하고 자세하게 답변
2. 문법 오류가 있으면 교정해주기
3. 더 나은 표현 제안
4. 학습 팁 제공
5. 격려와 동기부여

답변은 명확하고 이해하기 쉽게 해주세요.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            ai_response = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            grammar_correction = "문법이 완벽합니다! 👍"
            
            return {
                "success": True,
                "ai_response": ai_response,
                "grammar_correction": grammar_correction,
                "tokens_used": tokens_used
            }
            
        except Exception as e:
            print(f"OpenAI API 오류: {str(e)}")
            return {
                "success": False,
                "error": f"GPT-3.5 오류: {str(e)}"
            }
    
    def _get_mock_response(self, user_message: str, target_language: str) -> dict:
        """Mock 응답 생성 (테스트용)"""
        
        # 다양한 Mock 응답
        responses = [
            f"안녕하세요! {target_language} 학습을 도와드리겠습니다! 😊\n\n"
            f"'{user_message}' 에 대해 설명드리자면:\n\n"
            f"1. 기본적인 인사는 'Hello'나 'Hi'를 사용합니다.\n"
            f"2. 격식을 차린 인사는 'Good morning/afternoon/evening'을 사용해요.\n"
            f"3. 친구들에게는 'Hey'나 'What's up?'도 자주 사용합니다!\n\n"
            f"더 궁금한 점이 있으시면 언제든 물어보세요! 💪",
            
            f"좋은 질문이에요! {target_language} 학습에서 이 부분은 매우 중요합니다.\n\n"
            f"제 답변:\n"
            f"• 자주 연습하는 것이 가장 중요해요\n"
            f"• 원어민의 발음을 많이 듣고 따라하세요\n"
            f"• 실수를 두려워하지 마세요! 실수는 배움의 과정입니다.\n\n"
            f"계속 노력하시면 분명히 실력이 향상될 거예요! 🌟",
            
            f"훌륭한 질문입니다! 💡\n\n"
            f"이 문법은 다음과 같이 사용해요:\n"
            f"1. 주어 + 동사 + 목적어 순서\n"
            f"2. 시제에 주의하세요\n"
            f"3. 예문: 'I am learning English.'\n\n"
            f"더 많은 예문이 필요하시면 말씀해주세요! 📚",
        ]
        
        # 랜덤 응답 선택
        ai_response = random.choice(responses)
        
        # 문법 교정 (랜덤)
        grammar_corrections = [
            "문법이 완벽합니다! 👍",
            "Good job! 문장 구조가 정확해요! ✨",
            "훌륭해요! 자연스러운 표현이에요! 🎉",
        ]
        
        return {
            "success": True,
            "ai_response": ai_response,
            "grammar_correction": random.choice(grammar_corrections),
            "tokens_used": 100
        }