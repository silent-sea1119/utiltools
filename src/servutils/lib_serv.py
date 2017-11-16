
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



def get_user_agent(r, if_empty=''): #if_empty can be None
   return r.headers.get('User-Agent', if_empty)

def is_google_bot(r):
   return 'googlebot' in get_user_agent(r).lower()

def get_cf_data(r):
   get_env = r.environ.get
   ip = get_env('HTTP_CF_CONNECTING_IP', None)
   country = get_env('HTTP_CF_IPCOUNTRY', None)
   ray = get_env('HTTP_CF_RAY', None)
   visitor = get_env('HTTP_CF_VISITOR', None)

   ret = {
      'ip' : ip,
      'country' : country,
      'ray' : ray,
      'visitor' : visitor
   }

   return ret

def get_real_ip_addr(r, is_under_cloudflare=True):

   #if not proxy, then request.remote_addr
   http_x_real_ip = r.environ.get('HTTP_X_REAL_IP', request.remote_addr)

   if not is_under_cloudflare:
      return http_x_real_ip

   cf_data = get_cf_data(r)

   ip = cf_data['ip']
   if ip is None:
      return http_x_real_ip

   #print(ip)
   return ip






