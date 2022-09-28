# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 8:30:29 2021

@author: siddheshmore
"""
import requests
from urllib.parse import urljoin, urlparse, parse_qs
import csv
from lxml import html
import re

def scrape(link):
    review_fname = "review.csv"
    csv_writer = csv.writer(open(review_fname, "w", encoding='utf-8-sig', newline=''), delimiter=',')
    heading = [
        'Number of Star', 'Review'
    ]
    csv_writer.writerow(heading)
    
    url_body = link.split('/')[-3]
    id = link.split('/')[-1]

    review_url = f"https://www.amazon.com/{url_body}/product-reviews/{id}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.5',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
    }

    sess = requests.Session()
    r = sess.get(review_url, headers=headers)
    tree = html.fromstring(r.text)
    rows = tree.xpath('//div[@data-hook="review"]')

    for i, row in enumerate(rows):
        number_star = row.xpath('.//a[@class="a-link-normal"]/@title')[0].split()[0]
        review = " ".join([elm.strip() for elm in row.xpath('.//span[@data-hook="review-body"]//text()') if elm.strip()])

        result_row = [review, number_star]

        csv_writer.writerow(result_row)
        print(result_row)

    page = 1
    while 1:
        page += 1
        next_link = f"https://www.amazon.com/{url_body}/product-reviews/{id}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber={page}"
        sess = requests.Session()
        r = sess.get(next_link, headers=headers)
        tree = html.fromstring(r.text)
        rows = tree.xpath('//div[@data-hook="review"]')

        if rows:
            for i, row in enumerate(rows):
                try:
                    number_star = row.xpath('.//i[contains(@data-hook, "review-star-rating")]/@class')[0]
                    number_star = re.findall('a-star-([0-9]+)', number_star)[0]
                except:
                    number_star = ""

                try:
                    review = " ".join(
                        [elm.strip() for elm in row.xpath('.//span[@data-hook="review-body"]//text()') if elm.strip()])
                except:
                    review = ""

                if not number_star and not review:
                    continue

                result_row = [review, number_star]

                csv_writer.writerow(result_row)
                print(result_row)
        else:
            break

if __name__ == '__main__':
    link = "https://www.amazon.com/Sennheiser-Momentum-Cancelling-Headphones-Functionality/dp/B07VW98ZKG"
    scrape(link=link)
