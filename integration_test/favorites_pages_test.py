import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pytest
from server import app as flask_app, get_db_connection
from bs4 import BeautifulSoup  

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client

def test_favorites_page(client):
    test_user_id = '2'  

    with client.session_transaction() as session:
        session['user_id'] = test_user_id

    response = client.get('/favorites')

    soup = BeautifulSoup(response.data, 'html.parser')
    favorites_elements = soup.find_all(class_="favorite-image") 

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT DISTINCT COUNT(*) FROM likes WHERE user_id = %s", (test_user_id,))
        count = cursor.fetchone()[0]
    conn.close()

    assert len(favorites_elements) == count
