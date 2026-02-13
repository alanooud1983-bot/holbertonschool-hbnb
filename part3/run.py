import os
from app import create_app

# Force database mode
os.environ['USE_DATABASE'] = 'true'

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
