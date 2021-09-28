from application.app import app, server
from application.components.layouts.layout import make_layout

app.layout = make_layout()

if __name__ == '__main__':
    app.run_server(debug=True)