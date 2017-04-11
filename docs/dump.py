#!/usr/bin/env python

import sys
import getopt
import commands

BUSINESS = ["lq_credits", "lq_credits_redeem", "lq_diaries", "lq_hanzi_parts", "lq_hanzi_radicals", "lq_hanzi_set", "lq_inter_dict_dedup", "lq_korean_dedup", "lq_korean_dup_characters", "lq_korean_dup_zheng_codes", "lq_korean_variants_dict", "lq_task_packages", "lq_tasks", "lq_variants_input", "lq_variants_split"]
AUTH = ["auth_group", "user", "user_groups"]
OTHER = ["auth_group_permissions", "auth_permission", "django_admin_log", "django_content_type", "django_migrations", "django_session", "guardian_groupobjectpermission", "guardian_userobjectpermission", "operation_log", "rbac_actions", "registration_profile", "user_user_permissions"]

COMMAND = 'mysqldump -h %s -u %s -p %s --hex-blob --default-character-set=binary %s %s > %s.sql'


def usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def dump(param, tables):
    for t in tables:
        command = COMMAND % (param['host'], param['user'], param['passwd'], param['db'], t, t)
        (status, output) = commands.getstatusoutput(command)
        print (status, output)


def process(param, arg):
    if arg == 'business':
        dump(param, BUSINESS)

    elif arg == 'other':
        dump(param, OTHER)

    elif arg == 'auth':
        dump(param, AUTH)


def main(argv=None):
    """ %s [business, other, auth] to dump respectively the data from remote db.
    """

    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h:u:p:d:", ["help", "host=", "user=", "password=", "database="])
        except getopt.error, msg:
            raise usage(msg)

        param = {}
        for o, a in opts:
            if o == "--help":
                print(main.__doc__%(argv[0]))
                return 0
            if o in ('-h', '--host'):
                param['host'] = a
            if o in ('-u', '--user'):
                param['user'] = a
            if o in ('-p', '--password'):
                param['passwd'] = a
            if o in ('-d', '--database'):
                param['db'] = a

        for arg in args:
            process(param, arg)

    except usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, err.msg, "for help use --help"
        return 2


if __name__ == '__main__':
    sys.exit(main())
