## Contextual targeting engine

-----

### Description 
[Contextual targeting](https://www.criteo.com/blog/contextual-vs-behavioral-targeting/) - 
mechanism for extraction features from page content for ads targeting.

### Project technologies
1. Golang
2. Python 
3. React
4. NATS

---

### Supported features 
1. Detect language
2. Keywords
3. [IAB](https://support.aerserv.com/hc/en-us/articles/207148516-List-of-IAB-Categories) categories

Request example:
```http request
curl --location 'http://localhost:3000/api/extract' \
--header 'Authorization: Bearer demo' \
--header 'Content-Type: text/plain' \
--data '{
    "url": "https://www.criteo.com/blog/contextual-vs-behavioral-targeting/"
}'
```

Websocket response example:
```json
{
    "url": "https://www.criteo.com/blog/contextual-vs-behavioral-targeting/",
    "content": "Years ago, the question of whether to put your budget against contextual targeting or behavioral targeting was a spirited debate. Some said contextual targeting should step aside for the newer, more personalized behavioral targeting. Others purported that it wasn\u2019t a question of \u201ceither or\u201d at all, and that both should be used as complementary tactics. More than a decade later, the question still gets asked. The answer, as is the case with most marketing issues, is \u201cit depends\u201d. To help you arrive at an answer, let\u2019s dig into what each type of targeting means. Mythbusting Contextual AdvertisingWhy Every Marketer Should Test It. What is contextual targeting? Contextual targeting refers to displaying ads based on the content of the website on which the ad appears. For example, placing an ad for cookware on a recipe site or an ad for running shoes on a running forum. It\u2019s like the digital equivalent of placing a print ad in a niche magazine. There is category contextual targeting, where ads are targeted to pages that fall into pre-assigned categories, and keyword contextual targeting, where ads are targeted to pages that match specific keywords. Semantic targeting is a more advanced form of contextual targeting, and it involves using machine learning to understand the meaning of each page of content, rather than just identifying matching keywords on a page. Here\u2019s how it works: A crawler scans the web and categorizes pages based on context and semantics. When a user visits a page, that page content information goes to the ad server, which then matches it with relevant ads for the keywords and content The better your system is at understanding the true context of a page, the better your ad matching will be. Here\u2019s an example of a contextually targeted ad for skincare products next to an article about makeup. Photo source: https://blog.adbeat.com/how-to-choose-publishers-advertising-campaigns/ The most recent iteration of contextual advertising can also use first-party data to add commerce signals to contextual signals and build product affinity scores for each URL, so that marketers can zero in on the pages and products that will have the most impact. In light of the fact that third-party cookies are being phased out in the near future, contextual targeting has gained renewed attention because it doesn\u2019t rely on cookies. To learn more, read\u00a0Contextual Targeting in 2021: Everything You Need to Know Before Cookies Disappear. What is behavioral targeting? Behavioral targeting (also known as audience targeting) is the practice of segmenting customers based on web browsing behavior, including things like pages visited, searches performed, links clicked, and products purchased. If you add mobile and physical store data into the mix, that can also include things like location, and in-store purchases. Visitors with similar behaviors are then grouped into defined audience segments, allowing advertisers to target them with specific, relevant ads and content based on their browsing and purchase history. (Learn more:\u00a0[EBOOK] Retargeting 201: In-App, Social, and Video) With behavioral targeting, shopper behavior and purchase intent can be combined to deliver highly relevant, highly personalized ads just at the moment when a shopper is most likely to make a purchase. An oft cited example of behavioral targeting is retargeting ads. How behavioral targeting works. Source: Boomtrain.com So, which is better? In short, they\u2019re both worth testing as part of your digital marketing mix. You knew we\u2019d say that, right? As AI and Big Data continue to advance, and the marketing landscape continues to change, each is evolving to offer more capabilities to advertisers. Using both contextual and behavioral targeting together can help create a more holistic approach and reach shoppers in different ways at different points in their journey.",
    "title": "Targeting 101: Contextual vs. Behavioral Targeting | Criteo",
    "byline": "Betty Ho",
    "length": 3880,
    "excerpt": "To help you decide between contexual vs. behavioral targeting, let\u2019s dig into what each type of targeting means.",
    "site_name": "Criteo",
    "image": "https://www.criteo.com/wp-content/uploads/2018/10/pexels-photo-840996.jpeg",
    "favicon": "https://www.criteo.com/wp-content/themes/criteo2017/img/defaultico.png",
    "detected_language": {
        "language": "english"
    },
    "keywords": [
        {
            "keyword": "audience",
            "confidence": 0.1761
        },
        {
            "keyword": "involves",
            "confidence": 0.1848
        },
        {
            "keyword": "intent",
            "confidence": 0.2063
        },
        {
            "keyword": "semantics",
            "confidence": 0.2123
        },
        {
            "keyword": "marketer",
            "confidence": 0.2207
        },
        {
            "keyword": "marketers",
            "confidence": 0.2446
        },
        {
            "keyword": "ad",
            "confidence": 0.2551
        },
        {
            "keyword": "target",
            "confidence": 0.309
        },
        {
            "keyword": "campaigns",
            "confidence": 0.3377
        },
        {
            "keyword": "contextual",
            "confidence": 0.395
        }
    ],
    "categories": [
        {
            "category": "IAB17: Sports",
            "confidence": 0.2560770809650421
        },
        {
            "category": "IAB8: Food & Drink",
            "confidence": 0.08372100442647934
        },
        {
            "category": "IAB7: Health & Fitness",
            "confidence": 0.06890786439180374
        },
        {
            "category": "IAB10: Home & Garden",
            "confidence": 0.0627426952123642
        },
        {
            "category": "IAB9: Hobbies & Interests",
            "confidence": 0.05967579036951065
        },
        {
            "category": "IAB6: Family & Parenting",
            "confidence": 0.05292807146906853
        }
    ]
}
```