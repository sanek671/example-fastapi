import pytest
from typing import List
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, response.json())
    posts_list = list(posts_map)
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get("/posts/333")
    assert response.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**response.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize("title, content, published", [
    ("new title", "new content", True),
    ("favorite florida", "panters", False),
    ("i love is footbal", "top barcelona", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    create_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert create_post.title == title
    assert create_post.content == content
    assert create_post.published == published
    assert create_post.owner_id == test_user["id"]


def test_create_post_defoult_published_true(authorized_client, test_user, test_posts):
    response = authorized_client.post("/posts/", json={"title": "title", "content": "content"})
    create_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert create_post.title == "title"
    assert create_post.content == "content"
    assert create_post.published == True
    assert create_post.owner_id == test_user["id"]


def test_unauthorized_user_create_posts(client, test_posts, test_user):
    response = client.post("/posts/", json={"title": "title", "content": "content"})
    assert response.status_code == 401


def test_unauthorized_user_delete_posts(client, test_posts, test_user):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_delete_post_succes(authorized_client, test_posts, test_user):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204


def test_delete_post_no_exist(authorized_client, test_posts, test_user):
    response = authorized_client.delete("/posts/999")
    assert response.status_code == 404


def test_delete_post_other_user(authorized_client, test_posts, test_user):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "update title",
        "content": "update content",
        "id": test_posts[0].id
    }
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "update title",
        "content": "update content",
        "id": test_posts[3].id
    }
    response = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert response.status_code == 403
    

def test_unauthorized_user_update_post(client, test_posts, test_user):
    response = client.put(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_update_post_no_exist(authorized_client, test_posts, test_user):
    data = {
        "title": "update title",
        "content": "update content",
        "id": test_posts[3].id
    }
    response = authorized_client.put("/posts/999", json=data)
    assert response.status_code == 404