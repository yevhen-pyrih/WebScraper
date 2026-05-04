import os
import json
import  requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

product_code = "91869341"
page = 1
next = True
headers = {
    'Host': 'www.ceneo.pl',
    'Cookie': 'sv3=1.0_9ff2bc82-3ccc-11f1-b64f-bd1c4e0de6c9; urdsc=2; userCeneo=ID=52ddb52d-81ee-486e-b3f9-18503e4925cc; __RequestVerificationToken=5Lv4GDqyn3V0oOFKkc1LSsayvC2dvN01-C091ncoQlZpRReVe1xVX7xmtp1GPI6m-jcvylOxR3V2qCEkO0KIcxgksu-XKMCubZxQkwnFprk1; ai_user=jNUpw|2026-04-20T15:21:34.119Z; partner=3iflvgzSYhhh3mIx5yEvsYlKoMGjF6mAjLkpUyTprOnlDLl8no9cglzTpf087lUwHe0OqwBHZyX6II6giJnvTkMp1SgfgJv7rbzcZytnLZNlB30Ezw81tjuL0HBmWSFPeeWO3BoZIm4XrX3TIAwXsJmIextxP5PDlipeMDHL2Kr%2fLJnX6NUOWQ%3d%3d; __utmf=a0ddcba11e6839fa737ad3d04ed1d537_k2wCRI6tAVSgxOOwMsWh%2Bvo35Yf981ST; ai_session=KUsAt|1776698494498.1|1776698494498.1; appType=%7B%22Value%22%3A1%7D; cProdCompare_v2=; browserBlStatus=1; consentcookie=eyJBZ3JlZUFsbCI6bnVsbCwiQ29uc2VudHMiOlsxXSwiVENGQ29uc2VudERhdGEiOnsiPFB1cnBvc2VzPmtfX0JhY2tpbmdGaWVsZCI6W10sIjxTcGVjaWFsRmVhdHVyZXM+a19fQmFja2luZ0ZpZWxkIjpbXSwiPFZlbmRvcnM+a19fQmFja2luZ0ZpZWxkIjp7IjxDb25zZW50cz5rX19CYWNraW5nRmllbGQiOltdLCI8RGlzY2xvc2VkVmVuZG9ycz5rX19CYWNraW5nRmllbGQiOlsxLDIsNCw5LDEwLDExLDEyLDEzLDE1LDE2LDIxLDIyLDIzLDI0LDI1LDI3LDI4LDMwLDMxLDMyLDM0LDM3LDM5LDQwLDQyLDQ0LDQ1LDUwLDUyLDUzLDU5LDYwLDY4LDY5LDcwLDcxLDcyLDc2LDc3LDgwLDgxLDgyLDg0LDg1LDkxLDkzLDk1LDk3LDk4LDEwMiwxMDksMTEwLDExNSwxMTksMTIwLDEyMiwxMjQsMTI2LDEyNywxMjgsMTI5LDEzMCwxMzEsMTMyLDEzMywxMzQsMTM4LDEzOSwxNDAsMTQxLDE0NywxNTYsMTU3LDE2MSwxNjMsMTY4LDE4NCwxOTIsMTkzLDE5NSwyMDIsMjEwLDIxMywyMjYsMjI4LDIzMSwyNDEsMjQzLDI0NiwyNTMsMjU5LDI2NCwyNzIsMjczLDI3NSwyNzgsMjgxLDI4NCwyOTQsMzAxLDMwNCwzMTIsMzE1LDMxNywzMjgsMzQ1LDM2MSwzNzMsMzc1LDM4MSwzODQsMzg4LDM5NCwzOTcsNDAyLDQxNSw0MTYsNDM1LDQ0Nyw0NTIsNDY4LDQ3NSw0OTMsNDk4LDUxMiw1MzEsNTM0LDU0Niw1NTEsNTU5LDU2MSw1ODQsNTg3LDU5MSw2MDYsNjMwLDYzMSw2NTMsNjU3LDY2Myw2NjcsNjkwLDcwMyw3MDcsNzE2LDcyMSw3MjgsNzM0LDc0Miw3NDYsNzU1LDc1OCw3NTksNzYyLDc2Nyw3NzIsNzkzLDgwNiw4MTIsODE0LDgyNyw4MzEsODMyLDg0OCw4NTMsOTI5LDkzMCw5NjksOTg1LDEwMTksMTAyOSwxMDUxLDExMDAsMTExNiwxMTI2LDExMjcsMTEzNSwxMTQyLDExNzgsMTI0MiwxMjcwLDEzMDNdLCI8TGVnaXRpbWF0ZUludGVyZXN0cz5rX19CYWNraW5nRmllbGQiOltdfX0sIlRDU3RyaW5nIjoiQ1FpOWowQVFpOWowQUd5QUJDUExDYkVnQUFBQUFBQUFBQjVZQUFBQUFBQUEuSUtMdEQ3RDdkTFdGZ3dIeG5ZS3NRTUkxZjhlQ0FZb1FBQkFhQkFTQUJTQUtRSUlRR2trQVFKQVNnQkFBQ0FBSUFLQ1JCSVFBTUFBQ0FDRUFBUUlBQUlRQUVBQUNRQVFnS0FBQUVpQUFRQUFBWUFBQWlDSUFBQVFBSWdFSUVFQkVBbVFoQUFBSUFFRkFBakFBRUlBQUFBQUFBQUFBQUF3QUFBQUFDQUFJQUFBQUFnQ0FBQUlBQUFBQUFBRUFBUUJnSUVBQUFBQUVBQUFBQUFBQUFBUUFBQUJBQUFBQUlBIiwiVHJ1c3RlZFBhcnRuZXJzIjpbXSwiVmVyc2lvbiI6InYzIn0=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
}
url = f"https://www.ceneo.pl/{product_code}/opinie-{page}"

