import scraper
import json
import textwrap


def test_transform():

    with open('tests/example-response.json') as f:
        test_data = json.load(f)

    assert 'data' in test_data

    transformed_data = scraper.transform(test_data)

    assert isinstance(transformed_data, list)
    assert transformed_data[0]['title'] == 'Saunacious Dream Spa'
    assert transformed_data[0]['totalContributions'] == 18900


def test_render():

    data = [
        {
            "id": "625156b9bff459002d4b0801",
            "title": "Saunacious Dream Spa",
            "income": 0,
            "totalContributions": 18900,
            "published": True,
            "approved": True,
            "canceled": False,
            "__typename": "Dream"
        },
        {
            "id": "6253221dbff459002d4f33b8",
            "title": "Glowdome",
            "income": 1040000,
            "totalContributions": 10400,
            "published": True,
            "approved": True,
            "canceled": False,
            "__typename": "Dream"
        }
    ]

    rendered = scraper.render(data)

    assert rendered == textwrap.dedent(
        """\
        [Saunacious Dream Spa](https://kiezburn.dreams.wtf/kiez-burn-2022/625156b9bff459002d4b0801): 18900

        [Glowdome](https://kiezburn.dreams.wtf/kiez-burn-2022/6253221dbff459002d4f33b8): 10400

        """
    )
