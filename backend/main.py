from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
import graphene
from routers import customers, surveys, properties, lookup
from graphql_schema_simple import schema

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
@app.post("/graphql")
@app.get("/graphql")
@app.post("/graphql/")  # Handle trailing slash
@app.get("/graphql/")   # Handle trailing slash
async def graphql_endpoint(request: Request):
    if request.method == "GET":
        # Return GraphiQL interface for GET requests
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>GraphQL Playground</title>
            <link href="https://cdn.jsdelivr.net/npm/graphiql@1.5.16/graphiql.min.css" rel="stylesheet" />
        </head>
        <body style="margin: 0;">
            <div id="graphiql" style="height: 100vh;"></div>
            <script crossorigin src="https://unpkg.com/react@17/umd/react.production.min.js"></script>
            <script crossorigin src="https://unpkg.com/react-dom@17/umd/react-dom.production.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/graphiql@1.5.16/graphiql.min.js"></script>
            <script>
                ReactDOM.render(
                    React.createElement(GraphiQL, {
                        fetcher: function(params) {
                            return fetch('/graphql', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify(params),
                            }).then(response => response.json());
                        }
                    }),
                    document.getElementById('graphiql')
                );
            </script>
        </body>
        </html>
        """)
    
    # Handle POST requests
    try:
        body = await request.json()
        query = body.get("query", "")
        variables = body.get("variables", {})
        
        result = schema.execute(query, variables=variables)
        
        response_data = {"data": result.data}
        if result.errors:
            response_data["errors"] = [str(error) for error in result.errors]
            
        return JSONResponse(response_data)
    except Exception as e:
        return JSONResponse({
            "errors": [str(e)]
        }, status_code=400)

# Include REST API routers
app.include_router(customers.router, prefix="/api")
app.include_router(surveys.router, prefix="/api")
app.include_router(properties.router, prefix="/api")
app.include_router(lookup.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Survey Management API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
