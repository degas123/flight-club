import smtplib

class NotificationManager:
my_email = "jtt666664@gmail.com"
password =${{ secrets.PASSWORD }}
USERS_ENDPOINT= ${{secrets.USERS_ENDPOINT }}

    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(self.my_email,self.password)
            for email in emails:
                connection.sendmail(
                    from_addr=self.my_email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )



