"""
Representing steps, which can be used for testing seznam email
corresponding feature file : email_test_1.feature
"""
from pytest_bdd import scenarios, given, when, then, parsers

from helpers.email_manipulation import EmailInputs

# Load all scenarios from the feature file
scenarios("../features/email_test_1.feature")


@given(parsers.parse("load email login credentials from {testing_email}"))
def get_email_credentials(context, testing_email):
    """
    Step used for getting access credentials for email and store them into context variable

    :param context: variable which could be access in all steps
    :param testing_email: email used for testing
    :return:
    """
    result = EmailInputs.get_email_login(testing_email)
    if result is not None:
        email, password = result
        context["email"] = email
        context["password"] = password
        assert True, f"Valid credential used: {testing_email}"
    else:
        assert False, f"Invalid credential used: {testing_email}"


@when("log into email")
def log_in_to_email(context):
    """
    Step used for sign up into email

    :param context: variable which could be access in all steps
    :return:
    """
    result, message = context["testing_email"].login(
        context["email"], context["password"]
    )
    if not result:
        assert False, message
    else:
        assert True, message


@then("check if logg in was successfully proceeded")
def login_validation(context):
    """
    Step used for sign up validation

    :param context: variable which could be access in all steps
    :return:
    """
    result, message = context["testing_email"].check_successful_login()
    if not result:
        assert False, message
    else:
        assert True, message


@given(parsers.parse("load email context from {email_context_path}"))
def load_email_context(context, email_context_path):
    """
    Step used to load up context of email from .json file and store it into context variable

    :param context: variable which could be access in all steps
    :param email_context_path: define path to file which should be attached to the email
    :return:
    """
    result = EmailInputs.load_email_context(email_context_path)
    if result is not None:
        context["email_context"] = {
            "subject": result[0],
            "message": result[1],
            "attachment": result[2],
            "receiver_email": result[3],
        }
        assert True, f"Valid email context path used: {email_context_path}"
    else:
        assert False, f"Invalid email context path used: {email_context_path}"


@when("send email")
def send_email(context):
    """
    Step used to send email

    :param context: variable which could be access in all steps
    :return:
    """
    result, message = context["testing_email"].send_email(
        context["email_context"]["receiver_email"],
        context["email_context"]["subject"],
        context["email_context"]["message"],
        context["email_context"]["attachment"],
    )
    if not result:
        assert False, message
    else:
        assert True, message


@then("check if email was received")
def check_received_email(context):
    """
    Step used check if email was correctly send

    :param context: variable which could be access in all steps
    :return:
    """
    result, message = context["testing_email"].check_last_received_email(
        context["email_context"]["receiver_email"],
        context["email_context"]["subject"],
        context["email_context"]["message"],
        context["email_context"]["attachment"],
    )
    if not result:
        assert False, message
    else:
        assert True, message


@when("log out from email")
def log_out(context):
    """
    Step used to sign out from email

    :param context: variable which could be access in all steps
    :return:
    """
    result, message = context["testing_email"].logout()
    if not result:
        assert False, message
    else:
        assert True, message


@then("check if logg out was successfully proceeded")
def check_successful_logout(context):
    """
    Step used to check if sign up was successfully done

    :param context: variable which could be access in all steps
    :return:
    """
    result, message = context["testing_email"].check_successful_logout()
    if not result:
        assert False, message
    else:
        assert True, message
