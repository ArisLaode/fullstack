# FULLSTACK TEST


## Get started

### How to run api
```
$ cd graphql_api
$ virtualenv venv --python=python3
$ source venv/bin/activate
$ (venv) python manage.py seed
$ (venv) python manage.py runserver 8200
```

Go to `http://localhost:8200/graphql` to play around with the example api. Try execute this query
```
query {
  transactions {
    pk
    category
    amount
    createdAt
  }
}
```


### How to run frontend

Open new terminal
```
$ cd frontend
$ npm install
$ npm run app
```
