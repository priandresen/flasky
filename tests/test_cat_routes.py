def test_get_all_cats_with_no_records(client):
    # Act
    response = client.get("/cats")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_cat_succeeds(client, one_cat):
    # Act
    response = client.get(f"/cats/{one_cat.id}")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": one_cat.id,
        "name": "Morty",
        "color": "orange",
        "personality": "rechargeable"
    }

def test_create_one_cat(client):
    # Arrange
        request_body = {
            "name": "Ash",
            "color": "Black",
            "personality": "Curious"
        }

    # Act
        response = client.post("/cats", json=request_body)
        response_body = response.get_json()

        # Assert
        assert response.status_code == 201
        assert response_body == {
            "id": 1,
            "name": "Ash",
            "color": "Black",
            "personality": "Curious"
        }
