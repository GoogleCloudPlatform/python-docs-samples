import sys
from creator.creator_app import create_app

mode = sys.argv[1] if len(sys.argv) > 1 else 'production'
app = create_app(mode=mode)
if mode == 'development':
    app.run(**app.config.get_namespace('RUN_'))
