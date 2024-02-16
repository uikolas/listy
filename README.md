# Listy 📃
Small python flask app. To save and add groceries

## Install
* `cp .env.example .env`
  * Update `JWT_SECRET_KEY` inside `.env`
* `pip install -r requirements.txt`

## Endpoints
`POST /login`
```json
{
  "username": "",
  "password": ""
}
```
---
`GET /lists`

`POST /lists`
```json
{
  "name": "Test list"
}
```

---
`GET /lists/<id>/items`

`POST /lists/<id>/items`
```json
{
  "name": "banana", 
  "icon": "🍌"
}
```
---
`GET /search?name=value`