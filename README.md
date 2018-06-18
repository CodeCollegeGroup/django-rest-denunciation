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
  * header: 'Contend-type: application/json'

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
    * header: 'Contend-type: application/json'
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
    * header: 'Contend-type: application/json'
  ```
