"""
This module serves for running pytest
"""
import os

import pytest

BASEDIR = "D:/PYTHON/PROJECTS/PlayWright"


def main() -> None:
    """
    Function to run pytest-BDD

    :return:
    """
    ret_code = pytest.main(
        [
            os.path.join(BASEDIR, "tests/step_definitions/test_email.py"),
            "--verbose",
            "--html=" + os.path.join(BASEDIR, "reports/report_v1.html"),
            "--html-report=" + os.path.join(BASEDIR, "reports/report_v2.html"),
            "--self-contained-html",
            "-s",
        ]
    )
    print(ret_code)


if __name__ == "__main__":
    main()