# path_to_driver = "C:\\chromedriver-win64\\chromedriver.exe"
# service = Service(path_to_driver)
driver = webdriver.Chrome()
driver.get(url)
driver.find_element(by="xpath", value='//*[@id="js_cookie-consent-general"]/div/div[2]/button[1]').click()

all_opinions = []

while next:
    url = f"https://www.ceneo.pl/{product_code}/opinie-{page}"
    print(url)

    response = requests.get(url, headers=headers)
    print(response.status_code)

    if response.status_code == 200:
        page_dom = BeautifulSoup(response.text, 'html.parser')
        print(type(page_dom))

        if page == 1:
            product_name = page_dom.select_one("h1.product-top__product-info__name").get_text(strip=True) if page_dom.select_one("h1.product-top__product-info__name") else "N/A"
            print(product_name)

        opinions = page_dom.select("div.js_product-review:not(.user-post--highlight)")

        print(type(opinions))
        print(len(opinions))


        for opinion in opinions:
            single_opinion = {
                'opinion_id': opinion['data-entry-id'],
                'author': opinion.select_one("span.user-post__author-name").get_text().strip(),
                'recommendation': opinion.select_one("span.user-post__author-recommendation > em").get_text().strip() if opinion.select_one("span.user-post__author-recommendation > em") else None,
                'score': opinion.select_one("span.user-post__score-count").get_text().strip(),
                'content': opinion.select_one("div.user-post__text").get_text().strip(),
                'pros': [p.get_text().strip() for p in opinion.select_one("div.review-feature__item--positive")] if opinion.select_one("div.review-feature__item--positive") else [],
                'cons': [c.get_text().strip() for c in opinion.select_one("div.review-feature__item--negative")] if opinion.select_one("div.review-feature__item--negative") else [],
                'likes': opinion.select_one("button.vote-yes > span").get_text().strip(),
                'dislikes': opinion.select_one("button.vote-no > span").get_text().strip(),
                'publication_date': opinion.select_one("span.user-post__published > time:nth-child(1)")['datetime'].strip(),
                'purchase_date': opinion.select_one("span.user-post__published > time:nth-child(2)")['datetime'].strip() if opinion.select_one("span.user-post__published > time:nth-child(2)[datetime]") else None
            }
            all_opinions.append(single_opinion)

        next = True if page_dom.select_one("button.pagination__next") else False
        if next: page += 1

        if not os.path.exists("./opinions"):
            os.mkdir("./opinions")

        with open(f"./opinions/{product_code}.json", "w", encoding="UTF-8") as json_file:
            json.dump(all_opinions, json_file, indent=4, ensure_ascii=False)