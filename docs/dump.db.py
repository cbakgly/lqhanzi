#!/usr/bin/env python

import sys
import getopt
import commands

BUSINESS = ["mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi lq_credits > lq_credits.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi lq_credits_redeem > lq_credits_redeem.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi lq_diaries > lq_diaries.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi lq_hanzi_parts > lq_hanzi_parts.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi lq_hanzi_radicals > lq_hanzi_radicals.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi lq_hanzi_set > lq_hanzi_set.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi lq_inter_dict_dedup > lq_inter_dict_dedup.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi lq_korean_dedup > lq_korean_dedup.sql",
            "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi lq_korean_dup_characters > lq_korean_dup_characters.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi lq_korean_dup_zheng_codes > lq_korean_dup_zheng_codes.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi lq_korean_variants_dict > lq_korean_variants_dict.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi lq_task_packages > lq_task_packages.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi lq_tasks > lq_tasks.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi lq_variants_input > lq_variants_input.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi lq_variants_split > lq_variants_split.sql"]
AUTH = ["mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi auth_group > auth_group.sql",
        "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi user > user.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi user_groups > user_groups.sql"]
OTHER = ["mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi auth_group_permissions > auth_group_permissions.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi auth_permission > auth_permission.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi django_admin_log > django_admin_log.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi django_content_type > django_content_type.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi django_migrations > django_migrations.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi django_session > django_session.sql",
         "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi guardian_groupobjectpermission > guardian_groupobjectpermission.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi guardian_userobjectpermission > guardian_userobjectpermission.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi operation_log > operation_log.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi rbac_actions > rbac_actions.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi registration_profile > registration_profile.sql", "mysqldump -h 192.168.16.3 -ulq -p123456 --hex-blob --default-character-set=binary lqhanzi user_user_permissions > user_user_permissions.sql", ]


def usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def process(arg):
    if arg == 'business':
        for command in BUSINESS:
            (status, output) = commands.getstatusoutput(command)
            print status, output

    elif arg == 'other':
        for command in OTHER:
            (status, output) = commands.getstatusoutput(command)
            print status, output

    elif arg == 'auth':
        for command in AUTH:
            (status, output) = commands.getstatusoutput(command)
            print status, output


def main(argv=None):
    ''' %s [business, other, auth] to dump respectively the data from remote db.
    '''
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise usage(msg)

        for o, a in opts:
            if o in ('-h', "--help"):
                print __doc__
                return 0

        for arg in args:
            process(arg)

    except usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, err.msg, "for help use --help"
        return 2


if __name__ == '__main__':
    sys.exit(main())
