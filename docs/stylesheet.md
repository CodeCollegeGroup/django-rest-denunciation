## Histórico de Revisão

| Data | Responsável | Versão | Mudança realizada |
|:----:| ----------- |:------:| ----------------- |
| **22/05/18** | Ícaro Pires | 0.1  | Adicionando documento com estrutura inicial|

# Folha de estilo

## Backend

Para realizar a análise estática do código e de folha de estilo, estão sendo utilizadas as ferramentas Flake8 e Pylint. O pylint usado para checagem de algumas boas práticas, como: formato dos nomes de classes, métodos, ordem dos imports, dentre outros. Mas como as checkagens de folha de estilo do pylint não são tão rigorosas com relação a regra pep8 utilizada em projetos em python, optamos também por utilizar a ferramenta flake8, que realmente segue a pep8 utilizando a ferramenta pycodestyle e também pode realizar mais algumas checagens. As configurações do Flake8 no projeto estão default e as configurações do pylint foram alteradas para se adaptarem a dinâmica do projeto e foram retiradas para evitar colisões de regras com o flake8.

### Configurações Pylint

Algumas das configurações do pylint foram alteradas para se adaptarem a dinâmica do projeto e outras foram retiradas para evitar colisões de regras com o flake8, as alterações com relação as regras padrões do pylint podem ser conferidas no arquivo de configuração .pylintrc, na pasta do projeto.<br>
Por último, algumas configurações tiveram que ser alteradas para se adaptar ao framework, como por exemplo o uso do módulo pylint-django e a retirada do limite máximo na hierarquia de heranças, regra que já viria quebrada apenas pelo uso do framework.

### Regras do projeto
O django também possui algumas regras de estilo que também estão sendo seguidas neste projeto e podem ser conferidas na documentação do django. Mas, além destas regras, algumas definidas pela equipe estão especificadas abaixo:

#### Models
* Colocar os atributos de relacionamento antes de todos outros fields
* Colocar classe com o qual está estabelecendo relacionamento como string
* Se tiver mais que um atributo por field, por um em cada linha e não por atributos na mesma linha que o nome da classe.
* Pular uma linha no início da classe
* Pular uma linha entre atributos


##### Exemplo de model:
```python
class Model(models.Model):

    A = 'A'
    B = 'B'

    LETTERS = (
        (A, 'A'),
        (B, 'B'),
    )

    campo_relacionamento = models.ForeignKey(
        'algum_app.alguma_model',
         on_delete=models.CASCADE
    )
    
    campo_normal = models.CharField(max_length=10)

    campo_choices = models.CharField(
        max_length=1,
        choices=LETTERS,
        default=A
    )

    Class Meta:
        abstract=True
```

## Referências Bibliográficas

[Documentação do Pylint](https://pylint.readthedocs.io/en/latest/)<br/>
[Documentação do Flake8](http://flake8.pycqa.org/en/latest/)<br/>
[Documentação do Django](https://docs.djangoproject.com/en/2.0/internals/contributing/writing-code/coding-style/)
