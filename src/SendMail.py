# -*- coding: utf-8 -*-

from Liquirizia.Mailer import SendMail as Base, Error
from Liquirizia.Mailer.Mail import Mail

from boto3 import client
from botocore.exceptions import ClientError

__all__ = (
	'Mailer'
)


class SendMail(Base):
	"""
	SendMail Class for SES
	"""
	
	def __init__(self, token, secret, region):
		self.token = token
		self.secret = secret
		self.region = region
		return
	
	def __call__(self, mail: Mail):
		try:
			connection = client(
				'ses',
				aws_access_key_id=self.token,
				aws_secret_access_key=self.secret,
				region_name=self.region,
			)
			connection.send_raw_email(
				Source=mail.getFromAddress(),
				Destinations=mail.getToAddresses(),
				RawMessage={
					'Data': mail.getMessage().as_string(),
				}
			)
		except ClientError as e:
			raise Error(reason=str(e), error=e)
		except Exception as e:
			raise Error(reason=str(e), error=e)
		return
