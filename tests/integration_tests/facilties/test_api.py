

async def test_add_facilties(ac):
    response = await ac.post(
        '/facilities',
        json = {
            'title': 'Кондиционер',
            }
        )

    print(f'{response.json()}')
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert 'data' in res
    print(res['data'])

async def test_get_facilties(ac):
    response = await ac.get('/facilities')

    print(f'{response.json()}')
    assert response.status_code == 200
    assert isinstance(response.json(), list)





