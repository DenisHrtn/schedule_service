from __future__ import annotations
import random
import string
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from rest_framework import status

from users.models.user import User


class EmailService:
    """
    Functionalities for sending email to users
    Some docs:
    1. All methods are used in our APIs
    --------------------------------------------------------------------------------------------------------------------
    2. If you want to send custom mail - use this method: `send_custom_message`, also don’t forget to look at the
    required parameters for this method to eliminate possible errors
    --------------------------------------------------------------------------------------------------------------------
    3. If you want to change len or other params in generate code - change methods: `generate_code`
    """

    def generate_code(self) -> str:
        """
        Generate a random code
        """
        code = random.randint(1000, 9999)
        return str(code)

    def save_code(self, email: str, code: str):
        """
        Save the code in user's fields
        """
        user = User.objects.filter(email=email).first()
        try:
            if not user:
                return None
            else:
                user.code = code
                user.save()
        except Exception as e:
            print(f'Something went wrong {e}')

    def send_code_to_email(self, email: str):
        """
        Send code to user email
        """
        code = self.generate_code()
        self.save_code(email, code)

        subject = 'Your code for confirmation register'
        message = f'Your code for confirmation register: {code}'
        from_email = settings.EMAIL_HOST_USER

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=[email]
            )
        except Exception as e:
            return Response(f'Something went wrong {e}')
        return code