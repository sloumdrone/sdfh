import sys, os, bottle

sys.path = ['/var/www/sdfh.space/'] + sys.path
os.chdir(os.path.dirname(__file__))

import main

main.check_and_build_db()

application = bottle.default_app()
