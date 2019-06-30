from flask_assets import Bundle, Environment

assets = Environment()

assets.register({
    'home_css': Bundle(
        'styles/home/*.css',
        filters='cssmin',
        output='build/home.min.css',
    ),
    'user_css': Bundle(
        'styles/user/*.css',
        filters='cssmin',
        output='build/user.min.css',
    ),
    'user_js': Bundle(
        'scripts/user/*.js',
        filters='jsmin',
        output='build/user.min.js',
    ),
    'shared_css': Bundle(
        'styles/shared/*.css',
        filters='cssmin',
        output='build/shared.min.css',
    ),
    'shared_js': Bundle(
        'scripts/shared/*.js',
        filters='jsmin',
        output='build/shared.min.js',
    ),
})
