**Backend**
==

Repository for the backend of VPPR Depression Detection System created using [FastAPI](https://fastapi.tiangolo.com/)

Requirements
==
- MongoDB
- Python

Local Development
==
- Install the dependencies

    ```bash
    python -m pip install -r requirements.txt
    ```
- Specify Environment variables
    
    ```
    SECRET_KEY=SECRET KEY for signing JWT token
    
    MONGO_DETAILS=MongoDBConnectionString
    ```
- Run the project
    
    ```bash
    python -m app
    ```


Deployment
==

<table style="border:0px">
    <tr>
        <td>
            <b>Deployed Site</b> 
        </td>
        <td>
            <a href="https://backend.vppr.tech/">https://backend.vppr.tech/</a>
        </td>
    </tr>
    <tr>
        <td>
            <b>Swagger UI</b> 
        </td>
        <td>
            <a href="https://backend.vppr.tech/docs">https://backend.vppr.tech/docs</a>
        </td>
    </tr>
    <tr>
        <td>
            <b>Redoc</b> 
        </td>
        <td>
            <a  href="https://backend.vppr.tech/redoc">https://backend.vppr.tech/redoc</a>
        </td>
    </tr>
</table>


Credits
==
Template derived from 
- [Rev-AMP / Backend](https://github.com/rev-amp/backend)
- [markqiu / fastapi-mongodb-realworld-example-app](https://github.com/markqiu/fastapi-mongodb-realworld-example-app)
- [tiangolo
/
full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql/)