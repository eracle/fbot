import unittest
from fbconnection import FbConnection
from test_conf import *


class TestFbConnection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sut = FbConnection(email, password)
        assert cls.sut.user_name == account_user_name

    @classmethod
    def tearDownClass(cls):
        cls.sut.driver.close()

#    def test_post_to_sale_group(self):
#        self.sut.post_to_sale_group(sell_msg=sell_msg, group_id=sale_g_id, item_description=delete_post_msg, location=sell_location)

    def test_post_to_sale_group_then_jump(self):
        self.sut.post_to_sale_group(sell_msg=sell_msg, group_id=sale_g_id, item_description=sell_msg, location=sell_location)
        self.sut.driver.get('https://www.facebook.com/')

    def test_post_to_group_and_delete_many_posts(self):

        for post in seq_post_msgs:
            self.sut.post_to_group(post_msg=post, group_id=group_id)

        posts_posted = self.sut.iterate_group_posts(group_id=group_id)

        for post_example in seq_post_msgs[::-1]:
            real_post = next(posts_posted)
            assert real_post["name"] == self.sut.user_name
            assert real_post["text"] == post_example

        for post_example in seq_post_msgs:
            self.sut.delete_first_post_in_group(group_id=group_id, msg_to_remove=post_example)




if __name__ == "__main__":
    unittest.main()