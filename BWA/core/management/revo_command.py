import inspect
import os
from django.core.management.base import BaseCommand

from core.utils import CommandeUtils, LogUtils


class RevoCommand(BaseCommand):

    def run_from_argv(self, argv):
        # Identification du nom du batch.
        CommandeUtils.init(argv[1])
        super(RevoCommand, self).run_from_argv(argv)
