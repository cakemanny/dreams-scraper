import scraper
import json
import textwrap


def test_transform():
    test_data = {
        "data": {
            "dreamsPage": {
                "moreExist": True,
                "dreams": [
                    {
                        "id": "625062fcbff459002d4a2279",
                        "title": "🍑 ℍ𝕒𝕣𝕝𝕠𝕥 ℍ𝕒𝕝𝕝 🍑",
                        "income": 50000,
                        "totalContributions": 13600,
                        "minGoal": 438000,
                        "published": True,
                        "approved": True,
                        "canceled": False,
                        "__typename": "Dream"
                    },
                    {
                        "id": "6253221dbff459002d4f33b8",
                        "title": "Glowdome",
                        "income": 1040000,
                        "minGoal": 1460000,
                        "totalContributions": 10400,
                        "published": True,
                        "approved": True,
                        "canceled": False,
                        "__typename": "Dream"
                    },
                    {
                        "id": "625156b9bff459002d4b0801",
                        "title": "Saunacious Dream Spa",
                        "income": 0,
                        "minGoal": 357700,
                        "totalContributions": 18900,
                        "published": True,
                        "approved": True,
                        "canceled": False,
                        "__typename": "Dream"
                    },
                ],
                "__typename": "DreamsPage"
            }
        }
    }

    transformed_data = scraper.transform(test_data)

    assert isinstance(transformed_data, list)
    assert transformed_data[0]['title'] == 'Saunacious Dream Spa'
    assert transformed_data[0]['totalContributions'] == 18900
    assert transformed_data[0]['requiredFunding'] == 57700

    assert transformed_data[1]['title'] == "🍑 ℍ𝕒𝕣𝕝𝕠𝕥 ℍ𝕒𝕝𝕝 🍑"
    assert transformed_data[1]['totalContributions'] == 13600
    assert transformed_data[1]['requiredFunding'] == 88000  # FIXME


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
        | Dream | Total Contributions | Required Funds |
        | ----- | ------------------- | -------------- |
        | [Saunacious Dream Spa](https://kiezburn.dreams.wtf/kiez-burn-2022/625156b9bff459002d4b0801) | 189.0 | 0.0 |
        | [Glowdome](https://kiezburn.dreams.wtf/kiez-burn-2022/6253221dbff459002d4f33b8) | 104.0 | 0.0 |
        """
    )
