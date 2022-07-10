if __name__ == "__main__":
    from .nuct import NUCT
    nuct = NUCT()
    print(nuct.content("2021_1000070"))
    for d in nuct.content_data["2021_1000070"]:
        print(d["title"], d["url"])
