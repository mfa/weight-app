import os, sys
import site

site.addsitedir(os.path.join(os.path.dirname(__file__),
                             'env_weight/lib/python2.6/site-packages'))

sys.path[0:0] = [
       os.path.join(os.path.dirname(__file__), 'env_weight'),
       os.path.join(os.path.dirname(__file__), 'weight'),
    ]

from run import app as application
