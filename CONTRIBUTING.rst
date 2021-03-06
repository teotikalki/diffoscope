Contributing
============

The preferred way to report bugs about diffoscope, as well as suggest fixes and
requests for improvements, is to submit reports to the Debian bug tracker for
the ``diffoscope`` package. You can do this over e-mail, simply write an email
as follows:

::

    To: submit@bugs.debian.org
    Subject: <subject>

    Source: diffoscope
    Version: <version>
    Severity: <grave|serious|important|normal|minor|wishlist>


There are `more detailed instructions available
<https://www.debian.org/Bugs/Reporting>`__ about reporting a bug in the Debian bug tracker.

If you're on a Debian-based system, you can install and use the ``reportbug``
package to help walk you through the process.

You can also submit patches to the Debian bug tracker. Start by cloning the `Git
repository <https://anonscm.debian.org/git/reproducible/diffoscope.git/>`__,
make your changes and commit them as you normally would. You can then use
Git's ``format-patch`` command to save your changes as a series of patches that
can be attached to the report you submit. For example:

::

    git clone git://anonscm.debian.org/reproducible/diffoscope.git
    cd diffoscope
    git checkout origin/master -b <topicname>
    # <edits>
    git commit -a
    git format-patch -M origin/master

The ``format-patch`` command will create a series of ``.patch`` files in your
checkout. Attach these files to your submission in your e-mail client or
reportbug.

Uploading the package
=====================

When uploading diffoscope to the Debian archive, please take extra care to make
sure the uploaded source package is correct, that is it includes the files
tests/data/test(1|2).(a|o) which in some cases are removed by dpkg-dev when
building the package. See `#834315 <https://bugs.debian.org/834315>`__ for an example
FTBFS bug caused by this. (See `#735377
<https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=735377#44>`__ and followups
to learn how this happened and how to prevent it)

Please also release a signed tarball::

    $ VERSION=FIXME
    $ git archive --format=tar --prefix=diffoscope-${VERSION}/ ${VERSION} | bzip2 -9 > diffoscope-${VERSION}.tar.bz2
    $ gpg --detach-sig --armor --output=diffoscope-${VERSION}.tar.bz2.asc < diffoscope-${VERSION}.tar.bz2
    $ scp diffoscope-${VERSION}* alioth.debian.org:/home/groups/reproducible/htdocs/releases/diffoscope

After uploading, please also update the version on PyPI using::

   $ python3 setup.py sdist upload --sign

Once the tracker.debian.org entry appears, consider tweeting the release on
``#reproducible-builds`` with::

  %twitter diffoscope $VERSION has been released. Check out the changelog here: $URL

