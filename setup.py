# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
import codecs
import os
from setuptools import setup, find_packages
from version import get_version

name='gs.group.list.sender'
version = get_version()

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.rst"),
                 encoding='utf-8') as f:
    long_description += '\n' + f.read()

install_requires = [
    'setuptools',
    'SQLAlchemy',
    'zope.cachedescriptors',
    'zope.component',
    'zope.interface',
    'gs.cache',
    'gs.core',
    'gs.database',
    'gs.dmarc',
    'gs.email',
    'gs.group.member.base',
    'gs.profile.email.relay',
    'Products.GSGroup',
]

setup(name=name,
      version=version,
      description="Sending email messages from a GroupServer group",
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          "Environment :: Web Environment",
          "Framework :: Zope2",
          "Intended Audience :: Developers",
          'License :: OSI Approved :: Zope Public License',
          "Natural Language :: English",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='group, list, mailing list, email',
      author='Michael JasonSmith',
      author_email='mpj17@onlinegroups.net',
      url='https://github.com/groupserver/{0}'.format(name),
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['.'.join(name.split('.')[:i])
                          for i in range(1, len(name.split('.')))],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require={'docs': ['Sphinx', ], },
      test_suite="gs.group.list.sender.tests.test_all",
      entry_points="""# -*- Entry points: -*-
      """,)
