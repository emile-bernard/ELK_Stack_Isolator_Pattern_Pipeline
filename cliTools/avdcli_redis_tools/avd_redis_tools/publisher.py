import os
import re
import sys
import time

import redis
from avdcli import AVDApp
from avdlogger import lpl
from plumbum import cli, colors

from avd_redis_tools import __version__


class Publisher(AVDApp):

    def __init__(self, *args):
        super().__init__(*args)

    # Script flags
    PROGNAME = colors.bold & colors.yellow2
    VERSION = colors.bold & colors.yellow2 | __version__
    DESCRIPTION = colors.bold & colors.Grey84 | "[FR] L'outil de ligne de commande publisher sert a prendre un certain nombre de documents d'une cle redis (type liste) et a les publiers sur une autre cle redis (type channel)." + \
        '\n' + \
        "[EN] The publisher command line tool is used to get a number a documents from a redis key (list type) and publish them to a redis key (channel type)."
    COLOR_USAGE = colors.bold & colors.LightYellow3
    group = '1 Publisher'
    COLOR_GROUPS = {
        group: colors.bold & colors.LightGoldenrod3,
        "0.0 Lookup file": colors.bold & colors.LightGoldenrod2,
        "0.1 Authenfication": colors.bold & colors.LightGoldenrod2,
        "0.2 Logging": colors.bold & colors.LightGoldenrod2,
        "Meta-switches": colors.bold & colors.LightSalmon3A
    }

    # Redis flags
    redis_conf = []
    host = cli.SwitchAttr(["-H", "--host"], str, group=group,
                          mandatory=True, help="Le nom de l'host du serveur redis")
    port = cli.SwitchAttr(["-P", "--port"], str, group=group,
                          mandatory=True, help="Le numero de port du serveur redis")
    db = cli.SwitchAttr(["-D", "--db"], str, group=group,
                        mandatory=True, help="Numero de la db redis")

    # Operation flags
    key_pattern = cli.SwitchAttr(["-L", "--list-key"], str, group=group,
                                 mandatory=True, help="Le nom ou le pattern de la cle de liste redis")
    docs_to_publish_count = cli.SwitchAttr(["-N", "--count"], int, group=group,
                                           default=1000, help="Le nombre de documents a aller chercher et a publier)")
    show_progress_bar = cli.Flag(["-S", "--show_progress_bar"], default=False, group=group,
                                 help="Option d'afficher la progress bar lorsqu'on publish les documents sur le channel")

    def main(self):
        super().main()

        lpl.warning('Starting script {}'.format(os.path.basename(__file__)))

        self.connect_redis(self.host, self.port, self.db)

        # Get all keys that match the parttern
        for list_key in self.redis_conf.scan_iter(self.key_pattern):
            channel_key = list_key.decode("utf-8") + '_CHANNEL'

            # Publish documents
            self.publish_key(list_key, channel_key,
                             self.docs_to_publish_count, self.show_progress_bar)

    def connect_redis(self, host, port, db):
        config = {
            'host': host,
            'port': port,
            'db': db
        }

        try:
            self.redis_conf = redis.StrictRedis(**config)
            lpl.info('Current redis configuration => Host : {h}, Port : {p}, DB : {d}'.format(
                h=host, p=port, d=db))

        except Exception as e:
            lpl.error('Cannot configure redis')
            lpl.error(e)
            raise e

    def publish_key(self, list_key, channel_key, docs_to_publish_count, show_progress_bar):
        if(docs_to_publish_count == 0):
            docs_to_publish = []
        else:
            docs_to_publish = self.redis_conf.lrange(
                list_key, abs(docs_to_publish_count)*-1, -1)

        lpl.debug('Documents to publish from key {k} to channel {c}: {d}'.format(
            k=list_key, c=channel_key, d=docs_to_publish))
        lpl.info('Documents to publish from key {k} to channel {c}: {d},'
                 ' Show progress bar :  {s}'.format(k=list_key, c=channel_key,
                                                    d=channel_key, s=show_progress_bar))

        range_function = cli.terminal.Progress.range if show_progress_bar else range
        self.publish(channel_key, docs_to_publish, range_function)

        lpl.info('Published {} documents'.format(str(len(docs_to_publish))))

    def publish(self, channel_key_name, docs_to_publish, range_function):
        for i in range_function(len(docs_to_publish)):
            try:
                lpl.debug('Publishing {d} in {c} channel'.format(
                    d=docs_to_publish[i], c=channel_key_name))
                self.redis_conf.publish(channel_key_name, docs_to_publish[i])

            except Exception as e:
                lpl.error('Cannot publish {d} in {c} channel'.format(
                    d=docs_to_publish[i], c=channel_key_name))
                lpl.error(e)
                raise e


if __name__ == "__main__":
    Publisher.run()
