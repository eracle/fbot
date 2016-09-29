import pytest

from tests.conf import *
import fbot


@pytest.fixture(scope="session")
def driver():
    (driver, username) = fbot.login(email, password)
    assert username == account_user_name
    assert driver.title == 'Facebook'
    yield driver
    driver.close()


def test_post_to_group(driver):
    fbot.post_to_group(driver=driver, group_id=group_id, post_msg=delete_post_msg)
    driver.get('https://www.facebook.com/')


def test_post_to_sale_group(driver):
    fbot.post_to_sale_group(driver=driver, sell_msg=sell_msg, group_id=sale_g_id, item_description=sell_msg,
                            location=sell_location)
    driver.get('https://www.facebook.com/')
