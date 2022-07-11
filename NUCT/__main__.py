if __name__ == "__main__":
    from .content import Content
    content = Content()
    url_list = content.load_contents_url("2022_1002160")
    print(url_list)
    url_list.append("https://example.com")
    content.load_contents(url_list)
