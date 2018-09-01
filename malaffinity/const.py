"""malaffinity constants."""


class ENDPOINT_URLS:  # noqa: D101
    ANILIST = "https://graphql.anilist.co"
    MYANIMELIST = "https://myanimelist.net/malappinfo.php"


class ALIASES:  # noqa: D101
    ANILIST = ["ANILIST", "AL", "A"]
    MYANIMELIST = ["MYANIMELIST", "MAL", "M"]


GRAPHQL_QUERY = """
query ($userName: String) {
    MediaListCollection (userName: $userName, type: ANIME) {
        lists {
            name
            entries {
                # id  # Useless to us
                score (format: POINT_10_DECIMAL)  # POINT_10 ?
                media {
                    idMal
                }
            }
        }
    }
}
"""
