"""
Flask-Assets extension.
"""

from flask_assets import Bundle, Environment

assets = Environment()

assets.register({
    'auth_css': Bundle('styles/auth/*.css', filters='cssmin', output='build/auth.min.css'),
    'error_css': Bundle('styles/error/*.css', filters='cssmin', output='build/error.min.css'),
    'home_css': Bundle('styles/home/*.css', filters='cssmin', output='build/home.min.css'),
    'user_css': Bundle('styles/user/*.css', filters='cssmin', output='build/user.min.css'),
    'shared_css': Bundle('styles/shared/*.css', filters='cssmin', output='build/shared.min.css'),
    'shared_js': Bundle('scripts/shared/*.js', filters='jsmin', output='build/shared.min.js'),
})
