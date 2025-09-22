from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from starlette_graphene3 import GraphQLApp, make_graphiql_handler  # Temporarily disabled for testing
# from routers import customers, surveys, properties, lookup  # Temporarily disabled for testing
# from graphql_schema import schema  # Temporarily disabled for testing

app = FastAPI(
    title="Survey Management API",
    description="A comprehensive API for managing surveys, customers, and properties",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GraphQL endpoint
# graphql_app = GraphQLApp(schema=schema, on_get=make_graphiql_handler())  # Temporarily disabled for testing
# app.mount("/graphql", graphql_app)  # Temporarily disabled for testing

# Include REST API routers
# app.include_router(customers.router, prefix="/api")  # Temporarily disabled for testing
# app.include_router(surveys.router, prefix="/api")    # Temporarily disabled for testing
# app.include_router(properties.router, prefix="/api") # Temporarily disabled for testing
# app.include_router(lookup.router, prefix="/api")     # Temporarily disabled for testing

@app.get("/")
def read_root():
    return {"message": "Survey Management API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
