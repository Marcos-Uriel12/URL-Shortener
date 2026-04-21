def crear_url(client):
    response = client.post("/shorten", json={"original_url": "https://www.example.com"})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["original_url"] == "https://www.example.com/"
    assert "short_code" in data

def test_redireccionar_url(client):
    # Primero, creamos una URL corta
    response = client.post("/shorten", json={"original_url": "https://www.example.com"})
    assert response.status_code == 201
    data = response.json()
    short_code = data["short_code"]

    # Luego, intentamos redireccionar usando la URL corta
    response = client.get(f"/{short_code}", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == "https://www.example.com/"

def test_redireccionar_url_inexistente(client):
    response = client.get("/inexistente", follow_redirects=False)
    assert response.status_code == 404

def test_stats_url(client):
    # Crear una URL corta
    response = client.post("/shorten", json={"original_url": "https://www.example.com"})
    assert response.status_code == 201
    data = response.json()
    short_code = data["short_code"]

    # Obtener estadísticas de la URL corta
    response = client.get(f"/stats/{short_code}")
    assert response.status_code == 200
    data = response.json()
    assert data["original_url"] == "https://www.example.com/"
    assert data["clicks"] == 0

    # Redireccionar para incrementar los clics
    client.get(f"/{short_code}", follow_redirects=False)

    # Verificar que los clics se hayan incrementado
    response = client.get(f"/stats/{short_code}")
    assert response.status_code == 200
    data = response.json()
    assert data["clicks"] == 1