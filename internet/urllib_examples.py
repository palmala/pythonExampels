import urllib.parse

if __name__ == "__main__":
    # parsing url
    sample_url = "http://somedomain.whatever.com:8080/something.html?asd=123"
    print(sample_url)
    result = urllib.parse.urlparse(sample_url)
    print(result)

    # converting query
    query_data = {
        "Name" : "Me",
        "Date" : "Secret",
        "Place" : "Right here"
    }
    print(urllib.parse.urlencode(query_data))

