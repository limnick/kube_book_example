import tornado.ioloop
import tornado.web
import os

from google.cloud import storage

GCLOUD_ENV_VAR = 'GCLOUD_STORAGE_BUCKET_TARGET'

client = storage.Client()
bucket = client.get_bucket(os.getenv(GCLOUD_ENV_VAR))
print("connected to gcloud bucket")


class MainHandler(tornado.web.RequestHandler):
  def get(self):
    blob_iterator = bucket.list_blobs(max_results=10)
    for blob in blob_iterator:
      self.write("{} {}<br>".format(blob.size, blob.name))

class HealthHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("OK")
    self.set_header('Content-Type', 'text/plain')

def make_app():
  tornado_app = tornado.web.Application([
    (r"/", MainHandler),
    (r"/health", HealthHandler),
  ])
  return tornado_app


if __name__ == "__main__":
  app = make_app()
  app.listen(8888, address='0.0.0.0')
  tornado.ioloop.IOLoop.current().start()
