Feature: Email process
  Test email usage
   Scenario: Sign in email
     Given load email login credentials from testing_email
     When log into email
     Then check if logg in was successfully proceeded

    Scenario: Send email
      Given load email context from D:/PYTHON/PROJECTS/PlayWright/input_files/email_context.json
      When send email
      Then check if email was received

    Scenario: Sign out of email
      When log out from email
      Then check if logg out was successfully proceeded