# Automacao de Build com GitHub Actions

Projeto da pratica de Full Cycle adaptado de GitLab CI/CD para GitHub Actions. O pipeline executa testes, constroi uma imagem Docker, publica duas tags no GitHub Container Registry e reutiliza cache entre builds.

## Aplicacao

A aplicacao usa apenas a biblioteca padrao do Python e disponibiliza:

- `GET /`: informacoes da aplicacao e versao da imagem;
- `GET /health`: verificacao de saude usada pelo Docker.

### Executar no VS Code

Abra a pasta do projeto no VS Code e, no terminal integrado, execute:

```bash
python app.py
```

Acesse `http://localhost:8000`. Para testar:

```bash
python -m unittest discover -s tests -v
```

### Executar com Docker

```bash
docker build -t automacao-build .
docker run --rm -p 8000:8000 automacao-build
```

## Pipeline no GitHub

O arquivo `.github/workflows/build.yml` substitui o `.gitlab-ci.yml` do roteiro. Em cada push para `main`, o GitHub Actions:

1. baixa o codigo;
2. executa os testes;
3. autentica no `ghcr.io` com o `GITHUB_TOKEN`;
4. constroi e publica a imagem com as tags do hash do commit e `latest`;
5. restaura e grava o cache do BuildKit para acelerar os proximos builds.

Nao e necessario cadastrar usuario ou senha do registry: o token temporario e fornecido pelo proprio GitHub Actions. O job recebe somente as permissoes `contents: read` e `packages: write`.

## Imagem publicada

Depois da primeira execucao bem-sucedida, a imagem fica disponivel em:

```text
ghcr.io/rafacrusoe/automacao-build-github-actions:latest
```

Cada build tambem recebe uma tag imutavel com o hash completo do commit.
