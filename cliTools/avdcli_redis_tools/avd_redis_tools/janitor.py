import os
import sys
import time

import redis
from avdcli import AVDApp
from avdlogger import lpl
from plumbum import cli, colors

from avd_redis_tools import __version__


class Janitor(AVDApp):

    def __init__(self, *args):
        super().__init__(*args)

    # Script flags
    PROGNAME = colors.bold & colors.yellow2
    VERSION = colors.bold & colors.yellow2 | __version__
    DESCRIPTION = colors.bold & colors.Grey84 | "[FR] L'outil de ligne de commande janitor sert a supprimer les documents d'une cle redis de type liste et d'en conserver un certain nombre parmis les plus recents." + \
        '\n' + \
        "[EN] The janitor command line tool is used to delete documents in a redis key (list type) and keeps any number of most recent ones."
    COLOR_USAGE = colors.bold & colors.LightYellow3
    group = '1 Janitor'
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
    docs_to_kept_count = cli.SwitchAttr(["-N", "--keep"], int, group=group, default=1000,
                                   help="Le nombre de documents a garder dans la liste de la cle (parmis les plus recents)")
    key_pattern = cli.SwitchAttr(["-K", "--key"], str, group=group,
                                mandatory=True, help="Le nom ou le pattern de la cle de la liste redis")

    def main(self):
        super().main()

        lpl.warning('Starting script {}'.format(os.path.basename(__file__)))

        self.connect_redis(self.host, self.port, self.db)

        self.trim_keys(self.key_pattern, self.docs_to_kept_count)

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

    def trim_keys(self, key_pattern, docs_to_kept_count):
         # Get all keys that match the parttern
        for list_key in self.redis_conf.scan_iter(key_pattern):

            lpl.info('List name : {l}, Docs to keep {d}'.format(
                l=list_key, d=abs(docs_to_kept_count)))
            old_list_length = self.redis_conf.llen(list_key)
            lpl.info('Key {k} contains {o} documents'.format(
                k=list_key, o=old_list_length))

            self.trim_key(list_key, docs_to_kept_count)

            new_list_length = self.redis_conf.llen(list_key)
            lpl.info('Key {k} contains {n} documents'.format(
                k=list_key, n=new_list_length))

            docs_deleted_count = old_list_length - new_list_length
            lpl.info('Deleted {d} documents from {k}'.format(
                d=docs_deleted_count, k=list_key))

    def trim_key(self, list_key, docs_to_kept_count):
        if(abs(docs_to_kept_count) == 0):
            try:
                self.redis_conf.delete(list_key)
                lpl.debug('Key {} was deleted'.format(list_key))

            except Exception as e:
                lpl.error('Cannot delete key {}'.format(list_key))
                lpl.error(e)
                raise e
        else:
            try:
                self.redis_conf.ltrim(list_key, abs(docs_to_kept_count)*-1, -1)
                lpl.debug('Key {} was trimed'.format(list_key))

            except Exception as e:
                lpl.error('Cannot trim key {}'.format(list_key))
                lpl.error(e)
                raise e


if __name__ == "__main__":
    Janitor.run()
