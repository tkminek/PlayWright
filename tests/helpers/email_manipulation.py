"""
Python module for manipulation with seznam email.
"""

import os
import json
import time
from typing import Tuple, Optional
import keyring

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
    Error,
    Page,
    Playwright,
    Browser,
)


class SeznamEmail:
    """
    Class containing all methods which can be used for manipulation with email,
    like :   login
            check_successful_login
            logout
            check_successful_logout
            send_email
            check_last_received_email
            clear
    """

    def __init__(self):
        self._playwright: Playwright = sync_playwright().start()
        self._browser: Browser = self._playwright.firefox.launch(
            headless=False, slow_mo=1
        )
        self._page: Page = self._browser.new_page()

    def _fill_user_name(self, email: str) -> bool:
        try:
            self._page.wait_for_selector(
                "#login-username", state="visible", timeout=5000
            )
            user_name_field = self._page.locator("#login-username")
            user_name_field.fill(email)

            login_button = self._page.get_by_role("button", name="Continue")
            self._page.wait_for_selector(
                'button:has-text("Continue")', state="visible", timeout=5000
            )
            login_button.click()
            return True
        except PlaywrightTimeoutError:
            return False

    def _go_to_login(self) -> bool:
        try:
            self._page.wait_for_selector(
                'div.gadget__content >> role=link[name="Přihlásit"]', state="visible"
            )
            login_button = self._page.locator("div.gadget__content").get_by_role(
                "link", name="Přihlásit"
            )
            login_page_href = login_button.get_attribute("href")
            if login_page_href:
                self._page.goto(login_page_href, wait_until="load")
                return True
            return False
        except PlaywrightTimeoutError:
            return False

    def _fill_password(self, password: str) -> bool:
        try:
            self._page.wait_for_selector(
                "#login-password", state="visible", timeout=5000
            )
            password_name_field = self._page.locator("#login-password")
            password_name_field.fill(password)
            return True
        except PlaywrightTimeoutError:
            return False

    def _go_to_seznam_page(self) -> bool:
        try:
            self._page.goto("https://www.seznam.cz/", wait_until="load")
            return True
        except Error:
            return False

    def _click_login_button(self) -> bool:
        try:
            self._page.wait_for_selector(
                'button:has-text("Sign in")', state="visible", timeout=5000
            )
            login_button = self._page.get_by_role("button", name="Sign in")
            login_button.click()
            return True
        except PlaywrightTimeoutError:
            return False

    def _click_to_send_email(self):
        try:
            self._page.wait_for_selector(
                'role=button[name="Odeslat e-mail"]', state="visible", timeout=5000
            )
            send_email_button = self._page.get_by_role("button", name="Odeslat e-mail")
            send_email_button.click()
            return True
        except PlaywrightTimeoutError:
            return False

    def _open_new_email(self):
        try:
            self._page.wait_for_selector(
                'role=link[name="Napsat e-mail"]', state="visible", timeout=5000
            )
            wrote_email_button = self._page.get_by_role("link", name="Napsat e-mail")
            wrote_email_button.click()
            return True
        except PlaywrightTimeoutError:
            return False

    def _add_message(self, message: str) -> bool:
        try:
            self._page.wait_for_selector(
                'div.area.apply-styles[contenteditable="true"][placeholder="Text e-mailu…"]',
                state="visible",
            )
            email_text = self._page.locator(
                'div.area.apply-styles[contenteditable="true"][placeholder="Text e-mailu…"]'
            )
            email_text.fill(message)
            return True
        except PlaywrightTimeoutError:
            return False

    def _add_subject(self, subject: str) -> bool:
        try:
            self._page.wait_for_selector(
                '[placeholder="Předmět…"]', state="visible", timeout=5000
            )
            email_subject = self._page.get_by_placeholder("Předmět…")
            email_subject.fill(subject)
            return True
        except PlaywrightTimeoutError:
            return False

    def _add_attachment(self, path) -> bool:
        try:
            with self._page.expect_file_chooser() as fc_info:
                self._page.wait_for_selector(
                    '[aria-label="Přidat přílohu"]', state="visible", timeout=5000
                )
                self._page.get_by_label("Přidat přílohu").click()
            file_chooser = fc_info.value
            file_chooser.set_files(path)
            return True
        except PlaywrightTimeoutError:
            return False

    def _add_receiver(self, receiver_email: str) -> bool:
        try:
            self._page.wait_for_selector(
                'role=button[name="Komu"]', state="visible", timeout=5000
            )
            user_button = self._page.get_by_role("button", name="Komu")
            user_button.click()

            self._page.wait_for_selector(
                f'div[data-email="{receiver_email}"]', state="visible", timeout=5000
            )
            receiver_element = self._page.locator(f'div[data-email="{receiver_email}"]')
            receiver_element.click()
            user_button.click()
            return True
        except PlaywrightTimeoutError:
            return False

    def _wait_until_received_email(self) -> bool:
        try:
            # self._page.wait_for_selector('[data-dot="item-general.email.notification"]',
            #                              state='visible')
            initial_count = (
                self._page.locator(".message-list").get_by_role("listitem").count()
            )
            time_limit = 120
            time_start = time.time()
            while abs(time.time() - time_start) <= time_limit:
                self._page.reload()
                end_count = (
                    self._page.locator(".message-list").get_by_role("listitem").count()
                )
                if end_count != initial_count:
                    return True
                time.sleep(2)
            return False
        except PlaywrightTimeoutError:
            return False

    def _load_last_received_email(self) -> bool:
        try:
            self._page.get_by_role("link", name="Doručené").click()
            self._page.wait_for_selector(".message-list", state="visible", timeout=5000)
            received_emails = self._page.locator(".message-list").get_by_role(
                "listitem"
            )
            last_received_email = received_emails.nth(0)
            last_received_email.highlight()
            last_received_email.click()
            return True
        except PlaywrightTimeoutError:
            return False

    def _check_message(self, message_expected: str) -> bool:
        try:
            self._page.wait_for_selector(
                "div.body.apply-styles", state="visible", timeout=5000
            )
            message = self._page.locator("div.body.apply-styles").text_content()
            if message == message_expected:
                return True
            return False
        except PlaywrightTimeoutError:
            return False

    def _check_attachment(self, attachment_expected: str) -> bool:
        try:
            self._page.wait_for_selector("li.attachment", state="visible", timeout=5000)
            attachment = (
                self._page.locator("li.attachment").locator("strong").text_content()
            )
            path = os.path.basename(attachment_expected)
            file_name = os.path.basename(path)
            if attachment == file_name:
                return True
            return False
        except PlaywrightTimeoutError:
            return False

    def _check_subject(self, subject_expected: str) -> bool:
        try:
            self._page.wait_for_selector(".subject h2", state="visible", timeout=5000)
            subject = self._page.locator(".subject h2").text_content()
            if subject == subject_expected:
                return True
            return False
        except PlaywrightTimeoutError:
            return False

    def _check_sender_email(self, receiver_email: str) -> bool:
        try:
            self._page.wait_for_selector(".from strong", state="visible", timeout=5000)
            sender_email = self._page.locator(".from strong").text_content()
            if sender_email == receiver_email:
                return True
            return False
        except PlaywrightTimeoutError:
            return False

    def login(self, email: str, password: str) -> Tuple[bool, str]:
        """
        Method used for sign up to seznam email

        :param email: user email, which should be used for sign up
        :param password: user password, which should be used for sign up
        :return: True - if sign up was successfully done
                 False - if sign up was not successfully done
                 message - provide more information, like reason of fail, etc.
        """
        if not self._go_to_seznam_page():
            return False, "Not able to load seznam page"
        if not self._go_to_login():
            return False, "Not able to load up login page"
        if not self._fill_user_name(email):
            return False, "Not possible to fill in user"
        if not self._fill_password(password):
            return False, "Not able to fill in password"
        if not self._click_login_button():
            return False, "Not able to click on login button"
        return True, "Login successfully done"

    def check_successful_login(self) -> Tuple[bool, str]:
        """
        Method used for checking if sign up was succesfully done

        :return: True - if sign up was successfully done (additional check)
                 False - if sign up was not successfully done (additional check)
                 message - provide more information, like reason of fail, etc.
        """
        try:
            self._page.wait_for_load_state("networkidle")
            error_locator = self._page.locator(
                'div.error:text("Password or username is incorrect")'
            )
            if not error_locator.is_visible(timeout=2000):
                return True, "Login successful"
            return False, "Login not successful"
        except PlaywrightTimeoutError:
            return False, "Not able to do login check"

    def check_successful_logout(self) -> Tuple[bool, str]:
        """
        Method used for checking if sign out was succesfully done

        :return: True - if sign out was successfully done (additional check)
                 False - if sign out was not successfully done (additional check)
                 message - provide more information, like reason of fail, etc.
        """
        try:
            self._page.wait_for_load_state("networkidle")
            login_locator = self._page.locator('// *[ @ id = "login"]')
            if login_locator.is_visible(timeout=2000):
                return True, "Logout successful"
            return False, "Logout not successful"
        except PlaywrightTimeoutError:
            return False, "Not able to detect logout state"

    def logout(self) -> Tuple[bool, str]:
        """
        Method used for sign out to seznam email

        :return: True - if sign out was successfully done
                 False - if sign out was not successfully done
                 message - provide more information, like reason of fail, etc.
        """
        try:
            self._page.wait_for_selector(
                'role=button[name="Uživatel – osobní menu"]',
                state="visible",
                timeout=5000,
            )
            user_button = self._page.get_by_role(
                "button", name="Uživatel – osobní menu"
            )
            user_button.click()
            self._page.wait_for_selector(
                'role=link[name="Odhlásit se"]', state="visible", timeout=5000
            )
            logout_button = self._page.get_by_role("link", name="Odhlásit se")
            logout_button.click()
            return True, "Successfully logout"
        except PlaywrightTimeoutError:
            return False, "Unsuccessfully logout"

    def clear(self) -> None:
        """
        Method used to close the browser and stop sync_playwright()
        """
        self._browser.close()
        self._playwright.stop()

    def send_email(
        self, receiver_email: str, subject: str, message: str, path: str
    ) -> Tuple[bool, str]:
        """
        Method used for sending email

        :param receiver_email: email address where email should be sent
        :param subject: define subject of email
        :param message: define message of email
        :param path: define path to file which should be attached to the email
        :return: True - if sending of email was successfully done
                 False - if sending of email was not successfully done
                 message - provide more information, like reason of fail, etc.
        """
        if not self._open_new_email():
            return False, "Not able to open new email"
        if not self._add_receiver(receiver_email):
            return False, "Not able to add receiver"
        if not self._add_subject(subject):
            return False, "Not able to add subject"
        if not self._add_attachment(path):
            return False, "Not able to add attachment"
        if not self._add_message(message):
            return False, "Not able to add message"
        if not self._click_to_send_email():
            return False, "Not able to click on send email"
        return True, "Email was sent successfully"

    def check_last_received_email(
        self, receiver_email: str, subject: str, message: str, path: str
    ) -> Tuple[bool, str]:
        """
        Method used for checking if email was correctly received

        :param receiver_email: email address where email should be sent
        :param subject: define subject of email
        :param message: define message of email
        :param path: define path to file which should be attached to the email
        :return: True - if the last received email has correct attributes
                 False - if the last received email has not correct attributes
                 message - provide more information, like reason of fail, etc.
        """
        if not self._wait_until_received_email():
            return False, "Email was not received"
        if not self._load_last_received_email():
            return False, "Not able to load last received email"
        if not self._check_sender_email(receiver_email):
            return False, "Invalid email sender"
        if not self._check_subject(subject):
            return False, "Invalid email subject"
        if not self._check_message(message):
            return False, "Invalid email message context"
        if not self._check_attachment(path):
            return False, "Invalid email attachment file"
        return True, "Received email is valid"


