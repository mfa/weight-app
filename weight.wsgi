import os, sys
import site

site.addsitedir(os.path.join(os.path.dirname(__file__),
                             'env_weight/lib/python2.6/site-packages'))

sys.path[0:0] = [
       os.path.join(os.path.dirname(__file__), 'env_weight'),
       os.path.join(os.path.dirname(__file__), 'weight'),
    ]

from main import app as application
activate_this = os.path.join(os.path.dirname(__file__), 'weight/main.py')
execfile(activate_this, dict(__file__=activate_this))
