import time

from helpers.email_manipulation import EmailInputs, SeznamEmail


def main():
    credentials = "testing_email"
    email, password = EmailInputs.get_email_login(credentials)
    testing_email = SeznamEmail()
    testing_email.login(email, password)
    login_result = testing_email.check_successful_login()
    email_contex_path = "D:/PYTHON/PROJECTS/PlayWright/input_files/email_context.json"
    subject, message, attachment, receiver_email = EmailInputs.load_email_context(email_contex_path)
    print(login_result)
    testing_email.send_email(receiver_email, subject, message, attachment)
    email_result = testing_email.check_last_received_email(receiver_email, subject, message, attachment)
    print(email_result)
    testing_email.logout()
    logout_result = testing_email.check_successful_logout()
    print(logout_result)
    time.sleep(1)
    testing_email.clear()


if __name__ == "__main__":
    main()
