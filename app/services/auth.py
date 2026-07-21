import os
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, ExpiredSignatureError, jwt


class AuthService:

    def __init__(self):
        self.admin_email = os.getenv("ADMIN_EMAIL")
        self.admin_password_hash = os.getenv("ADMIN_PASSWORD_HASH")

        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
        )

    def login(self, email: str, password: str) -> str | None:

        email = email.strip().lower()

        if email != self.admin_email.lower():
            return None

        if not self.verify_password(password):
            return None

        return self.create_access_token()

    def verify_password(self, password: str) -> bool:

        return bcrypt.checkpw(
            password.encode("utf-8"),
            self.admin_password_hash.encode("utf-8"),
        )

    def create_access_token(self) -> str:

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.access_token_expire_minutes
        )

        payload = {
            "sub": self.admin_email,
            "iat": datetime.now(timezone.utc),
            "exp": expire,
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    def verify_token(self, token: str) -> dict | None:

        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )

            return payload

        except ExpiredSignatureError:
            return None

        except JWTError:
            return None