gunicorn app.wsgi:application -w 2 -b :8000 --timeout 120

from iz import app
if __name__ == "__main__":
  app.run()
