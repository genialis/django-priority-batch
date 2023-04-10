##########
Change Log
##########

All notable changes to this project are documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`_.


==================
5.0.0 - 2023-04-09
==================

Changed
=======
- **BACKWARD INCOMPATIBLE:** Require ``Django 4.2``
- Add support for ``Python 3.11``
- Drop support for ``Python 3.6`` and ``Python 3.7``
- Bump ``setuptools`` version


================
4.0.0 2022-02-16
================

Changed
=======
- **BACKWARD INCOMPATIBLE:** Drop support for Django 3.0 and 3.1
- Add support for Python 3.10


================
3.0.0 2021-04-19
================

Changed
=======
- **BACKWARD INCOMPATIBLE:** Require Django 3.x


================
2.2.0 2020-12-20
================

Added
------
- Add support for Python 3.9


================
2.1.0 2020-02-07
================

Added
-----
- Add support for Python 3.8


================
2.0.0 2019-04-26
================

Changed
-------
- Require Django 2.x


================
1.1.1 2018-10-22
================

Fixed
-----
- Rollback batcher transaction at the beginning of middleware if is left
  over from previous request


================
1.1.0 2018-10-19
================

Added
-----
- Support using prioritized batcher as a context manager


================
1.0.0 2018-10-19
================

Initial version
