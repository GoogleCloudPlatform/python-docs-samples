# appengine_config.py
import pkg_resources
from google.appengine.ext import vendor

# Set path to your libraries folder.
path = 'lib'

# Add libraries installed in the path folder.
vendor.add(path)

# Add libraries to pkg_resources working set to find the distribution.
pkg_resources.working_set.add_entry(path)
pkg_resources.get_distribution('google-cloud-tasks')
