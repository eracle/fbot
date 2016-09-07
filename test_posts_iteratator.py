import unittest
from fbconnection import FbConnection

from test_conf import *

sut = FbConnection(email, password)

group_id = "cercocasapisa"


class test_iterator(unittest.TestCase):


    def test_iterate_group_posts(self):
        try:
            iterator = sut.iterate_group_posts(group_id=group_id)
            for i in iterator:
                pass
        except Exception:
            print ("exception!")
            #import q
            #q.d()


if __name__ == "__main__":
    unittest.main()