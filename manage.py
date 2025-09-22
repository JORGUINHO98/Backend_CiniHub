#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cinehub_project.settings")
    from django.core.management import execute_from_command_line # type: ignore
    execute_from_command_line(sys.argv)
