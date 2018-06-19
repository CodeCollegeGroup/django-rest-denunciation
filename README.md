[![Build Status](https://travis-ci.org/CodeCollegeGroup/django-rest-denunciation.svg?branch=master)](https://travis-ci.org/CodeCollegeGroup/django-rest-denunciation)
[![Maintainability](https://api.codeclimate.com/v1/badges/326580a7635149dc314b/maintainability)](https://codeclimate.com/github/CodeCollegeGroup/django-rest-denunciation/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/326580a7635149dc314b/test_coverage)](https://codeclimate.com/github/CodeCollegeGroup/django-rest-denunciation/test_coverage)

## Executando o projeto
Utilizando o docker e docker-compose:
`sudo docker-compose up`
e o servidor estará escutando na porta 8000 do localhost, depois é necessário apenas que abra o link no navegador `localhost:8000`

## Rotas da API Restful

## Rotas para Administradores

### Registrar um novo Administrador
  ```
  /api/domains/admins/

  * Methods allowed: ['POST']
  * request data:
    * username: String (required);
    * password: String (required);
    * email: String (optional);
    * first_name: String (optional);
    * last_name: String (optional)
    * header: 'Authorization: JWT authentication_token'
  * response data:
    * ok: administrator registered
  ```

### Autenticação do Administrador
```
/api/domains/authenticate/

* Methods allowed: ['POST']
* request data:
  * username: String,
  * password: String,
  * header: 'Content-type: application/json'

* response data:
  * token: String,
```

### Recuperar chave de um Domínio
  ```
  /api/domains/recover-domain-key/

  * Methods allowed: ['GET']
  * requires domain administrator authentication
  * request data:
    * application_name: String
    * header: 'Authorization: JWT authentication_token'
  ```

### Resetar senha de um Administrador
  ```
  /api/domains/admins/

  * Methods allowed: ['PUT']
  * request data:
    * email: String
    * header: 'Content-type: application/json'
  ```

## Rotas para Domínios

### Rota para criação de um Domínio
  ```
  /api/domains/domains/

  * Methods allowed: ['POST']
  * request data:
    * uri: String
    * application_name: String,
    * administrator: int
    * header: 'Content-type: application/json'
  ```
## Rotas para Denuncias
  
### Rota para criação e listagem de denuncias 
  ```
  /api/denunciations/denunciation/

  * Methods allowed: ['POST', 'GET']
  
  POST:
  * request data:
    * key: String (required)
    * denunciable.denunciable_id: Integer (required)
    * denunciable.denunciable_type: String (required)
    * denunciation.categories: String list (optional)
    * denunciation.justification: String (required)
    * denunciation.denouncer: String (optional)
    * header: 'Content-type: application/json'
    
   GET:
   * request data:
    * header: '**{'HTTP_KEY': 'key'}' (required)
   * response data:
    * list[
      * url: Link
      * current_state: String
      * justification: String
      * denunciable: Link
      * categories: Link list (may not be)
      * denouncer: Link (may not be)
      * evaluation: String (may not be)
      * fake: Boolean (may not be)
    *] 
  ```
### Rota para listar denuncia com prioridade
  ```
   /api/denunciations/denunciation-queue/
   
   * Methods allowed: ['GET']
   * query_params:
    * start: Date 'yyyy-mm-dd' (optional)
    * end: Date 'yyyy-mm-dd' (optional)
    * queries: ['gravity','-gravity','date','-date'] (optional)
   * response data:
    * denunciation_queue: list of urls to denunciation
   
  ```
### Rota para mostrar e deletar uma denuncia
 ```
  /api/denunciations/denunciation/id/

  * Methods allowed: ['GET', 'DELETE']
  
   GET:
   * request data:
    * header: '**{'HTTP_KEY': 'key'}' (required)
   * response data:
    * url: Link
    * current_state: String
    * justification: String
    * denunciable: Link
    * categories: Link list (may not be)
    * denouncer: Link (may not be)
    * evaluation: String (may not be)
    * Fake: Boolean (may not be)
    
  DELETE:
  * request data:
    * header: '**{'HTTP_KEY': 'key'}' (required) 
  ```
  ### Rotas para mudança de estado de uma denuncia
  ```
  * Methods allowed: ['GET', 'PATCH']
  
   GET:
   /api/denunciations/denunciation/id/null
   
    * request data:
      * header: '**{'HTTP_KEY': 'key'}' (required)
  
   /api/denunciations/denunciation/id/waiting
   
    * require denunciation state be in nullstate
    * request data:
      * header: '**{'HTTP_KEY': 'key'}' (required)
  
   /api/denunciations/denunciation/id/evaluating
   
    * require denunciation state be in waitingstate
    * request data:
      * header: '**{'HTTP_KEY': 'key'}' (required)
  
   PATCH: 
   /api/denunciations/denunciation/id/done
   
   * require denunciation state be in evaluatingstate
   * request data:
     * evaluation: String (required)
     * fake: Boolean (required)
     * header: '**{'HTTP_KEY': 'key'} Content-type: application/json' (required)
  
  ```
  ## Rotas para Categorias 
  
  ### Rota para criação de categorias
  ```
    /api/denunciations/denunciation-categories/
    
    * Methods allowed: ['POST']
    
    POST:
     
    * request data: 
      * name: String (required)
      * gravity: enum('High', 'Medium', 'Low') (required)
      * header: 'Content-type: application/json'
  ```
      
