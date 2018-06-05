# Reunião 04/06/2018

Participantes: Ícaro Pires, Vinicius Bernardo, Daniel

## Decisões

* Será uma API RESTful seguindo o Richardson Maturity Model
* O usuário tem que conseguir cadastrar uma denúncia
* A denúncia tem que conter uma descrição
* O usuário tem que conseguir avaliar uma denúncia
* Tem que existir uma fila de denúncias a serem avaliadas
* A fila de denúncias a serem avaliadas tem que considerar a gravidade
* A fila de denúncias a serem avaliadas deve considerar credibilidade do denunciante
* A fila de denúncias a serem avaliadas deve considerar ordem de chegada
* O administrador deve poder bloquear um usuário (por email)
* Denunciante e administrador devem ser notificados na mudança do estado da denúncia
* Ações devem ser limitadas dependendo do estado da denúncia
* O usuário deve poder se autenticar
* Cada conjunto de denúncias deve ser associado a um domínio e uma página
* a API deverá ter mecanismos de defesa (exemplo: throttling)

## Referências utilizadas para tomada das decisões
https://www.martinfowler.com/articles/richardsonMaturityModel.html
https://restfulapi.net/richardson-maturity-model/
