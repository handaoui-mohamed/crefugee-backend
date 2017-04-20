from flask_restplus import reqparse
import werkzeug


post_file = reqparse.RequestParser()
post_file.add_argument('post_image', type=werkzeug.datastructures.FileStorage,\
                        help='Post\'s cover image', required=True, location='files')

profile_image = reqparse.RequestParser()
profile_image.add_argument('profile_image', type=werkzeug.datastructures.FileStorage,\
                        help='Profile image', required=True, location='files')

legal_document = reqparse.RequestParser()
legal_document.add_argument('legal_document', type=werkzeug.datastructures.FileStorage,\
                        help='Upload legal document for a refugee', required=True, location='files')

upload_filename = reqparse.RequestParser()
upload_filename.add_argument('filename', type=str, help='File name to be served', required=True)


user_file = reqparse.RequestParser()
user_file.add_argument('filename', type=str, help='File name to be served', required=True)
user_file.add_argument('username', type=str, help='Profile\'s username', required=True)