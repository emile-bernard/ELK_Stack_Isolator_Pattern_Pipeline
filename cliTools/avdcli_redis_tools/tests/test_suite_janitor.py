import unittest

import redis
from avdcli import AVDApp

from avd_redis_tools import Janitor

TEST_SCRIPT = 'janitor'
TEST_LIST_KEYS = ["UL_REPLAY_TEST_1", "UL_REPLAY_TEST_2", "BAD_TEST_KEY"]
TEST_KEY_PATTERN = 'UL_REPLAY_*'
TEST_HOST = 'localhost'
TEST_PORT = 6379
TEST_DB = 0


class TrimMethodsTestCase(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        self.redis_conf = None
        return super().__init__(methodName=methodName)

    def setUp(self):
         # Redis configs
        config = {
            'host': TEST_HOST,
            'port': TEST_PORT,
            'db': TEST_DB
        }
        self.redis_conf = redis.StrictRedis(**config)

        # Load test documents in redis
        for list_key in TEST_LIST_KEYS:
            if(list_key.startswith('UL_REPLAY_')):
                for i in range(0, 1000):
                    self.redis_conf.lpush(
                        list_key, 'testDocument{}'.format(str(i)))

    def tearDown(self):
        for list_key in TEST_LIST_KEYS:
            self.redis_conf.delete(list_key)

        self.redis_conf = None


class KeepAllDocsTestCase(TrimMethodsTestCase):
    def runTest(self):
        inst, rc = Janitor.run([TEST_SCRIPT, "-H", TEST_HOST, "-P",
                                TEST_PORT, "-D", TEST_DB, "-N", "1000", "-K", TEST_KEY_PATTERN], exit=False)

        for list_key in TEST_LIST_KEYS:
            if(list_key.startswith('UL_REPLAY_')):
                self.assertEqual(self.redis_conf.llen(list_key), 1000)


class KeepTenDocsTestCase(TrimMethodsTestCase):
    def runTest(self):
        inst, rc = Janitor.run([TEST_SCRIPT, "-H", TEST_HOST, "-P",
                                TEST_PORT, "-D", TEST_DB, "-N", "10", "-K", TEST_KEY_PATTERN], exit=False)

        for list_key in TEST_LIST_KEYS:
            if(list_key.startswith('UL_REPLAY_')):
                self.assertEqual(self.redis_conf.llen(list_key), 10)


class KeepNegativeTenDocsTestCase(TrimMethodsTestCase):
    def runTest(self):
        inst, rc = Janitor.run([TEST_SCRIPT, "-H", TEST_HOST, "-P",
                                TEST_PORT, "-D", TEST_DB, "-N", "-10", "-K", TEST_KEY_PATTERN], exit=False)

        for list_key in TEST_LIST_KEYS:
            if(list_key.startswith('UL_REPLAY_')):
                self.assertEqual(self.redis_conf.llen(list_key), 10)


class KeepZeroDocsTestCase(TrimMethodsTestCase):
    def runTest(self):
        inst, rc = Janitor.run([TEST_SCRIPT, "-H", TEST_HOST, "-P",
                                TEST_PORT, "-D", TEST_DB, "-N", "0", "-K", TEST_KEY_PATTERN], exit=False)

        for list_key in TEST_LIST_KEYS:
            if(list_key.startswith('UL_REPLAY_')):
                self.assertFalse(self.redis_conf.exists(list_key))


if __name__ == '__main__':
    unittest.main()
