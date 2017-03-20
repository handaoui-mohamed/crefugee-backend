#!flask/bin/python
from app import app, io
# Run app using socketIO
io.run(app,debug=True)