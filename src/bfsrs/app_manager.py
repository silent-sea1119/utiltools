

class AppManager(object):

   def __init__(self):
      pass


   def add_app(self, app_name, default_limits=None, static_path=None):
      pass

   def add_app_conf(self, app_conf):
      '''
      app_conf = {
         'app_name' : 'required',
         'default_limits' : 'optional',

         'accepts' : ['head', 'get', 'post'],

         'templates_path' : 'path', #default is <app_name>/templates
         'backend_path' : 'path', #default is <app_name>/src
         'react_path' : 'path', #default is <app_name>/jsx
         'sass_path' : 'path', #default is <app_name>/sass

         'static_prefix' : 'static', #if None, then static. '' for empty #TODO
         'static_path' : 'optional', #TODO

         'conf_modifier' : <get_final_conf/conf_modifier_func>, #default is None

         'static_urls' : [ #optional
            { 'name' : 'url_var_name2'
              'url' : 'route_url', #url in flask
              'path' : 'path' #actual path on disk relative to the app group root
            },
            {
               'name' : 'url_var_name2',
               ...
            }
            #'base_url' : 'actual_path',
            #'base_url2' : 'actual_path'
         ],

         'dynamic_urls' : [ #same as add_path
            { 'url' : 'base_url',
              'func' : view_function,
              'prior' : <priority>,
              'limit' : <limit>,
              'conf_modifier' : get_final_conf
            },
            { ... }
         ]

      }
      '''
      pass



   def add_path(self, path, page_view_func, app_name=None, prior=None, limit=None):
      '''
      #bad args to page_view_func = page_view_func(app, flask_req)

      args to page_view_func =
      def page_view_func(**url_args, *etc, conf = {
                                             'template_conf' : template_conf = {
                                                'root' : 'site_root_path',
                                                'domain' : 'site_domain',
                                                'is_mobile' : is_mobile
                                             }
                                             'template_path' : <path_to_view_template>,

                                             'req' : flask_request,
                                             'sess' : flask_session,

                                             'flask_app' : flask_app, #TODO: is this needed?
                                             'app_manager' : app_manager, #TODO: is this needed?

                                             'is_post' : is_post,
                                             'is_get' : is_get,
                                             'is_head' : is_head,

                                           })

      TODO: how is this class gonna be used? do we need app_name in add_path?
      '''
      pass


   def render_template(self, name, *args, **kwargs):
      pass

   pass