class EmailInputs:
    """
    Class consists of methods which help to get the inputs necessary for email logging/sending
    like :
        load_email_context,
        get_email_login
    """

    @staticmethod
    def load_email_context(
        email_context_path,
    ) -> Optional[Tuple[str, str, str, str]]:
        """
        Method to load up context of email from .json file

        :param email_context_path: path to json file which consists all necessary inputs for email
        :return: subject - define subject of email
                 message - define message of email
                 attachment - define path to file which should be attached to the email
                 receiver_email - email address where email should be sent
                 None - in case of invalid email_context_path
        """
        try:
            with open(email_context_path) as file:
                json_context = json.load(file)
                subject = json_context["subject"]
                message = json_context["message"]
                attachment = json_context["attachment"]
                receiver_email = json_context["receiver_email"]
                return subject, message, attachment, receiver_email
        except AttributeError:
            return None
        except FileNotFoundError:
            return None

    @staticmethod
    def get_email_login(credential_name: str) -> Optional[Tuple[str, str]]:
        """
        Method used for getting access credentials for email

        :param credential_name: name of credentials which are stored in credential manager
        :return: username - email address which is used for logging
                 password - email password which is used for logging
                 None - in case of invalid credential_name
        """
        try:
            credentials = keyring.get_credential(credential_name, None)
            if credentials:
                return credentials.username, credentials.password
            return None
        except AttributeError:
            return None
