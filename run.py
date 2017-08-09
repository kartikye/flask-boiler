# Run a test server.
from app import app

app.run(host='0.0.0.0', port=4016, debug=True)