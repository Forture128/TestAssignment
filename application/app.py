from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from application import routers as r
origins = [
    'localhost:3000',
    'http://localhost:3000'
]


def create_app(version='0.0.0', debug=False):

    app = FastAPI(title="COVID19_Analyst", description="BE support COVID19 Analyst", version=version,
                  debug=debug, servers=[{"url": "/"}],
                  root_path='/',
                  openapi_url="/swagger/swagger.json"
                  )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )

    app.include_router(r.country_route,
                       tags=["Country"],
                       prefix="/data",
                       )
    return app
