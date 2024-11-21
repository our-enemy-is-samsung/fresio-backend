import aiosmtplib
from email.mime.text import MIMEText
import random
import string
import asyncio

from app.env_validator import get_settings
from app.logger import use_logger

settings = get_settings()
logger = use_logger("email_service")


class EmailService:
    def __init__(self):
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 587
        self.username = settings.GMAIL_ADDRESS
        self.password = settings.GMAIL_PASSWORD
        self.smtp: aiosmtplib.SMTP | None = None

    async def connect(self) -> None:
        self.smtp = aiosmtplib.SMTP(
            hostname=self.smtp_host, port=self.smtp_port, use_tls=True
        )
        await self.smtp.connect()
        await self.smtp.login(self.username, self.password)

    async def disconnect(self) -> None:
        if self.smtp:
            await self.smtp.quit()
            self.smtp = None

    @staticmethod
    def generate_verification_code(length: int = 6) -> str:
        return "".join(random.choices(string.digits, k=length))

    async def _send_verification_email(self, to_email: str, code: str) -> bool:
        if not self.smtp:
            await self.connect()

        message = MIMEText(
            f"""
        Mixir에 오신 것을 환영합니다!

        귀하의 인증 코드는 다음과 같습니다:

        {code}

        이 인증 코드는 10분간 유효합니다.
        코드를 요청하지 않으셨다면 이 이메일을 무시해주세요.
        """
        )

        message["From"] = self.username
        message["To"] = to_email
        message["Subject"] = "[Mixir] 이메일 인증 코드는 {0}입니다.".format(code)

        try:
            await self.smtp.send_message(message)
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False

    async def send_verify_email(self, to_email: str) -> tuple[bool, str]:
        code = self.generate_verification_code()
        success = await self._send_verification_email(to_email, code)
        return success, code
