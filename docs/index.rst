Welcome to Flask-Sass's documentation!
=========================================

With Flask-Sass's you can use Sass_ while writing CSS. It'll regenerate
your CSS files from your ``.scss`` (the new "Sassy CSS" formatting) or
``.sass`` ("Sass", the older, "idented syntax").


How does it actually work?
^^^^^^^^^^^^^^^^^^^^^^^^^^

If your Flask application is in ``testing`` or ``debug`` mode, it'll
search your application's ``static_folder``, any loaded modules or
blueprints ``static_folder``'s for any Sass supported files, compares
their modification times and if required, regenerates the CSS into the
same directory.


From Sass_:
	*Sass makes CSS fun again*

Trust me, it greatly simplifies life on those long, long stylesheets.



Instalation
^^^^^^^^^^^

In order to use Flask-Sass you need to have the ``sass`` ruby gem installed::

	sudo gem install --no-ri --no-rdoc --verbose sass


On an Ubuntu system, the ``sass`` ruby gem ``bin`` file is installed to
``/var/lib/gems/1.8/bin/sass`` which is the place Flask-Sass expect's it to be.
If on your system the path to the ``sass`` binary is different, you can also
define ``SASS_BIN_PATH`` on your application's configuration and that path
will be the one used.

To install Flask-Saas you can do::

	pip install Flask-Sass


If you wish the development version::

	pip install git+https://github.com/s0undt3ch/Flask-Sass/zipball/master



Usage
^^^^^

If your application is installed as a system package, this extension
will, most likely, not have the required permissions to write generated CSS
files.

So, the recommended usage would be to use this extension while
developing your applications.
Before releasing your application, delete the previously generated CSS
files if you're not sure they're up-to-date. Start it in `debug` or `testing`
mode once more and visit at least your application's url root. That'll
make this extension regenerate your CSS files which can then be shipped
within your application's package.

Using this extension is as simple as:

.. code-block:: python

	from flask import Flask
	from flaskext.sass import Sass

	app = Flask(__name__)
	sass = Sass(app)


Or, if you need a "deferred" setup:

.. code-block:: python

	from flask import Flask
	from flaskext.sass import Sass

	app = Flask(__name__)
	sass = Sass()

	# Some other app code

	sass.init_app(app)


Links
^^^^^

If you find any bugs, please submit them to here_:

The main repository can be found on my development_ website.
Alternatively you can also get the source from a GitHub_ mirror_
repository.


.. _Sass: http://sass-lang.com/
.. _here: http://dev.ufsoft.org/projects/sass/issues/new
.. _development: http://dev.ufsoft.org/projects/sass/repository
.. _GitHub: https://github.com
.. _mirror: https://github.com/s0undt3ch/Flask-Sass
