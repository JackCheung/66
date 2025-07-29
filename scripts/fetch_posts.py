import requests
import json
import os

# 飞书API配置
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
TABLE_ID = os.getenv('TABLE_ID')

def get_feishu_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    payload = {"app_id": APP_ID, "app_secret": APP_SECRET}
    response = requests.post(url, headers=headers, json=payload)
    return response.json().get('tenant_access_token')

def fetch_table_records():
    token = get_feishu_token()
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_ID}/tables/{TABLE_ID}/records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    records = response.json().get('data').get('items')
    
    # 格式化数据
    posts = []
    for item in records:
        fields = item.get('fields')
        posts.append({
            'id': fields.get('id'),
            'title': fields.get('title'),
            'content': fields.get('content'),
            'slug': fields.get('slug'),
            'date': fields.get('create_time'),
            'category': fields.get('category')
        })
    return posts

if __name__ == "__main__":
    posts = fetch_table_records()
    with open('posts.json', 'w') as f:
        json.dump(posts, f, ensure_ascii=False)
