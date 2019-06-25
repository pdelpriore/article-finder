from bs4 import BeautifulSoup
import os
import re
import shutil

with open("entities.xml", encoding="utf-8") as xml_file:
    xml_content = xml_file.read()

    soup = BeautifulSoup(xml_content, 'lxml-xml')

    object_pages = set(soup.find_all("object", {"class": "Page"}))
    body_contents = soup.find_all("object", {"class": "BodyContent"})

    without_title = 0

for object_page in object_pages:
    title = object_page.find_next("property", {"name": "title"})
    id_article = object_page.find_next("element", {"class": "BodyContent"}).find("id")

    for body_content in body_contents:
        id_body_content = body_content.find_next("id", {"name": "id"})

        if id_article.get_text() == id_body_content.get_text():
            article = id_body_content.find_next("property", {"name": "body"})
            os.chdir("C:\\dev\\python\\confluence\\wiki_articles\\")

            if title.get_text():
                sanitized_title = re.sub("[~#%&*{}:<>?/+|()!$\"]", "", title.get_text())
                with open(f"{sanitized_title}.txt", mode="w", encoding="utf-8") as file_txt:
                    file_txt.write(article.get_text())
            else:
                without_title += 1
                with open(f"Sans titre {without_title}.txt", mode="w", encoding="utf-8") as file_txt:
                    file_txt.write(article.get_text())
            break

shutil.make_archive("C:\\dev\\python\\confluence\\wiki_articles", "zip")

