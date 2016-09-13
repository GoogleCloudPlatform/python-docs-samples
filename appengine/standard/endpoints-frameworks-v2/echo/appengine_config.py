from google.appengine.ext import vendor
import pkg_resources

# Add any libraries installed in the `lib` folder.
vendor.add('lib')

# The Python runtime declares a "google" package, but so does
# google-endpoints-api-management. Therefore the "google" package must behave
# as a namespace package, otherwise one import or another will fail.
pkg_resources.declare_namespace('google')
