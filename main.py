import tornado.ioloop
import tornado.web
import os

# Directory to save uploaded files
UPLOAD_DIR = "web/static/uploads"

# Landing Page Handling
class LandPageRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("web/index.html", uploaded_file=None)

# File Upload Handling
class FileUploadHandler(tornado.web.RequestHandler):
    def post(self):
        fileinfo = self.request.files.get("uploadFile", None)
        if fileinfo:
            filename = fileinfo[0]["filename"]
            filepath = os.path.join(UPLOAD_DIR, filename)

            # Save the uploaded file
            with open(filepath, "wb") as f:
                f.write(fileinfo[0]["body"])

            # Render the page with the uploaded file preview
            self.render("web/index.html", uploaded_file=filename)
        else:
            self.render("web/index.html", uploaded_file=None)

def make_app():
    return tornado.web.Application([
        (r"/", LandPageRequestHandler),
        (r"/upload", FileUploadHandler),  # Endpoint for file uploads
        (r"/web/static/(.*)", tornado.web.StaticFileHandler, {"path": "web/static"})
    ])

if __name__ == "__main__":
    # Ensure the upload directory exists
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # Create and run the Tornado application
    app = make_app()
    app.listen(2040)  # Listen on port 2040
    print("Port open at 2040")
    tornado.ioloop.IOLoop.current().start()
