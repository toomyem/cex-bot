
import config
import smtplib

def send_mail(msg):
  try:
    m = smtplib.SMTP_SSL(config.mail_srv)
    subject = "[cex.io] Information from cex-bot"
    data = "To: %s\r\nSubject: %s\r\n%s" % (config.mail_to, subject, msg)
    if config.mail_user: m.login(config.mail_user, config.mail_pass)
    m.sendmail("bot@cex.io", config.mail_to, data)
    m.quit()
  except smtplib.SMTPException as ex:
    print ex
    return False

  return True

