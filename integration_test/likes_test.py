import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pytest
from server import app as flask_app, get_db_connection

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client

def test_add_to_favorites(client):
    test_user_id = '1'  
    test_cocktail_id = '14229' 

    with client.session_transaction() as session:
        session['user_id'] = test_user_id

    client.post('/like', data={'recipe_id': test_cocktail_id})

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM likes WHERE user_id = %s AND idDrink = %s", (test_user_id, test_cocktail_id))
        result = cursor.fetchone()
        assert result is not None
        cursor.execute("DELETE FROM likes WHERE user_id = %s AND idDrink = %s", (test_user_id, test_cocktail_id))


    conn.commit()
    conn.close()