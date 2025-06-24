import pprint

from googleapiclient.discovery import build


def main():
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    service = build(
        "customsearch", "v1", developerKey="api_key"
    )

    res = (
        service.cse()
        .list(
            q="台灣總統是誰",
            cx="search_key",
            num = 3  
        )
        .execute()
    )
    pprint.pprint(res)


if __name__ == "__main__":
    main()