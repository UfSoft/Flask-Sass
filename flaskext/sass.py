# -*- coding: utf-8 -*-
"""
    flaskext.sass
    ~~~~~~~~~~~~~

    A small Flask extension that makes it easy to use Sass_ with your Flask
    application.

    :copyright: (c) 2011 by Pedro Algarvio.
    :license: BSD, see LICENSE for more details.
"""

__version__         = '0.8'
__package_name__    = 'Flask-Sass'
__summary__         = "A small Flask extension that makes it easy to use " + \
                      "Sass with your Flask application."
__author__          = 'Pedro Algarvio'
__email__           = 'pedro@algarvio.me'
__license__         = 'BSD'
__url__             = 'http://dev.ufsoft.org/projects/sass'
__description__     = __doc__


import os
import logging
import warnings
import subprocess
from flask import Blueprint
log = logging.getLogger(__name__)

class Sass(object):
    def __init__(self, app):
        if app:
            self.init_app(app)

    def init_app(self, app):
        log.debug("Setting up Flask-Sass")
        self.app = app
        self.app.sass = self
        self.continuous_processing = app.debug or app.testing
        self.sass_bin_path = app.config.get(
            'SASS_BIN_PATH', '/var/lib/gems/1.8/bin/sass'
        )
        self.process_args = [self.sass_bin_path]
        if self.continuous_processing:
            self.process_args.append("--style=expanded")
            self.app.before_request(self.find_searcheable_paths)
        else:
            self.process_args.append("--style=compressed")
            self.app.before_first_request(self.find_searcheable_paths)
        if os.name != "nt":
            self.process_args.append("--unix-newlines")

    def find_searcheable_paths(self):
        log.debug("Searching for Sass files for Flask application: %s",
                  self.app.name)
        for fsass, fcss in self.find_sass_files(self.app.static_folder):
            self.generate_css_from_sass(fcss, fsass)

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            if self.app.enable_modules:

                for module in self.app.modules.values():
                    if isinstance(module, Blueprint):
                        # Since this "module" is actually a
                        # blueprint, handle it bellow
                        continue
                    if not module.static_folder:
                        continue
                    log.debug("Searching for Sass files for Module: %s",
                              module.name)
                    for fsass, fcss in self.find_sass_files(module.static_folder):
                        self.generate_css_from_sass(fcss, fsass)

        for blueprint in self.app.blueprints.values():
            if not blueprint.static_folder:
                continue
            log.debug("Searching for Sass files for Blueprint: %s",
                      blueprint.name)
            for fsass, fcss in self.find_sass_files(blueprint.static_folder):
                self.generate_css_from_sass(fcss, fsass)

        if hasattr(self.app, 'theme_manager'):
            for theme in self.app.theme_manager.themes.values():
                for fsass, fcss in self.find_sass_files(theme.static_path):
                    self.generate_css_from_sass(fcss, fsass)

    def find_sass_files(self, search_path):
        log.debug("Finding *.{sass,scss} files under %s", search_path)
        for path, subdirs, filenames in os.walk(search_path):
            for f in filenames:
                if f.endswith('.sass'):
                    yield (
                        os.path.join(path, f),
                        os.path.join(path, f.replace('.sass', '.css'))
                    )
                elif f.endswith('.scss'):
                    yield (
                        os.path.join(path, f),
                        os.path.join(path, f.replace('.scss', '.css'))
                    )

    def generate_css_from_sass(self, css_file, sass_file):
        if not os.path.isfile(css_file):
            css_mtime = -1
        else:
            css_mtime = os.path.getmtime(css_file)

        sass_mtime = os.path.getmtime(sass_file)
        if sass_mtime >= css_mtime:
            log.info("Generating %s from %s",
                     os.path.basename(sass_file),
                     os.path.basename(css_file))
            args = self.process_args + [sass_file, css_file]
            log.debug("Subprocess call \"%s\"", ' '.join(args))
            try:
                retcode = subprocess.call(args, shell=False)
                if retcode != 0:
                    log.error("Failed to compile %s", sass_file)
                    if os.path.isfile(css_file):
                        os.remove(css_file)
            except OSError, err:
                log.exception(err)
                if os.path.isfile(css_file):
                    os.remove(css_file)

