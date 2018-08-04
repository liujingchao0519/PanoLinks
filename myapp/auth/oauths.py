# from myapp import oauth
# from flask import current_app
#
#
# credentials = current_app.config['OAUTH_CREDENTIALS']
#
# facebook = oauth.remote_app(
#     'facebook',
#     consumer_key=credentials['facebook']['id'],
#     consumer_secret=credentials['facebook']['secret'],
#     request_token_params={'scope': 'email'},
#     base_url='https://graph.facebook.com',
#     request_token_url=None,
#     access_token_url='/oauth/access_token',
#     access_token_method='GET',
#     authorize_url='https://www.facebook.com/dialog/oauth'
#
#
# )