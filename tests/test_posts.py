import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostVote(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    # Not ordered so this won't work in current form but could play with
    #assert posts_list[0].Post.id == test_posts[0].id

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{8888}")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostVote(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert res.status_code == 200

@pytest.mark.parametrize("title, content, published", [ 
    ("new title", "new content", True),
    ("favorite pizza", "margherita", False),
    ("Yellowest fruit", "Lots of citrus", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title" : title, "content" : content, "published" : published})
    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_creat_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title" : "title", "content" : "content"})

    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title" : "title", "content" : "content"})

    assert res.status_code == 401

def test_unauthorized_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_authorized_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/69")

    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    updated_post = {
        "title" : "Updated title",
        "content" : "Updated content"
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json = updated_post)

    up_post = schemas.PostResponse(**res.json())

    assert res.status_code == 200
    assert up_post.title == updated_post["title"]
    assert up_post.content == updated_post["content"]

def test_update_other_users_post(authorized_client, test_user, test_user_second, test_posts):

    updated_post = {
        "title" : "Updated title",
        "content" : "Updated content",
        "id" : test_posts[3].id
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json = updated_post)

    assert res.status_code == 403

def test_unauthorized_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_user, test_posts):
    updated_post = {
        "title" : "Updated title",
        "content" : "Updated content",
        "id" : test_posts[3].id
    }

    res = authorized_client.put(f"/posts/69", json = updated_post)

    assert res.status_code == 404

