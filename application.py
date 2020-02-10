import os

from url_shortener.url_shortener import create_app
import url_shortener.errors


app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
