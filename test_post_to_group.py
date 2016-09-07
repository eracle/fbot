import unittest
from fbconnection import FbConnection

from test_conf import *

sut = FbConnection(email, password)


class test_post_to_group(unittest.TestCase):

    def test_delete_first_post_in_group(self):
        sut.post_to_group(post_msg=delete_post_msg, group_id=group_id)
        sut.delete_first_post_in_group(group_id=group_id)

    def test_post_to_group_then_jump(self):
        sut.post_to_group(post_msg=delete_post_msg, group_id=group_id)
        sut.delete_first_post_in_group(group_id=group_id)
        sut.driver.get('https://www.facebook.com/')

if __name__ == "__main__":
    unittest.main()
