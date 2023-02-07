from deta import Deta

deta = Deta("a01tzp6n_pHJbLGxWzJ3zP3g58YqNJ37FXZFtaUcv")

users = deta.Base("scores")

users.insert({
    "id": 0,
    "scores": [
        {"score": 0, "user": "Test"}
    ],
})

fetch_res = users.fetch({})

print(fetch_res.items)

#for item in fetch_res.items:
#    users.delete(item["key"])
