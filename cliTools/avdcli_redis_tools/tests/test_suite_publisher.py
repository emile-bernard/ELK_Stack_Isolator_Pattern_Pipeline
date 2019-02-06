import re
import threading
import unittest
from time import sleep

import redis
from avdcli import AVDApp

from avd_redis_tools import Publisher

TEST_SCRIPT = 'publisher'
TEST_LIST_KEYS = ["UL_REPLAY_TEST_1", "UL_REPLAY_TEST_2", "BAD_TEST_KEY"]
TEST_KEY_PATTERN = 'UL_REPLAY_*'
TEST_HOST = 'localhost'
TEST_PORT = 6379
TEST_DB = 0


class PubMethodsTestCase(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        self.redis_conf = None
        self.redis_pub_subs = dict()
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

        # Register subscriber to publisher
        for list_key in TEST_LIST_KEYS:
            if(list_key.startswith('UL_REPLAY_')):
                match = re.search("UL_REPLAY_(.*)", list_key).group(1)
                if match:
                    channel_key = 'UL_REPLAY_' + match + '_CHANNEL'
                    redis_pub_sub = self.redis_conf.pubsub()
                    redis_pub_sub.subscribe(channel_key)
                    messages = []
                    self.redis_pub_subs[list_key] = {
                        'channel_key': channel_key, 'redis_pub_sub': redis_pub_sub, 'messages': messages
                    }

    def tearDown(self):
        for key, value in self.redis_pub_subs.items():
            value['redis_pub_sub'].unsubscribe(value['channel_key'])

        self.redis_pub_subs.clear()

        for list_key in TEST_LIST_KEYS:
            self.redis_conf.delete(list_key)

        self.redis_conf = None

    def listen_to_buffers(self):
        for key, value in self.redis_pub_subs.items():
            message = value['redis_pub_sub'].get_message()
            first_message = True

            while(message):
                if first_message:
                    # Ignore the channel subscription message
                    message = value['redis_pub_sub'].get_message()
                    first_message = False
                    continue
                else:
                    message = value['redis_pub_sub'].get_message()
                    value['messages'].append(message)
                    continue


class PublishAllDocsTestCase(PubMethodsTestCase):
    def runTest(self):
        # Start publisher
        inst, rc = Publisher.run([TEST_SCRIPT, "-H", TEST_HOST, "-P",
                                  TEST_PORT, "-D", TEST_DB, "-N", "1000", "-L", TEST_KEY_PATTERN], exit=False)

        # Iterate message buffer
        self.listen_to_buffers()

        # Assert received message count
        for key, value in self.redis_pub_subs.items():
            received_messages_count = len(value['messages'])
            self.assertEqual(received_messages_count, 1000)


class PublishTenDocsTestCase(PubMethodsTestCase):
    def runTest(self):
        # Start publisher
        inst, rc = Publisher.run([TEST_SCRIPT, "-H", TEST_HOST, "-P",
                                  TEST_PORT, "-D", TEST_DB, "-N", "10", "-L", TEST_KEY_PATTERN], exit=False)

        # Iterate message buffer
        self.listen_to_buffers()

        # Assert received message count
        for key, value in self.redis_pub_subs.items():
            received_messages_count = len(value['messages'])
            self.assertEqual(received_messages_count, 10)


class PublishNegativeTenDocsTestCase(PubMethodsTestCase):
    def runTest(self):
        # Start publisher
        inst, rc = Publisher.run([TEST_SCRIPT, "-H", TEST_HOST, "-P",
                                  TEST_PORT, "-D", TEST_DB, "-N", "-10", "-L", TEST_KEY_PATTERN], exit=False)

        # Iterate message buffer
        self.listen_to_buffers()

        # Assert received message count
        for key, value in self.redis_pub_subs.items():
            received_messages_count = len(value['messages'])
            self.assertEqual(received_messages_count, 10)


class PublishZeroDocsTestCase(PubMethodsTestCase):
    def runTest(self):
        # Start publisher
        inst, rc = Publisher.run([TEST_SCRIPT, "-H", TEST_HOST, "-P",
                                  TEST_PORT, "-D", TEST_DB, "-N", "0", "-L", TEST_KEY_PATTERN], exit=False)

        # Iterate message buffer
        self.listen_to_buffers()

        # Assert received message count
        for key, value in self.redis_pub_subs.items():
            received_messages_count = len(value['messages'])
            self.assertEqual(received_messages_count, 0)


if __name__ == '__main__':
    unittest.main()
