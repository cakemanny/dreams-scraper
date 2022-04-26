#
# This is a very shitty script for scraping some festival dream voting data
#
import requests
import sys

QUERY = """\
query Dreams($eventSlug: String!, $textSearchTerm: String, $tag: String, $offset: Int, $limit: Int) {
dreamsPage(eventSlug: $eventSlug, textSearchTerm: $textSearchTerm, tag: $tag, offset: $offset, limit: $limit) {
    moreExist
    dreams(eventSlug: $eventSlug, textSearchTerm: $textSearchTerm, tag: $tag, offset: $offset, limit: $limit) {
    id
    title
    income
    totalContributions
    published
    approved
    canceled
    __typename
    }
    __typename
}
}
"""


def get_data():
    """
    Returns some data about dreams
    """
    headers = {
        "authority": "api.dreams.wtf",
        "accept": "*/*",
        "accept-language": "en-GB,en;q=0.9",
        "authorization": "",
        "content-type": "application/json",
        "dreams-subdomain": "kiezburn",
        "origin": "https://kiezburn.dreams.wtf",
        "referer": "https://kiezburn.dreams.wtf/",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
    }

    session = requests.Session()

    # Assumption: there are not more than 100 dreams
    payload = {
        'operationName': 'Dreams', 'variables': {
            'eventSlug': 'kiez-burn-2022', 'offset': 0, 'limit': 100
        },
        'query': QUERY
    }
    r = session.post(
        'https://api.dreams.wtf/graphql', headers=headers, json=payload
    )
    data = r.json()
    if data.get('data', {}).get('dreamsPage', {}).get('moreExist'):
        print('😬', file=sys.stderr)
    return data


def transform(data):
    """
    Transform takes the GraphQL response and plays with the numbers
    """
    dreams = data['data']['dreamsPage']['dreams']
    return sorted(
        dreams, key=lambda dream: dream['totalContributions'], reverse=True
    )


def render(data):
    """
    Render takes the GraphQL response and renders a static page
    """

    def dream_line(dream):
        _id = dream['id']
        url = f'https://kiezburn.dreams.wtf/kiez-burn-2022/{_id}'
        title = dream.get('title', '')
        contributions = dream.get('totalContributions', 0)
        return f'[{title}]({url}): {contributions}\n'

    import io
    buffer = io.StringIO()
    for dream in data:
        buffer.write(dream_line(dream))
    return buffer.getvalue()


if __name__ == '__main__':
    with open('README.md', 'w') as f:
        f.write(render(transform(get_data())))
