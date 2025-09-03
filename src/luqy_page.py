import json
import pandas as pd
from mako.template import Template

def gen_index_page(data_dir, doc_dir, template_dir, index_dir):
    article_file = f"{data_dir}/lqy_articles_241206.pkl"
    df_article = pd.read_pickle(article_file)
    df_article["type"] = "[文章] "
    lecture_file = f"{data_dir}/lqy_lectures_241206.pkl"
    df_lecture = pd.read_pickle(lecture_file)
    df_lecture["type"] = "[讲座] "
    latest_file = f"{doc_dir}/latest_lecture.pkl"
    df_latest = pd.read_pickle(latest_file)
    df_latest["type"] = "[讲座] "

    df = pd.concat([df_article, df_lecture, df_latest], ignore_index=True)
    df = df.sort_values("publish_date").reset_index(drop=True)
    art_li = []
    post_li = []

    for idx in df.index:
        columns = ["type", "title", "publish_date", "content"]
        tp, title, publish_date, content = df.loc[idx, columns]
        art_id = publish_date.replace("-", "")
        art_li.append((art_id, tp+title, publish_date))
        post_li = [(title, publish_date, content)]

        article_template_file = f"{template_dir}/luqy_page.html"
        html = Template(filename=article_template_file).render(art_li=post_li)
        with open(f"{html_dir}/{art_id}.html", "w", encoding="utf8") as f:
            f.write(html)
        print(f"{html_dir}/{art_id}.html saved!")
    
    index_template_file = f"{template_dir}/luqy_index.html"
    INDEX = Template(filename=index_template_file)
    html = INDEX.render(art_li=art_li)
    with open(f"{index_dir}/index.html", "w") as f:
        f.write(html)
    print(f"{index_dir}/index.html saved!")


def gen_search_data(data_dir, doc_dir, search_dir):
    article_file = f"{data_dir}/lqy_articles_241206.pkl"
    df_article = pd.read_pickle(article_file)
    lecture_file = f"{data_dir}/lqy_lectures_241206.pkl"
    df_lecture = pd.read_pickle(lecture_file)
    latest_file = f"{doc_dir}/latest_lecture.pkl"
    df_latest = pd.read_pickle(latest_file)

    df = pd.concat([df_article, df_lecture, df_latest], ignore_index=True)
    df = df.sort_values("publish_date").reset_index(drop=True)

    article_list = []
    for idx in df.index:
        columns = ["title", "publish_date", "content"]
        title, publish_date, post = df.loc[idx, columns]
        id = publish_date.replace("-", "")
        article_list.append({"id": id, "title": title, "date": publish_date,
                             "post":post})
    
    article_dict = {"article": article_list}
    with open(f"{search_dir}/article.json", "w") as f:
        f.write(json.dumps(article_dict, indent=4, ensure_ascii=False))
    
if __name__ == "__main__":
    index_dir       = ".."
    data_dir        = "/mnt/e/gitLFS/luqiyuan/data"
    template_dir    = "./templates"
    html_dir        = "../html"
    search_dir      = "../search"
    doc_dir         = "../doc"

    gen_index_page(data_dir, doc_dir, template_dir, index_dir)
    gen_search_data(data_dir, doc_dir, search_dir)