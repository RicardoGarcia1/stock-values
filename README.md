# COMO DESCARGAR IMAGEN SUBIDA POR .gitlab-ci.yml

## Crear mi personal token

User -> Preferences -> Accesss Tokens -> Create Token 

Mandatory scope: read_repository

## Login in GitLab registry: 

docker login registry.gitlab.com -u ricardogarcia283 -p <TOKEN>

## Docker run

docker run -d -p 8001:8000 -e DB_URL=postgresql://admin:KCxJ5SODxXsGfbBU8dE5dnahefBgjkoI@dpg-d2jcd4be5dus738ud4v0-a.oregon-postgres.render.com/fastapi_01kh -e secret_key=mi_clave_secreta_super_segura -e algorithm=HS256 registry.gitlab.com/ricardogarcia283-group/auth-jwt:latest


## Stack AWS 

ALB -> AWS LAMBDA -> DYNAMODB 

# Step 1 
Add Mangum handler in the main file
# Step 2
Install dependecies in the working directory:
```
pip install -r requirements.txt -t .
```
# Step 3 
Package the folder 
```
zip -r app.zip .
```
# Step 4 
Create Lambda fuction
- Create the lambda function 
- Update the code from the .zip
- Set the handler(Code -> Configuración del tiempo de ejecución -> Controlador)

# Step 5 
Create ALB

- Create Target Group



# Git 

## eliminar archivos sin seguimiento 

git clean -fdx


# AWS 
## Lambda 
### Update Lambda code
docker build -t lambda-fastapi .
docker create --name extract lambda-fastapi
docker cp extract:/var/task/lambda.zip ./lambda.zip
docker rm extract

### SAM 

sam build --use-container
sam local start-api


### Localstack 

