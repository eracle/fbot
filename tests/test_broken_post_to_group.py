import pytest

from tests.test_fbot import driver
from tests.conf import *
import fbot


def test_delete_post(driver):
    fbot.post_to_group(driver=driver, group_id=group_id, post_msg=delete_post_msg)
    fbot.delete_first_post_in_group(driver=driver, user_name=account_user_name, group_id=group_id)


def test_post_to_group_and_delete_many_posts(driver):
    for post in seq_post_msgs:
        fbot.post_to_group(driver=driver, post_msg=post, group_id=group_id)

    posts_posted = fbot.iterate_group_posts(driver=driver, group_id=group_id)

    for post_example in seq_post_msgs[::-1]:
        real_post = next(posts_posted)
        assert real_post["name"] == account_user_name
        assert real_post["text"] == post_example

    for post_example in seq_post_msgs:
        fbot.delete_first_post_in_group(driver=driver, group_id=group_id, msg_to_remove=post_example)


def test_iterate_group_posts(driver):
    group_id = "cercocasapisa"

    n_posts = 0
    posts_iterator = fbot.iterate_group_posts(driver=driver, group_id=group_id)
    for post in posts_iterator:
        n_posts += 1
        assert post is not None
        assert post != ''
        assert post.name is not None
        assert post.name != ''
        assert post.date is not None
        assert post.date != ''
        assert post.title is not None
        assert post.title != ''
        assert post.price is not None
        assert post.price != ''
        assert post.location is not None
        assert post.location != ''
        assert post.text is not None
        assert post.text != ''
        assert post.xpath_element is not None
        assert post.xpath_element != ''

    assert n_posts > 1
