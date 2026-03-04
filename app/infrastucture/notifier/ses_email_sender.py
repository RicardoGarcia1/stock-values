from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
import locale
from typing import List
from app.domain.models.user_data import History, User
from app.domain.ports.email_sender_port import EmailSenderPort
from app.infrastucture.client.ses_client import BODY_HTML, BODY_TEXT, RECIPIENT, SENDER, SUBJECT, get_ses_client
from botocore.exceptions import ClientError


class SesEmailSender(EmailSenderPort):
    def send_email(self, total: str, name:str, email: str, user_history: List[History]):
        try:
            BODY_HTML_TEMPLATE = """<html>
            <head></head>
            <body>
            <h1>¡Hola {name}!</h1>
            <p>¡Aquí van los updates que tanto esperas recibir!</p>
            <p>¡El equipo te desea que hayas tenido una buena semana de inversiones y negocios!</p>
            <p>Si ha sido así nos alegramos y si no ha sido así recuerda: "Invertir no se trata de evitar riesgos, sino de tomar decisiones inteligentes hoy para cosechar oportunidades mañana."</p>
            <p> A dia de hoy ({today}), tienes una cartera valorada en:</p>
            <div style="text-align: center;">
                <b style="font-size: 32px;"> {total} euros</b>
            </div>
             <div>

            Esto quiere decir que su cartera se ha visto {signed} en la ultima semana en: <b style="font-size: 15px;">{amount} euros</b> o un <b style="font-size: 15px;"> {percent}%</b>. 

             </div>

            <p> El equipo de <b style="font-size: 15px;">RGP Investments</b> te desea una buena semana</p>
            </body>
            </html>
            """
            print(user_history)
            locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
            date = datetime.now()
            current_value = Decimal(total)
            last_week_value=Decimal("0")
            for history_value in user_history:
                history_date = datetime.strptime(history_value.day, "%Y-%m-%d")
                if history_date.day == (date.day - 7):
                    last_week_value = history_value.totalValue
            

            signed = "incrementado" if current_value - last_week_value > 0 else "disminuido"
            amount_updated = current_value - last_week_value
            percent = ((current_value - last_week_value) / last_week_value) *100

            BODY_HTML = BODY_HTML_TEMPLATE.format(
                name=name,
                today=date.strftime("%d de %B de %Y"),
                total=total, 
                signed = signed, 
                amount=abs(amount_updated), 
                percent = percent.quantize(Decimal("0.01"), 
                                            rounding=ROUND_HALF_UP
                                            )
            )

            response = get_ses_client().send_email(
                Source=SENDER,
                Destination={"ToAddresses": [email]},
                Message={
                    "Subject": {"Data": SUBJECT},
                    "Body": {
                        "Html": {"Data": f"{BODY_HTML}"},
                    }
                }
            )
            print("Correo enviado! Messageuser_identifier:", response['MessageId'])
        except ClientError as e:
            print("Error al enviar correo:", e.response['Error']['Message'])