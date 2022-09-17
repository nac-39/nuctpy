import nuctpy

content = nuctpy.Content()

SITE_ID = "<site_id>"
resources_list = content.site(SITE_ID)

print(resources_list)

for resource in resources_list:
    print("title: ", resource["title"])
    print("download url: ", resource["url"])
    content.load_contents(resource["url"])

# 謎にリソースの一括ダウンロードのための
# ショートハンドが存在します。
url_list = content.collect_url(SITE_ID)

for url in url_list:
    content.load_contents(url, save_path="~/Desktop/testete")
