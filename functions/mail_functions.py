import smtplib

my_email = "portfoliodb.info@gmail.com"
email_password = "khoe xkyh irky xsqc"
# connection = smtplib.SMTP("smtp.gmail.com")
# connection.starttls
# connection.login(user=my_email,password=email_password)
# connection.sendmail(from_addr=my_email,to_addrs="alwglass@gmail.com",msg="hello")

def smtp_sendmail(email,message):
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
            connection.login(user = my_email, password = email_password)
            connection.sendmail(from_addr=my_email,
                                    to_addrs=email, 
                                    msg = message
                                     )
    except:
        print("connection error.")
    else:
        print("E-Mail sent successfully.")

# connection.close

# smtp_sendmail(email = "alwglass@gmail.com" , message = "Subject:Sign Up Success\n\nCongratulations on starting your portfolio!!") 