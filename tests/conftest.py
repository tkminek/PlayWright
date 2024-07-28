"""
The conftest.py file serves as a means of providing fixtures for an entire directory.
"""

from typing import Generator

import pytest

from helpers.email_manipulation import SeznamEmail


@pytest.fixture(scope="function", autouse=True)
def before_test_case(context) -> Generator[None, None, None]:
    """
    Method called before/after each Test Case. Now its empty

    :param context: variable which could be access in all steps
    :return:
    """
    # print("\nbefore TC")
    yield
    # print("\nafter TC")


@pytest.fixture(scope="module", autouse=True)
def before_module(context) -> Generator[None, None, None]:
    """
    Method called before/after each Test run.
    Now creating instance of SeznamEmail nad provide it into context.

    :param context: variable which could be access in all steps
    :return:
    """
    # print("\nbefore MODULE")
    testing_email = SeznamEmail()
    context["testing_email"] = testing_email
    yield
    # print("\nafter MODULE")
    context["testing_email"].clear()
    context["testing_email"] = None


@pytest.fixture(scope="session")
def context() -> dict:
    """
    Define context variable which could be access in all steps

    :return: dictionary. which can be access in all steps
    """
    return {}

