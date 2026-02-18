import requests
from bs4 import BeautifulSoup
import time
import re
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 商品データの更新
def save_json(filepath, data):
    full_path = os.path.join(BASE_DIR, filepath)
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[Success] {len(data)} products data added in {filepath}")
    except Exception as e:
        print(f"[Error] Error has occurred in {filepath} : {e}")

# FamilyMart
def fetch_family():
    print("\n--- FamilyMart ---")
    TARGET_CATEGORIES = [
        {"name": "おむすび", "url": "https://www.family.co.jp/goods/omusubi.html"},
        {"name": "お弁当", "url": "https://www.family.co.jp/goods/obento.html"},
        {"name": "お寿司", "url": "https://www.family.co.jp/goods/sushi.html"},
        {"name": "サンドイッチ・ロールパン・バーガー", "url": "https://www.family.co.jp/goods/sandwich.html"},
        {"name": "パン", "url": "https://www.family.co.jp/goods/bread.html"},
        {"name": "そば・うどん・中華めん", "url": "https://www.family.co.jp/goods/noodle.html"},
        {"name": "パスタ", "url": "https://www.family.co.jp/goods/pasta.html"},
        {"name": "サラダ", "url": "https://www.family.co.jp/goods/salad.html"},
        {"name": "チルド惣菜", "url": "https://www.family.co.jp/goods/sidedishes.html"},
        {"name": "スープ・グラタン・お好み焼き", "url": "https://www.family.co.jp/goods/deli.html"},
        {"name": "日配品 加工肉 たまご カット野菜 漬物など", "url": "https://www.family.co.jp/goods/chilleddaily.html"},
        {"name": "ホットスナック・惣菜", "url": "https://www.family.co.jp/goods/friedfoods.html"},
        {"name": "中華まん", "url": "https://www.family.co.jp/goods/chukaman.html"},
        {"name": "おでん", "url": "https://www.family.co.jp/goods/oden.html"},
        {"name": "デザート", "url": "https://www.family.co.jp/goods/dessert.html"},
        {"name": "焼き菓子・和菓子", "url": "https://www.family.co.jp/goods/baked_sweets.html"},
        {"name": "コーヒー・フラッペ", "url": "https://www.family.co.jp/goods/cafe.html"},
        {"name": "加工食品", "url": "https://www.family.co.jp/goods/processed_foods.html"},
        {"name": "お菓子", "url": "https://www.family.co.jp/goods/snack.html"},
        {"name": "飲料", "url": "https://www.family.co.jp/goods/drink.html"},
        {"name": "お酒", "url": "https://www.family.co.jp/goods/alcohol.html"},
        {"name": "冷凍食品", "url": "https://www.family.co.jp/goods/frozen_foods.html"},
        {"name": "アイス", "url": "https://www.family.co.jp/goods/ice.html"},
    ]
    
    all_products = []

    for category in TARGET_CATEGORIES:
        if not category["url"]: continue
        print(f"Retrieving data for {category['name']} category...")
        try:
            response = requests.get(category["url"], headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.find_all("li", class_="ly-mod-layout-clm")
            for item in items:
                try:
                    # 商品名
                    name_tag = item.select_one(".ly-mod-infoset3-name")
                    if not name_tag: continue
                    name = name_tag.text.strip()
                    # 発売地域
                    desc_tag = item.select_one(".ly-mod-infoset3-notes")
                    desc = desc_tag.text.strip() if desc_tag else ""
                    # 商品ページ
                    url_tag = item.select_one(".ly-mod-infoset3-link")
                    item_url = url_tag.get('href') if url_tag else ""
                    # 商品画像
                    img_tag = item.select_one(".ly-hovr")
                    img_url = ""
                    if img_tag:
                        src = img_tag.get('src')
                        if src:
                            img_url = "https://www.family.co.jp" + src
                    # 価格
                    price_tag = item.select_one(".ly-mod-infoset3-price")
                    if not price_tag: continue
                    price_text = price_tag.text.strip()
                    match = re.search(r'税込([\d\.,]+)円', price_text)
                    if match:
                        price = int(match.group(1).replace(',', ''))
                    else:
                        continue

                    product_data = {
                        "name": name,
                        "category": category['name'],
                        "price": price,
                        "area": desc,
                        "image": img_url,
                        "url": item_url,
                        "store": "FamilyMart"
                    }
                    all_products.append(product_data)

                except Exception as e:
                    continue
            
            time.sleep(1)

        except Exception as e:
            print(f"[Error] Error has occurred in {category['name']} category : {e}")

    return all_products

# Seven-Eleven
def fetch_seven():
    print("\n--- Seven-Eleven ---")
    # 頂いたリストを使用
    TARGET_CATEGORIES = [
        {"name": "おにぎり/手巻きおにぎり", "url": "https://www.sej.co.jp/products/a/cat/010010010000000/kanto/1/l100/"},
        {"name": "おにぎり/直巻おむすび", "url": "https://www.sej.co.jp/products/a/cat/010010020000000/kanto/1/l100/"},
        {"name": "おにぎり/その他のおむすび", "url": "https://www.sej.co.jp/products/a/cat/010010030000000/kanto/1/l100/"},
        {"name": "お寿司/手巻寿司", "url": "https://www.sej.co.jp/products/a/cat/010030010000000/kanto/1/l100/"},
        {"name": "お寿司/いなり寿司", "url": "https://www.sej.co.jp/products/a/cat/010030020000000/kanto/1/l100/"},
        {"name": "お寿司/その他のお寿司", "url": "https://www.sej.co.jp/products/a/cat/010030030000000/kanto/1/l100/"},
        {"name": "お弁当/お弁当", "url": "https://www.sej.co.jp/products/a/cat/010020010000000/kanto/1/l100/"},
        {"name": "お弁当/チルド弁当", "url": "https://www.sej.co.jp/products/a/cat/010020020000000/kanto/1/l100/"},
        {"name": "サンドイッチ・ロールパン", "url": "https://www.sej.co.jp/products/a/sandwich/kanto/1/l100/"},
        {"name": "パン/食パン", "url": "https://www.sej.co.jp/products/a/cat/050010010000000/kanto/1/l100/"},
        {"name": "パン/食事パン", "url": "https://www.sej.co.jp/products/a/cat/050010020000000/kanto/1/l100/"},
        {"name": "パン/菓子パン", "url": "https://www.sej.co.jp/products/a/cat/050020010000000/kanto/1/l100/"},
        {"name": "パン/惣菜パン", "url": "https://www.sej.co.jp/products/a/cat/050020020000000/kanto/1/l100/"},
        {"name": "ドーナツ", "url": "https://www.sej.co.jp/products/a/donut/kanto/1/l100/"},
        {"name": "そば・うどん・中華麺/そば", "url": "https://www.sej.co.jp/products/a/cat/030010010000000/kanto/1/l100/"},
        {"name": "そば・うどん・中華麺/うどん", "url": "https://www.sej.co.jp/products/a/cat/030010020000000/kanto/1/l100/"},
        {"name": "そば・うどん・中華麺/中華麺", "url": "https://www.sej.co.jp/products/a/cat/030010030000000/kanto/1/l100/"},
        {"name": "そば・うどん・中華麺/焼きそば・焼うどんほか", "url": "https://www.sej.co.jp/products/a/cat/030010040000000/kanto/1/l100/"},
        {"name": "スパゲティ・パスタ", "url": "https://www.sej.co.jp/products/a/pasta/kanto/1/l100/"},
        {"name": "グラタン・ドリア", "url": "https://www.sej.co.jp/products/a/gratin/kanto/1/l100/"},
        {"name": "惣菜", "url": "https://www.sej.co.jp/products/a/dailydish/kanto/1/l100/"},
        {"name": "惣菜", "url": "https://www.sej.co.jp/products/a/dailydish/kanto/2/l100/"},
        {"name": "サラダ/サラダ", "url": "https://www.sej.co.jp/products/a/cat/040020010000000/kanto/1/l100/"},
        {"name": "サラダ/パスタサラダ・おかずサラダほか", "url": "https://www.sej.co.jp/products/a/cat/040020020000000/kanto/1/l100/"},
        {"name": "サラダ/７プレミアム（副菜）", "url": "https://www.sej.co.jp/products/a/cat/040020030000000/kanto/1/l100/"},
        {"name": "サラダ/カット野菜・カットフルーツ", "url": "https://www.sej.co.jp/products/a/cat/080080030000000/kanto/1/l100/"},
        {"name": "スイーツ/洋菓子", "url": "https://www.sej.co.jp/products/a/cat/060010010000000/kanto/1/l100/"},
        {"name": "スイーツ/和菓子", "url": "https://www.sej.co.jp/products/a/cat/060010020000000/kanto/1/l100/"},
        {"name": "アイス/アイスクリーム", "url": "https://www.sej.co.jp/products/a/cat/060020010000000/kanto/1/l100/"},
        {"name": "アイス/ファミリータイプ", "url": "https://www.sej.co.jp/products/a/cat/060020020000000/kanto/1/l100/"},
        {"name": "揚げ物・フランク・焼き鳥/揚げ物惣菜", "url": "https://www.sej.co.jp/products/a/cat/090030010000000/kanto/1/l100/"},
        {"name": "揚げ物・フランク・焼き鳥/その他の商品", "url": "https://www.sej.co.jp/products/a/cat/090030020000000/kanto/1/l100/"},
        {"name": "おでん", "url": "https://www.sej.co.jp/products/a/oden/kanto/1/l100/"},
        {"name": "中華まん", "url": "https://www.sej.co.jp/products/a/chukaman/kanto/1/l100/"},
        {"name": "冷凍食品/冷凍食品", "url": "https://www.sej.co.jp/products/a/cat/150010000000000/1/l100/"},
        {"name": "冷凍食品/冷凍食品", "url": "https://www.sej.co.jp/products/a/cat/150010000000000/2/l100/"},
        {"name": "冷凍食品/冷凍食材", "url": "https://www.sej.co.jp/products/a/cat/150020000000000/1/l100/"},
        {"name": "冷凍食品/ロックアイス", "url": "https://www.sej.co.jp/products/a/cat/150030000000000/1/l100/"},
        {"name": "セブンカフェ", "url": "https://www.sej.co.jp/products/a/sevencafe/kanto/1/l100/"},
        {"name": "セブンプレミアム/チルド惣菜/７プレミアム（主菜）", "url": "https://www.sej.co.jp/products/a/7premium/cat/040010020000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/チルド惣菜/７プレミアム（副菜）", "url": "https://www.sej.co.jp/products/a/7premium/cat/040010030000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/チルド惣菜/７プレミアム（サラダ）", "url": "https://www.sej.co.jp/products/a/7premium/salad/kanto/1/l100/"},
        {"name": "セブンプレミアム/チルド惣菜/７プレミアム（その他）", "url": "https://www.sej.co.jp/products/a/7premium/cat/040010040000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/生鮮", "url": "https://www.sej.co.jp/products/a/7premium/fresh/kanto/1/l100/"},
        {"name": "セブンプレミアム/生鮮", "url": "https://www.sej.co.jp/products/a/7premium/fresh/kanto/2/l100/"},
        {"name": "セブンプレミアム/常温・加工食品/インスタント食品", "url": "https://www.sej.co.jp/products/a/7premium/cat/140020000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/常温・加工食品/レトルト食品・パスタ・パスタソース", "url": "https://www.sej.co.jp/products/a/7premium/cat/140030000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/常温・加工食品/米・米加工品", "url": "https://www.sej.co.jp/products/a/7premium/cat/140050000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/常温・加工食品/乾麺・乾物", "url": "https://www.sej.co.jp/products/a/7premium/cat/140040000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/常温・加工食品/珍味・缶詰", "url": "https://www.sej.co.jp/products/a/7premium/cat/140080000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/常温・加工食品/調味料", "url": "https://www.sej.co.jp/products/a/7premium/cat/140010000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/常温・加工食品/ジャム・はちみつ", "url": "https://www.sej.co.jp/products/a/7premium/cat/140070000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/常温・加工食品/インスタントドリンク", "url": "https://www.sej.co.jp/products/a/7premium/cat/140060000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/パン・シリアル", "url": "https://www.sej.co.jp/products/a/7premium/bread/kanto/1/l100/"},
        {"name": "セブンプレミアム/お菓子/和風菓子・豆菓子", "url": "https://www.sej.co.jp/products/a/7premium/cat/130010000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/お菓子/駄菓子・ガム・キャンディ", "url": "https://www.sej.co.jp/products/a/7premium/cat/130020000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/お菓子/チョコレート・焼き菓子", "url": "https://www.sej.co.jp/products/a/7premium/cat/130030000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/お菓子/スナック", "url": "https://www.sej.co.jp/products/a/7premium/cat/130040000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/スイーツ・アイス/洋菓子", "url": "https://www.sej.co.jp/products/a/7premium/cat/060010010000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/スイーツ・アイス/和菓子", "url": "https://www.sej.co.jp/products/a/7premium/cat/060010020000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/スイーツ・アイス/アイス", "url": "https://www.sej.co.jp/products/a/7premium/cat/060020000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/冷凍食品/冷凍食品", "url": "https://www.sej.co.jp/products/a/7premium/cat/150010000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/冷凍食品/冷凍食材", "url": "https://www.sej.co.jp/products/a/7premium/cat/150020000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/冷凍食品/ロックアイス", "url": "https://www.sej.co.jp/products/a/7premium/cat/150030000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/牛乳・乳製品/牛乳・乳飲料", "url": "https://www.sej.co.jp/products/a/7premium/cat/070010000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/牛乳・乳製品/ヨーグルト・ヨーグルト飲料", "url": "https://www.sej.co.jp/products/a/7premium/cat/070020000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/牛乳・乳製品/バター・チーズ", "url": "https://www.sej.co.jp/products/a/7premium/cat/070030000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/ソフトドリンク/果汁・炭酸飲料", "url": "https://www.sej.co.jp/products/a/7premium/cat/110010000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/ソフトドリンク/お茶・コーヒー・紅茶", "url": "https://www.sej.co.jp/products/a/7premium/cat/110030000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/ソフトドリンク/スポーツドリンク・水・健康飲料ほか", "url": "https://www.sej.co.jp/products/a/7premium/cat/110020000000000/kanto/1/l100/"},
        {"name": "セブンプレミアム/お酒", "url": "https://www.sej.co.jp/products/a/7premium/alcohol/kanto/1/l100/"},
    ]

    all_products = []

    for category in TARGET_CATEGORIES:
        if not category["url"]: continue
        print(f"Retrieving data for {category['name']} category...")
        try:
            response = requests.get(category["url"], headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.find_all("div", class_="list_inner")

            for item in items:
                try:
                    # 商品名
                    name_tag = item.select_one(".detail .item_ttl a")
                    if not name_tag: continue
                    name = name_tag.text.strip()
                    # 商品ページ
                    item_url = "https://www.sej.co.jp" + name_tag['href']
                    # 商品画像
                    img_tag = item.select_one("figure img")
                    img_url = ""
                    if img_tag:
                        img_url = img_tag.get('data-original')
                        if not img_url:
                            img_url = img_tag.get('src')
                    # 価格
                    price_tag = item.select_one(".detail .item_price p")
                    if not price_tag: continue
                    price_text = price_tag.text.strip()
                    match = re.search(r'税込([\d\.,]+)円', price_text)
                    if match:
                        price = float(match.group(1).replace(',', ''))
                    else:
                        continue

                    product_data = {
                        "name": name,
                        "category": category['name'],
                        "price": price,
                        "image": img_url,
                        "url": item_url,
                        "store": "SevenEleven"
                    }
                    all_products.append(product_data)

                except Exception as e:
                    continue

            time.sleep(1)

        except Exception as e:
            print(f"[Error] Error has occurred in {category['name']} category : {e}")

    return all_products

# Lawson
def fetch_lawson():
    print("\n--- Lawson ---")
    TARGET_CATEGORIES = [
        {"name": "おにぎり", "url": "https://www.lawson.co.jp/recommend/original/rice/"},
        {"name": "寿司", "url": "https://www.lawson.co.jp/recommend/original/sushi/"},
        {"name": "お弁当", "url": "https://www.lawson.co.jp/recommend/original/bento/"},
        {"name": "チルド弁当", "url": "https://www.lawson.co.jp/recommend/original/chilledbento/"},
        {"name": "サンドイッチ・ロールパン", "url": "https://www.lawson.co.jp/recommend/original/sandwich/"},
        {"name": "ベーカリー", "url": "https://www.lawson.co.jp/recommend/original/bakery/"},
        {"name": "パスタ", "url": "https://www.lawson.co.jp/recommend/original/pasta/"},
        {"name": "そば・うどん・中華麺", "url": "https://www.lawson.co.jp/recommend/original/noodle/"},
        {"name": "アイス", "url": "https://www.lawson.co.jp/recommend/original/icecream/"},
        {"name": "サラダ", "url": "https://www.lawson.co.jp/recommend/original/salad/"},
        {"name": "お惣菜", "url": "https://www.lawson.co.jp/recommend/original/select/osozai/"},
        {"name": "スープ", "url": "https://www.lawson.co.jp/recommend/original/soup/"},
        {"name": "グラタン・ドリア", "url": "https://www.lawson.co.jp/recommend/original/gratin/"},
        {"name": "お好み焼・たこ焼・他", "url": "https://www.lawson.co.jp/recommend/original/konamono/"},
        {"name": "揚げ物", "url": "https://www.lawson.co.jp/recommend/original/fry/"},
        {"name": "中華まん", "url": "https://www.lawson.co.jp/recommend/original/chukaman/"},
        {"name": "おでん", "url": "https://www.lawson.co.jp/recommend/original/oden/"},
        {"name": "まちかど厨房", "url": "https://www.lawson.co.jp/recommend/original/machikadochubo/"},
        {"name": "コーヒー", "url": "https://www.lawson.co.jp/recommend/original/coffee/"},
        {"name": "デザート", "url": "https://www.lawson.co.jp/recommend/original/dessert/"},
        {"name": "ローソンオリジナル/ベーカリー", "url": "https://www.lawson.co.jp/recommend/original/select/bakery/index.html"},
        {"name": "ローソンオリジナル/お惣菜", "url": "https://www.lawson.co.jp/recommend/original/select/osozai/index.html"},
        {"name": "ローソンオリジナル/カット野菜・カットフルーツ", "url": "https://www.lawson.co.jp/recommend/original/select/cutvegetable/index.html"},
        {"name": "ローソンオリジナル/サラダチキン・他", "url": "https://www.lawson.co.jp/recommend/original/select/salad/index.html"},
        {"name": "ローソンオリジナル/加工肉", "url": "https://www.lawson.co.jp/recommend/original/select/meat/index.html"},
        {"name": "ローソンオリジナル/たまご", "url": "https://www.lawson.co.jp/recommend/original/select/egg/index.html"},
        {"name": "ローソンオリジナル/乳製品", "url": "https://www.lawson.co.jp/recommend/original/select/dairy/index.html"},
        {"name": "ローソンオリジナル/水産・練物", "url": "https://www.lawson.co.jp/recommend/original/select/paste/index.html"},
        {"name": "ローソンオリジナル/水物", "url": "https://www.lawson.co.jp/recommend/original/select/liquid/index.html"},
        {"name": "ローソンオリジナル/漬物", "url": "https://www.lawson.co.jp/recommend/original/select/pickles/index.html"},
        {"name": "ローソンオリジナル/冷凍食品", "url": "https://www.lawson.co.jp/recommend/original/select/frozen/index.html"},
        {"name": "ローソンオリジナル/カップ麺", "url": "https://www.lawson.co.jp/recommend/original/select/cupnoodle/index.html"},
        {"name": "ローソンオリジナル/即席食品", "url": "https://www.lawson.co.jp/recommend/original/select/instant/index.html"},
        {"name": "ローソンオリジナル/飲料", "url": "https://www.lawson.co.jp/recommend/original/select/drink/index.html"},
        {"name": "ローソンオリジナル/菓子", "url": "https://www.lawson.co.jp/recommend/original/select/snack/index.html"},
        {"name": "ローソンオリジナル/アイス", "url": "https://www.lawson.co.jp/recommend/original/select/icecreem/index.html"},
        {"name": "ローソンオリジナル/嗜好食品", "url": "https://www.lawson.co.jp/recommend/original/select/jam/index.html"},
        {"name": "ローソンオリジナル/缶詰・乾物・乾麺", "url": "https://www.lawson.co.jp/recommend/original/select/dry/index.html"},
        {"name": "ローソンオリジナル/調味料", "url": "https://www.lawson.co.jp/recommend/original/select/spice/index.html"},
        {"name": "チルド飲料", "url": "https://www.lawson.co.jp/recommend/original/chilled/index.html"},
        {"name": "焼菓子", "url": "https://www.lawson.co.jp/recommend/original/gateau/index.html"},
        {"name": "ナチュラルローソン菓子", "url": "https://www.lawson.co.jp/recommend/original/kenkosnack/"},
        {"name": "お酒", "url": "https://www.lawson.co.jp/recommend/original/liquor/"},
    ]

    all_products = []

    for category in TARGET_CATEGORIES:
        if not category["url"]: continue
        print(f"Retrieving data for {category['name']} category...")
        try:
            response = requests.get(category["url"], headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.select("ul.col-4 li")
            if not items:
                items = soup.select("ul.col-3 li")

            for item in items:
                try:
                    # 商品名
                    name_tag = item.select_one(".ttl")
                    if not name_tag: continue
                    name = name_tag.text.strip()
                    # 価格
                    price_tag = item.select_one(".price")
                    if not price_tag: continue
                    price_text = price_tag.text.strip()
                    price = 0
                    match_in_paren = re.search(r'税込([\d,]+)円', price_text)
                    if match_in_paren:
                        price = int(float(match_in_paren.group(1).replace(',', '')))
                    else:
                        match_simple = re.search(r'([\d,]+)円', price_text)
                        if match_simple:
                            price = int(float(match_simple.group(1).replace(',', '')))
                        else:
                            continue
                    # 商品ページ
                    url_tag = item.select_one("a")
                    item_url = "https://www.lawson.co.jp" + url_tag.get('href') if url_tag else ""
                    # 商品画像
                    img_tag = item.select_one(".img img")
                    img_url = ""
                    if img_tag:
                        img_url = "https://www.lawson.co.jp" + img_tag.get('src')

                    product_data = {
                        "name": name,
                        "category": category['name'],
                        "price": price,
                        "image": img_url,
                        "url": item_url,
                        "store": "Lawson"
                    }
                    all_products.append(product_data)

                except Exception as e:
                    continue

            time.sleep(1)

        except Exception as e:
            print(f"[Error] Error has occurred in {category['name']} category : {e}")

    return all_products

def create_pr_body(svn, fam, law):
    body = f"""This PR contains the following updates:

| Store | Changes | Status |
|:---|:---:|:---|
| **Seven-Eleven** | `{len(svn)}` | ✅ Success |
| **FamilyMart** | `{len(fam)}` | ✅ Success |
| **Lawson** | `{len(law)}` | ✅ Success |

---

### Changes

- `svn/products_seven.json`
- `fam/products_family.json`
- `law/products_lawson.json`

### Configuration

📅 **Schedule**: Branch creation - At any time (no schedule defined), Automerge - At any time (no schedule defined).

🚦 **Automerge**: Disabled by config. Please merge this manually once you are satisfied.

🔕 **Ignore**: Close this PR and you won't be reminded about this update again.

---

This PR was generated by [GitHub Action](https://github.com/10thGrade/convenience-1000yen-gacha/blob/master/.github/workflows/update_products.yml).

"""
    with open(os.path.join(BASE_DIR, "pr_body.txt"), "w", encoding="utf-8") as f:
        f.write(body)

if __name__ == "__main__":
    svn_data = fetch_seven()
    fam_data = fetch_family()
    law_data = fetch_lawson()
    
    save_json("svn/products_seven.json", svn_data)
    save_json("fam/products_family.json", fam_data)
    save_json("law/products_lawson.json", law_data)
    
    create_pr_body(svn_data, fam_data, law_data)