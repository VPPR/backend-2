import uvicorn

uvicorn.run('app.server:app', host='0.0.0.0', port=8000, reload=True)
