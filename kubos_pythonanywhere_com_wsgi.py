# This file contains the WSGI configuration required to serve up your
# web application at http://kubos.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.

import webapp2
#webapp2.application

from server import kubos
from server import static_file_handler

routes = [
    ('/', kubos.KubosBlocksApp),
    ('/solids', kubos.KubosSolidsApp),
    ('/boxes', kubos.KubosBlocksApp),
    ('/blocks', kubos.KubosBlocksApp),
    ('/upload_stl', kubos.UploadStl),
    ('/(.+)', static_file_handler.StaticFileHandler),
]

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'something-very-very-secret',
}

application = webapp2.WSGIApplication(routes=routes, debug=True, config=config)
