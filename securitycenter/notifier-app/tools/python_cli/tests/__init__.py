"""Makes upfolder available to import."""
import sys
import os

MY_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MY_PATH + '/../')
