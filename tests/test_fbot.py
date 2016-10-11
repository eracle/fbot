import pytest

from tests.conf import *
import fbot


@pytest.fixture(scope="session")
def driver():
    (driver, username) = fbot.login(email, password)
    assert username == account_user_name
    assert 'Facebook' in driver.title
    yield driver
    driver.close()


def test_post_to_group(driver):
    fbot.post_to_group(driver=driver, group_id=group_id, post_msg=delete_post_msg)
    driver.get('https://www.facebook.com/')


def test_post_to_sale_group(driver):
    fbot.post_to_sale_group(driver=driver, sell_msg=sell_msg, group_id=sale_g_id, item_description=sell_msg,
                            location=sell_location)
    driver.get('https://www.facebook.com/')


def test_iterate_group_posts(driver):
    n_posts = 0
    posts_iterator = fbot.iterate_group_posts(driver=driver, group_id=group_id)
    for post in posts_iterator:
        n_posts += 1
        assert post
        assert post.name
        assert post.name != ''
        assert post.date
        assert post.date != ''
        assert post.title
        assert post.price
        assert post.location
        assert post.text
        assert post.text != ''
        assert post.xpath_element

    #assert n_posts > 0


def test_post_to_group_and_delete_many_posts(driver):
    for post in seq_post_msgs:
        fbot.post_to_group(driver=driver, post_msg=post, group_id=group_id)

    posts_posted = fbot.iterate_group_posts(driver=driver, group_id=group_id)

    for post_example in seq_post_msgs[::-1]:
        real_post = next(posts_posted)
        assert real_post.name == account_user_name
        assert real_post.text == post_example

    for post_example in seq_post_msgs:
        fbot.delete_first_post_in_group(driver=driver, user_name=account_user_name, group_id=group_id, msg_to_remove=post_example)


def test_delete_post(driver):
    fbot.delete_first_post_in_group(driver=driver, user_name=account_user_name, group_id=group_id)

