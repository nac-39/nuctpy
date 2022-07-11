if __name__ == "__main__":
    from .content import Content
    content = Content()
    print(content.site("2022_1002140"))
    print(content.load_contents_url("2022_1002140"))
