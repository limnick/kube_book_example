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
    self.application.request_count += 1
    blob_iterator = bucket.list_blobs(max_results=10)
    for blob in blob_iterator:
      self.write("{} {}<br>".format(blob.size, blob.name))

class HealthHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("OK")
    self.set_header('Content-Type', 'text/plain')

class MetricsHandler(tornado.web.RequestHandler):
  def get(self):
    out_txt = ""
    metric_name = "WithKubeToyServer_requests_total"
    out_txt = out_txt + "# HELP {} Total number of requests".format(metric_name) + "\n"
    out_txt = out_txt + "# TYPE {} counter".format(metric_name) + "\n"
    out_txt = out_txt + "{} {}".format(metric_name, self.application.request_count) + "\n"
    self.write(out_txt)
    self.set_header('Content-Type', 'text/plain')

def make_app():
  tornado_app = tornado.web.Application([
    (r"/", MainHandler),
    (r"/health", HealthHandler),
    (r"/metrics", MetricsHandler),
  ])
  tornado_app.request_count = 0
  return tornado_app


if __name__ == "__main__":
  app = make_app()
  app.listen(8888, address='0.0.0.0')
  tornado.ioloop.IOLoop.current().start()
