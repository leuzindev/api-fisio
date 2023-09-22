import os
import requests
import logging
from datetime import datetime, timezone, timedelta
from admin_honeypot.signals import honeypot
from django.dispatch import receiver

logger = logging.getLogger(__name__)


def convert_iso_to_br_with_timezone(iso_date_with_timezone):
    date = datetime.fromisoformat(iso_date_with_timezone)
    date_brazil = date + timedelta(hours=-3)
    formatted_date = date_brazil.strftime('%d/%m/%Y %H:%M:%S')

    return formatted_date


@receiver(honeypot)
def send_admin_attempt_alert(sender, **kwargs):
    logger.warning('Attempting to login in FAKE admin')

    username = kwargs['instance'].username
    ip = kwargs['instance'].ip_address
    time = convert_iso_to_br_with_timezone(str(kwargs['instance'].timestamp))

    token = os.getenv('TELEGRAM_BOT_API_KEY')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    url = f'https://api.telegram.org/bot{token}/sendMessage'

    message = (
        f'🔴 Alerta 🔴\nAlguém tentou fazer login no admin\n\n'
        f'Nome: {username}\n'
        f'ip: {ip}\n'
        f'às {time}\n'
    )

    params = {
        'chat_id': chat_id,
        'text': message
    }

    requests.post(url, json=params)

