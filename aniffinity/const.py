"""aniffinity constants."""


DEFAULT_SERVICE = "ANILIST"


class ENDPOINT_URLS:  # noqa: D101
    ANILIST = "https://graphql.anilist.co"
    KITSU = "https://kitsu.io/api/edge/library-entries"
    MYANIMELIST = "https://myanimelist.net/animelist/{username}/load.json"


GRAPHQL_QUERY = """
query ($userName: String) {
    MediaListCollection (userName: $userName, status_not: PLANNING,
                         type: ANIME, forceSingleCompletedList: true) {
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
