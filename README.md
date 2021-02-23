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
            :
        </td>
        <td>
            <a href="https://vppr-test.herokuapp.com/">https://vppr-test.herokuapp.com/</a>
        </td>
    </tr>
    <tr>
        <td style="border:0px">
            <b>Swagger UI</b> 
        </td>
        <td  style="border:0px">
            :
        </td>
        <td style="border:0px">
            <a href="https://vppr-test.herokuapp.com/docs">https://vppr-test.herokuapp.com/docs</a>
        </td>
    </tr>
    <tr>
        <td style="border:0px">
            <b>Redoc</b> 
        </td>
        <td style="border:0px">
            :
        </td>
        <td style="border:0px">
            <a  href="https://vppr-test.herokuapp.com/redoc">https://vppr-test.herokuapp.com/redoc</a>
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