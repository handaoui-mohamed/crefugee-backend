#!flask/bin/python
from app import app, io
# while True:
#     try:
#         app.run(debug=True)
#     except:
#         pass
io.run(app,debug=True)