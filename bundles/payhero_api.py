import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class PayheroService:
    def __init__(self):
        self.api_url = settings.PAYHERO_API_URL
        self.callback_url = settings.PAYHERO_CALLBACK_URL
        self.basic_auth_token = settings.BASIC_AUTH_TOKEN
        self.channel_id = settings.PAYHERO_CHANNEL_ID

    def initiate_stk_push(self, phone_number, amount, reference, description):
        """
        Initiates an STK Push to the user's phone.
        """
        try:
            formatted_phone = self._format_phone_number(phone_number)

            # Ensure amount is an integer if it has no decimal part (MPesa preference)
            final_amount = float(amount)
            if final_amount == int(final_amount):
                final_amount = int(final_amount)

            # channel_id must be an integer for PayHero API
            try:
                channel_id_int = int(self.channel_id)
            except (ValueError, TypeError):
                logger.error(f"Invalid channel_id: {self.channel_id}")
                return {"success": False, "message": "Configuration error: Invalid channel ID"}

            payload = {
                "amount": final_amount,
                "phone_number": formatted_phone,
                "channel_id": channel_id_int,
                "provider": "m-pesa",
                "external_reference": reference,
                "customer_name": description,
                "callback_url": self.callback_url
            }
            
            # Debug logging - remove in production if sensitive
            logger.info(f"PayHero Payload: {payload}")

            # Ensure token has Basic prefix
            token = self.basic_auth_token
            if not token.startswith("Basic "):
                token = f"Basic {token}"

            headers = {
                "Content-Type": "application/json",
                "Authorization": token
            }

            logger.info(f"Initiating STK Push for {formatted_phone}, Amount: {final_amount}")

            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=60
            )

            if response.status_code in [200, 201]:
                return {
                    "success": True,
                    "message": "STK Push sent successfully.",
                    "data": response.json()
                }
            else:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', response.text)
                except:
                    error_msg = response.text
                
                logger.error(f"PayHero API Error: {response.status_code} - {error_msg}")
                return {
                    "success": False,
                    "message": f"API Error: {error_msg}"
                }

        except requests.exceptions.Timeout:
            logger.error("PayHero API Request Timed Out (60s)")
            return {"success": False, "message": "The payment request timed out. Please try again."}
        except Exception as e:
            logger.error(f"STK Push Error: {str(e)}")
            return {"success": False, "message": f"An unexpected error occurred: {str(e)}"}

    def _format_phone_number(self, phone_number):
        """Ensures phone number is in 254 format."""
        phone = phone_number.replace(" ", "").replace("-", "").replace("+", "")
        if phone.startswith("0"):
            return "254" + phone[1:]
        if not phone.startswith("254"):
            return "254" + phone
        return phone
