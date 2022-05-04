import os
import uvicorn
from application import create_app


app = create_app()

is_local = os.getenv('APP_ENV', 'local') == 'local'

if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=3001, reload=is_local, root_path='/')
