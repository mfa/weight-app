
Weight App
==========

This app was written out of a personal need.
I want to track my weight every day using my Android smartphone.
Because of this need the forms and lists are optimized for touch input.


initial installation
--------------------

::

  virtualenv env_weight
  . env_weight/bin/activate
  pip install -r pip-requirements.txt


run
---

::

  . env_weight/bin/activate
  cd weight
  python main.py


run tests
---------

::

  . env_weight/bin/activate
  cd weight/tests
  python maintest.py


future work
-----------

 * more tests
 * plotting of weight data
 * export to xml
