#!/usr/bin/env python3

import argparse
import filecmp
import pathlib as pl
import re
import shutil
import sys
import warnings

# some needed directories as path objects
DOTFILESDIR = pl.Path(__file__).parent.resolve()
HOMEDIR = pl.Path.home()

IS_PYTHON_38 = sys.version_info[1] >= 8


class DotFilesSyncer(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
                description='Sync tool to push and pull dotfiles',
        )
        parser.add_argument(
                '--debug',
                action='count',
                help='Print debug info',
                default=0,
        )
        subparsers = parser.add_subparsers()

        parser_push = subparsers.add_parser('push')
        parser_push.set_defaults(func=self.push)

        command_group = parser_push.add_mutually_exclusive_group()
        command_group.add_argument('--force',
                                   action='store_true',
                                   help='Force override existing files even if '
                                        'they are newer')
        command_group.add_argument('--skip-existing',
                                   action='store_true',
                                   help='Skip overriding existing files with '
                                        'new last-modified time stamps')

        parser_pull = subparsers.add_parser('pull')
        parser_pull.set_defaults(func=self.pull)
        parser_pull.add_argument('--force',
                                 action='store_true',
                                 help='Force override existing files even if '
                                      'they are newer')

        self.parser = parser

    def go(self, options):
        options = self.parser.parse_args(options)

        return options.func(options)

    def push(self, options):
        # first, find all files and directories that could should published
        publishable = self._find_publishable()

        # loop over each file and publish it to $HOME/.path
        for line in publishable:
            # source path
            src = DOTFILESDIR / line
            # build new file path
            dest = HOMEDIR / f'.{line}'

            # file statistics
            src_stat = src.stat()
            dest_stat = dest.stat()

            # check if target is newer than sourrce
            if dest_stat.st_mtime > src_stat.st_mtime \
                    and not filecmp.cmp(src, dest):
                # don't bother any more if user asked to skip existing files
                if options.skip_existing:
                    continue

                # no skipping of existing files, so let's see if they should
                # be overriden
                if not options.force:
                    raise FileExistsError(
                            f'Target {dest!s} exists with a newer '
                            f'last-modified time stamp than the source. If '
                            f'you want to force override, provide the '
                            f'`--force` option. If you don\'t want it '
                            f'overriden, provide the --skip-newer` option.')

            # check if source is directory
            try:
                if src.is_dir():
                    shutil.copytree(src, dest, symlinks=True,
                                    dirs_exist_ok=True)
                else:
                    shutil.copyfile(src, dest, follow_symlinks=True)
            except Exception as e:
                warnings.warn(e, RuntimeWarning)

    def pull(self, options):
        # first, find all files and directories that could should published
        publishable = self._find_publishable()

        # loop over each file and publish it to $HOME/.path
        for line in publishable:
            # source path
            src = HOMEDIR / f'.{line}'
            # build new file path
            dest = DOTFILESDIR \
                   / f'{line}'

            # file statistics
            src_stat = src.stat()
            dest_stat = dest.stat()

            # check if target is newer than sourrce
            if dest_stat.st_mtime > src_stat.st_mtime \
                    and not filecmp.cmp(src, dest):
                # no skipping of existing files, so let's see if they should
                # be overriden
                if not options.force:
                    raise FileExistsError(
                            f'Target {dest!s} exists with a newer '
                            f'last-modified time stamp than the source. If '
                            f'you want to force override, provide the '
                            f'`--force` option.')

            # check if source is directory
            try:
                # if source is a directory, we need to copy it slightly
                # differently
                if src.is_dir():
                    # first, clear the old directory
                    shutil.rmtree(dest)
                    # then copy files over
                    if IS_PYTHON_38:
                        shutil.copytree(src, dest, symlinks=True,
                                        dirs_exist_ok=True)
                    else:
                        # and copy over
                        shutil.copytree(src, dest, symlinks=True)
                else:
                    shutil.copyfile(src, dest, follow_symlinks=True)
            except Exception as e:
                warnings.warn(e, RuntimeWarning)

    def _find_publishable(self):
        # load the ".dotpublish" file
        publish = (DOTFILESDIR / '.dotpublish').read_text().splitlines()

        # regular expression to match any line that starts with a "#"
        re_comment = re.compile('^#.*$')

        # turn all lines into path objects
        return [line for line in publish if not re_comment.match(line)]


if __name__ == '__main__':
    syncer = DotFilesSyncer()
    syncer.go(sys.argv[1:])
