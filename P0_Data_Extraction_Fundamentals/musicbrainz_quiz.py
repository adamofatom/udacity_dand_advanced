import json
import requests

BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"


# query parameters are given to the requests.get function as a dictionary; this
# variable contains some starter parameters.
query_type = {"simple": {},
              "atr": {"inc": "aliases+tags+ratings"},
              "aliases": {"inc": "aliases"},
              "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    """
    This is the main function for making queries to the musicbrainz API. The
    query should return a json document.
    """
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print("requesting", r.url)

    if r.status_code == 200:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    """
    This adds an artist name to the query parameters before making an API call
    to the function above.
    """
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    """
    After we get our output, we can use this function to format it to be more
    readable.
    """
    if isinstance(data, dict):
        print(json.dumps(data, indent=indent, sort_keys=True))
    else:
        print(data)


def main():
    """
    Below is an example investigation to help you get started in your
    exploration. Modify the function calls and indexing below to answer the
    questions on the next quiz.

    HINT: Note how the output we get from the site is a multi-level JSON
    document, so try making print statements to step through the structure one
    level at a time or copy the output to a separate output file. Experimenting
    and iteration will be key to understand the structure of the data!
    """

    # # Query for information in the database about bands named Nirvana
    # results = query_by_name(ARTIST_URL, query_type["simple"], "First Aid Kit")
    # pretty_print(results)

    # # Isolate information from the 4th band returned (index 3)
    # print("\nARTIST:")
    # pretty_print(results["artists"][3])

    # # Query for releases from that band using the artist_id
    # artist_id = results["artists"][3]["id"]
    # artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    # releases = artist_data["releases"]

    # # Print information about releases from the selected band
    # print("\nONE RELEASE:")
    # pretty_print(releases[0], indent=2)

    # release_titles = [r["title"] for r in releases]
    # print("\nALL TITLES:")
    # for t in release_titles:
    #     print(t)

    name_query = query_by_name(ARTIST_URL, query_type["simple"], "First Aid Kit")
    name_results = [artist["name"] for artist in name_query["artists"] if artist["name"] == "First Aid Kit"]    
    print("First Aid Kit occurrences: ", len(name_results)) 

    # area_query = query_by_name(ARTIST_URL, query_type["simple"], "Queen")
    # queen_begin_area = area_query["artists"][0]["begin_area"]["name"]
    # print("Queen begin area is: ", queen_begin_area)
     
    # beatles_query = query_by_name(ARTIST_URL, query_type["simple"], "Beatles")
    # aliases = [alias["name"] for alias in beatles_query["artists"][0]["aliases"] if alias["locale"] == "es"]
    # print("Beatles Spanish alias is: ", aliases)

    nirvana_query = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    disambiguation = nirvana_query["artists"][0]["disambiguation"]
    print("Nirva disambigution: ", disambiguation)

    one_direction_query = query_by_name(ARTIST_URL, query_type["simple"], "One Direction")
    form_date = one_direction_query["artists"][0]["life-span"]["begin"]
    print("One Direction was formed in: ", form_date)


if __name__ == '__main__':
    main()
