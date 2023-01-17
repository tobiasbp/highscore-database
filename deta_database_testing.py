from deta import Deta

print("Running...")

deta = Deta("a01tzp6n_pHJbLGxWzJ3zP3g58YqNJ37FXZFtaUcv")

users = deta.Base("games")

users.insert({
    "id": 0,
    "name": "Space Invaders"
})

fetch_res = users.fetch({})

print(fetch_res.items)

#for item in fetch_res.items:
#    users.delete(item["key"])
