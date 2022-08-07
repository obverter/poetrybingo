from poetry_factory import poetry_factory


@poetry_factory.route("/")
@poetry_factory.route("/index")
def index():
    user = {'username': 'Billiam'}
    return '''
<html>
    <head>
        <title>Home Page - Microblog</title>
    </head>
    <body>
        <h1>Hello, ''' + user['username'] + '''!</h1>
    </body>
</html>'''
