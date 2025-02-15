from django.contrib.admin.models import LogEntry
from django.core.management import BaseCommand
from django.db.models.sql.query import get_field_names_from_opts
from django.utils.translation import gettext_lazy as _

from django_boost.core import get_version


class Command(BaseCommand):

    COMPARISON_OPERATION = {"<=": "lte",
                            ">=": "gte",
                            "=": "exact",
                            "<": "lt",
                            ">": "gt", }

    def get_sortable_fields(self, model):
        return sorted(get_field_names_from_opts(model._meta))

    def _parse_filter(self, condition):
        for op in self.COMPARISON_OPERATION.keys():
            field, op, value = condition.partition(op)
            op = self.COMPARISON_OPERATION.get(op, None)
            if op is not None:
                return {"%s__%s" % (field, op): value}
        raise Exception("""
        Unsupported operation '%s'
        --filter and --exclude supported %s
        """ % (field, ",".join(self.COMPARISON_OPERATION.keys())))

    def parse_filter(self, conditions):
        parsed = {}
        for condition in conditions:
            parsed.update(self._parse_filter(condition))
        return parsed

    def print_log(self, log):
        fmt = "{id} | {action} | {object} | {user} | {time}"
        fmap = {}
        if log.is_addition():
            fmap["action"] = self.style.SUCCESS("Added")
            fmap["object"] = log.object_repr
        elif log.is_change():
            fmap["action"] = self.style.WARNING("Changed")
            fmap["object"] = "%s - %s" % (log.object_repr,
                                          log.get_change_message())
        else:  # log.is_deletion
            fmap["action"] = self.style.ERROR("Deleted")
            fmap["object"] = log.object_repr
        fmap["user"] = log.user.username
        fmap["time"] = log.action_time
        fmap["id"] = log.id
        self.stdout.write(fmt.format_map(fmap))

    def add_arguments(self, parser):
        supported_fields = self.get_sortable_fields(LogEntry)
        supported_fields_str = ", ".join(supported_fields)
        parser.add_argument('-d', '--delete',
                            action='store_true', help='Delete displayed logs.')
        parser.add_argument('--filter', nargs='+',
                            type=str, default=[],
                            help="""Filter the Log to be displayed.
                                    Supported filed is %s.
                                    e.g. "action_time>=2019-8-22" """
                            % supported_fields_str)
        parser.add_argument('--exclude', nargs='+',
                            type=str, default=[],
                            help="""Exclude the Log to be displayed.
                                    Supported filed is same as --filter.
                                    e.g. "user__username=admin" """)
        parser.add_argument('--order_by', nargs='+',
                            type=str, default=['action_time'],
                            help="""Order of Log to be displayed.
                                    Supported filed is %s.
                                    e.g. "-action_flag" """
                            % supported_fields_str)

    def handle(self, *args, **options):
        queryset = LogEntry.objects.all()

        queryset = queryset.filter(**self.parse_filter(options['filter']))
        queryset = queryset.exclude(**self.parse_filter(options['exclude']))

        queryset = queryset.order_by(*options['order_by'])

        if queryset.count() == 0:
            self.stderr.write('No logs')
            return
        self.stdout.write("id | action | detail | user | time")
        for log in queryset:
            self.print_log(log)
        if options['delete']:
            answer = input(_("Do you want to delete these logs [y/n]?"))
            if answer.lower() in ["y", "yes"]:
                queryset.delete()
                self.stdout.write('delete complete')
            else:
                self.stderr.write('operation canceled')
            return

    def get_version(self):
        return get_version()
