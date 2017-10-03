
import sys
sys.path.append('/root/orgs/Kosandr')

import user_acc


route_args = {
   'strict_slashes' : False,
   'methods' : ['POST', 'GET']
}


def init_lib(app):

   @app.route('/robots.txt', **route_args)
   def robots():
      #render_template('robots.txt')
	return '''User-agent: *\nDisallow:'''



