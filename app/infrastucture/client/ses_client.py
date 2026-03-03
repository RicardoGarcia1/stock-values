import os
import boto3
from botocore.exceptions import ClientError

SENDER = "ricardogarciapericuesta@gmail.com"
RECIPIENT = "ricardogarciapericuesta@gmail.com"

SUBJECT = "Actualización de tus inversiones"

BODY_TEXT = "Hola, este es un correo enviado con las actualizaciones de tus inversiones actuales"
BODY_HTML = """<html>
<head></head>
<body>
  <h1>Hola!</h1>
  <p>Aquí van los updates</p>
</body>
</html>
"""

def get_ses_client():
    return boto3.client("ses", region_name="eu-west-2")