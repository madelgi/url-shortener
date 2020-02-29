import os

from url_shortener.url_shortener import create_app
import url_shortener.errors
# import url_shortener.jobs.expire_urls


app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')


if __name__ == '__main__':
    print(os.getenv('ALLOWED_HOSTS')
    app.run(debug=os.getenv('DEBUG'), host='0.0.0.0', port=5001)
