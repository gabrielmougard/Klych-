
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib
import os


class Mailing:

  def __init__(self,isepNumber):
    self.isepNumber = isepNumber # pass in the constructor the value read by the 4x4 keyboard

  def recherche(self):
	  #return email address for the associated tuple (nom,prenom)

	  with open("/database/database2.csv") as myFile:


		  for line in myFile.readlines():
			  data = line.split("\t")
			  if (data[2].lower() == nom.lower() and data[3].lower() == prenom.lower()):
				  return data[4]

	  myFile.close()



  def send_mail(self,mail_to,photo):



    email_content = """<html>
      <head>

        <title>Tutsplus Email Newsletter</title>
        <style type="text/css">
          a {color: #d80a3e;}
          body, #header h1, #header h2, p {margin: 0; padding: 0;}
          #main {border: 1px solid #cfcece;}
          img {display: block;}
          #top-message p, #bottom p {color: #3f4042; font-size: 12px; font-family: Arial, Helvetica, sans-serif; }
          #header h1 {color: #ffffff !important; font-family: "Lucida Grande", sans-serif; font-size: 24px; margin-bottom: 0!important; padding-bottom: 0; }
          #header p {color: #ffffff !important; font-family: "Lucida Grande", "Lucida Sans", "Lucida Sans Unicode", sans-serif; font-size: 12px;  }
          h5 {margin: 0 0 0.8em 0;}
          h5 {font-size: 18px; color: #444444 !important; font-family: Arial, Helvetica, sans-serif; }
          p {font-size: 12px; color: #444444 !important; font-family: "Lucida Grande", "Lucida Sans", "Lucida Sans Unicode", sans-serif; line-height: 1.5;}
        </style>
      </head>

      <body>
        <table width="100%" cellpadding="0" cellspacing="0" bgcolor="e4e4e4"><tr><td>
        <table id="top-message" cellpadding="20" cellspacing="0" width="600" align="center">
          <tr>
            <td align="center">
              <p><a href="#">Made with love by GarageISEP</a></p>
            </td>
          </tr>
        </table>

        <table id="main" width="600" align="center" cellpadding="0" cellspacing="15" bgcolor="ffffff">
          <tr>
            <td>
              <table id="header" cellpadding="10" cellspacing="0" align="center" bgcolor="8fb3e9">
                <tr>
                  <td width="570" align="center"  bgcolor="#d80a3e"><h1>Ta Photo !</h1></td>
                </tr>
                <tr>
                  <td width="570" align="right" bgcolor="#d80a3e"><p>5 Octobre 2018</p></td>
                </tr>
              </table>
            </td>
          </tr>

        <tr>
          <td>
            <table id="content-3" cellpadding="0" cellspacing="0" align="center">
              <tr>
                <td width="250" valign="top" bgcolor="d0d0d0" style="padding:5px;">
                  <img src=https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-9/24775259_382470715524483_5601397863366452275_n.png?_nc_cat=103&oh=064fcb028210d0ba8493ac3eed4afb58&oe=5C601109 width="250" height="150"  />
                </td>
                <td width="15"></td>
                <td width="250" valign="top" bgcolor="d0d0d0" style="padding:5px;">
                  <img src=""" +photo+ """  width="250" height="150" />
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td>
            <table id="content-4" cellpadding="0" cellspacing="0" align="center">
              <tr>
                <td width="200" valign="top">
                  <h5>Le Garage... c'est cool.</h5>
                  <p>///presentation cool</p>
                </td>
                <td width="15"></td>
                <td width="200" valign="top">
                  <h5>Tu est magnifique !</h5>
                  <p>///petit mot sympa</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    <table id="bottom" cellpadding="20" cellspacing="0" width="600" align="center">
      <tr>
        <td align="center">
          <p><a href="http://www.gaaab.work">Design</a> by some GarageISEP dudes...</p>
          <p><a href="https://www.facebook.com/garageisep/">Nous suivre !</a></p>
        </td>
      </tr>
    </table><!-- top message -->
    </td></tr></table><!-- wrapper -->

    </body>
    </html>"""

	  msg = MIMEMultipart('alternative')

	  #parameters of message
	  password = "" #put the associated password !
	  msg['From'] = "" #put the email address of the mailing server... the one of Garage ISEP.
	  msg['To'] = mail_to
	  msg['Subject'] = "Photo GarageISEP"

	  #msg.add_header('Content-type','text/html')
	  #msg.set_payload(email_content)

	  #attach HTML
	  html = MIMEText(email_content,'html')
	  msg.attach(html)

	  #attach image

	  image = MIMEImage(file(photo).read())
	  msg.attach(image)
	  #######################

	  #create server
	  server = smtplib.SMTP('smtp.gmail.com: 587')
	  server.starttls()

	  #Login cred for sending mail
	  server.login(msg['From'],password)

	  #send the messagevia the server
	  server.sendmail(msg['From'],msg['To'],msg.as_string())
	  server.quit()
	  print "mail has been successfully sent to %s " % (msg['To'])

#########################	main	#######################"

while(True):
	nom = raw_input('Entre le nom : ')
	prenom = raw_input('Entre le prenom : ')

	mail = recherche(nom,prenom)

	print(mail)
	print('\n')
	imageName = raw_input('Entre le nom de la photo : ') #should be in the same directory
	send_mail(mail,imageName)

	print('\n')
