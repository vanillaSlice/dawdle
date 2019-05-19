"""
Exports asset bundles to be used in the UI.
"""

from flask_assets import Bundle

bundles = {
    'app_js': Bundle('scripts/app.js', filters='jsmin', output='build/app.min.js'),
    'app_css': Bundle('styles/app.css', filters='cssmin', output='build/app.min.css'),
}
