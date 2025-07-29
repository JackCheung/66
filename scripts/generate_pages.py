import json
from jinja2 import Environment, FileSystemLoader
import os

# 加载模板
env = Environment(loader=FileSystemLoader('templates'))
index_template = env.get_template('index.html')
post_template = env.get_template('post.html')

# 创建输出目录
os.makedirs('public/posts', exist_ok=True)

# 读取数据
with open('posts.json') as f:
    posts = json.load(f)

# 生成首页
with open('public/index.html', 'w') as f:
    f.write(index_template.render(posts=posts))

# 生成文章页
for post in posts:
    filepath = f"public/posts/{post['slug']}.html"
    with open(filepath, 'w') as f:
        f.write(post_template.render(post=post))
