# 📘 UCr - Desenvolvimento de Sistemas

Este repositório corresponde ao projeto final da disciplina **UCr - Desenvolvimento de Sistemas**, integrante do curso **Técnico em Desenvolvimento de Sistemas** na modalidade **semipresencial**, ofertado pelo **SENAI Lauro de Freitas**.

## 🎓 Docentes Responsáveis

A disciplina é conduzida pelos seguintes professores:

- 👨‍🏫 **Marcos Antônio Gomes de Souza Silva** — Aulas presenciais.
- 💻 **Dennis Jean Borges Rosado da Rocha** — Aulas online.

## 🎯 Objetivo do Repositório

Este repositório irá armazenar o andamento do projeto final da matéria, com Backlogs e construções sendo ajustadas à medida em que forem sendo disponibilizadas pelos docentes.

## 📂 Organização do Repositório

```text
projeto_final/
├── colabepi/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── colaboradores/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   └── colaboradores/
│       ├── colaborador_confirm_delete.html
│       ├── colaborador_form.html
│       └── colaborador_list.html
├── .gitignore
├── .python-version
├── README.md
├── db.sqlite3
├── main.py
├── manage.py
├── pyproject.toml
└── uv.lock
```

## 📌 Entregáveis

- Situação de Aprendizagem 6:
  - Implementação das operações CRUD (Criar, Ler, Atualizar e Excluir).
  - Garantia de dados salvos e persistidos no banco de dados.
  - Disponibilização de um arquivo `Dockerfile`.

## 🚀 Execução do sistema

1. Instale a ferramenta [`uv`](https://github.com/astral-sh/uv).
2. Inicie um novo projeto com o comando `uv init`.
3. Crie o ambiente virtual com `uv venv`.
4. Acesse o ambiente virtual, se necessário, `source .venv/bin/activate`.
5. Instale as dependências com `uv add "Django>=6.0.5"`.
6. Execute as migrações com `python manage.py migrate`.
7. Inicie o servidor com `python manage.py runserver`.
8. Crie o usuário administrativo manualmente com `python manage.py createsuperuser`.
9. Acesso para Django Admin em `http://127.0.0.1:8000/admin/`.

> [!NOTE]
> Este projeto conta com um pequeno banco de dados de exemplo, com acesso através de credenciais User e Senha `ciromota`.
> Para uso com banco de dados externo, descomente e edite as credenciais no arquivo `colabepi/settings.py`.

## 🐋 Docker

Construa a imagem com o comando:

```bash
docker buildx build -t projeto_final .
```

Execute:

```bash
docker container run -d -p 8000:8000 projeto_final
```

## 📋 Backlog

- [x] Situação de Aprendizagem 6
- [x] Situação de Aprendizagem 7 (branch sa7)
- [x] Situação de Aprendizagem 8 (branch sa8)
- [x] Situação de Aprendizagem 9 (branch sa9)