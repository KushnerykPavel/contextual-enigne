import logging
from datetime import datetime

from transformers import pipeline
import langid
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

sentence_model = SentenceTransformer("/app/models/all-MiniLM-L12-v2")

classifier = pipeline("zero-shot-classification", model="/app/models/MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli",
                      repo_type='model')
kw_model = KeyBERT(model=sentence_model)


class ContentProcessor:
    def __int__(self):
        pass

    async def process_content(self, content: str) -> dict:

        print('processing start: ', self.get_current_time())
        iab_categories = self.get_iab_categories()
        res = langid.classify(content)
        detected_language = {
            'language': res[0] if res[0] not in self.language_dict() else self.language_dict()[res[0]].lower()
        }

        keywords = kw_model.extract_keywords(content, keyphrase_ngram_range=(1, 1), stop_words='english',
                                             use_maxsum=True, top_n=10)
        keywords_result = []
        for keyword in keywords:
            keywords_result.append({
                'keyword': keyword[0],
                'confidence': keyword[1]
            })

        output = classifier(content[:1000], list(iab_categories.keys()), multi_label=False)
        categories = []
        for i in range(len(output['scores'])):
            score = output['scores'][i]
            if score < 0.05:
                break
            label = output['labels'][i]
            category_key = f'{iab_categories[label]}: {label}'
            tmp = {
                'category': category_key,
                'confidence': score
            }
            categories.append(tmp)

        print('processing finished: ', self.get_current_time())
        return {
            'detected_language': detected_language,
            'keywords': keywords_result,
            'categories': categories,
        }

    def get_iab_categories(self) -> dict:
        return {
            "Arts & Entertainment": "IAB1",
            "Automotive": "IAB2",
            "Business": "IAB3",
            "Careers": "IAB4",
            "Education": "IAB5",
            "Family & Parenting": "IAB6",
            "Health & Fitness": "IAB7",
            "Food & Drink": "IAB8",
            "Hobbies & Interests": "IAB9",
            "Home & Garden": "IAB10",
            "Law, Government, & Politics": "IAB11",
            "News": "IAB12",
            "Personal Finance": "IAB13",
            "Society": "IAB14",
            "Science": "IAB15",
            "Pets": "IAB16",
            "Sports": "IAB17",
            "Style & Fashion": "IAB18",
            "Technology & Computing": "IAB19",
            "Travel": "IAB20",
            "Real Estate": "IAB21",
            "Shopping": "IAB22",
            "Religion & Spirituality": "IAB23",
            "Illegal Content": "IAB26"
        }

    def language_dict(self) -> dict:
        return {'aa': 'Afar', 'ab': 'Abkhazian', 'af': 'Afrikaans', 'ak': 'Akan', 'am': 'Amharic',
                'ar': 'Arabic',
                'an': 'Aragonese', 'as': 'Assamese', 'av': 'Avaric', 'ae': 'Avestan', 'ay': 'Aymara',
                'az': 'Azerbaijani', 'ba': 'Bashkir',
                'bm': 'Bambara', 'be': 'Belarusian', 'bn': 'Bengali', 'bh': 'Bihari languages',
                'bi': 'Bislama', 'bs': 'Bosnian',
                'br': 'Breton', 'bg': 'Bulgarian', 'ca': 'Catalan; Valencian', 'ch': 'Chamorro', 'ce': 'Chechen',
                'cu': 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic',
                'cv': 'Chuvash', 'kw': 'Cornish', 'co': 'Corsican',
                'cr': 'Cree', 'cs': 'Czech', 'da': 'Danish', 'de': 'German',
                'dv': 'Divehi; Dhivehi; Maldivian', 'dz': 'Dzongkha',
                'en': 'English', 'eo': 'Esperanto', 'et': 'Estonian', 'eu': 'Basque',
                'ee': 'Ewe', 'fo': 'Faroese', 'fj': 'Fijian', 'fi': 'Finnish', 'fr': 'French', 'fy': 'Western Frisian', 'ff': 'Fulah',
                'Ga': 'Georgian', 'gd': 'Gaelic; Scottish Gaelic', 'ga': 'Irish',
                'gl': 'Galician', 'gv': 'Manx', 'el': 'Greek-Modern (1453-)', 'gn': 'Guarani', 'gu': 'Gujarati',
                'ht': 'Haitian; Haitian Creole', 'ha': 'Hausa',
                'he': 'Hebrew', 'hz': 'Herero', 'hi': 'Hindi', 'ho': 'Hiri Motu', 'hr': 'Croatian', 'hu': 'Hungarian',
                'hy': 'Armenian', 'ig': 'Igbo', 'io': 'Ido', 'ii': 'Sichuan Yi; Nuosu', 'iu': 'Inuktitut', 'ie': 'Interlingue; Occidental',
                'ia': 'Interlingua (International Auxiliary Language Association)', 'id': 'Indonesian', 'ik': 'Inupiaq',
                'is': 'Icelandic', 'it': 'Italian',
                'jv': 'Javanese', 'ja': 'Japanese', 'kl': 'Kalaallisut; Greenlandic', 'kn': 'Kannada', 'ks': 'Kashmiri',
                'ka': 'Georgian', 'kr': 'Kanuri', 'kk': 'Kazakh',
                'km': 'Central Khmer', 'ki': 'Kikuyu; Gikuyu', 'rw': 'Kinyarwanda', 'ky': 'Kirghiz; Kyrgyz',
                'kv': 'Komi', 'kg': 'Kongo', 'ko': 'Korean',
                'kj': 'Kuanyama; Kwanyama', 'ku': 'Kurdish', 'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian',
                'li': 'Limburgan; Limburger; Limburgish', 'ln': 'Lingala',
                'lt': 'Lithuanian', 'lb': 'Luxembourgish; Letzeburgesch', 'lu': 'Luba-Katanga', 'lg': 'Ganda',
                'mh': 'Marshallese',
                'ml': 'Malayalam', 'mr': 'Marathi', 'Mi': 'Micmac', 'mk': 'Macedonian',
                'mg': 'Malagasy', 'mt': 'Maltese',
                'mn': 'Mongolian', 'mi': 'Maori', 'ms': 'Malay', 'my': 'Burmese', 'na': 'Nauru', 'nv': 'Navajo; Navaho',
                'nr': 'Ndebele-South; South Ndebele',
                'nd': 'Ndebele-North; North Ndebele', 'ng': 'Ndonga', 'ne': 'Nepali', 'nl': 'Dutch; Flemish',
                'nn': 'Norwegian Nynorsk; Nynorsk:Norwegian',
                'nb': 'Bokmål-Norwegian; Norwegian Bokmål', 'no': 'Norwegian', 'oc': 'Occitan (post 1500)',
                'oj': 'Ojibwa', 'or': 'Oriya', 'om': 'Oromo',
                'os': 'Ossetian; Ossetic', 'pa': 'Panjabi; Punjabi', 'fa': 'Persian', 'pi': 'Pali', 'pl': 'Polish',
                'pt': 'Portuguese', 'ps': 'Pushto; Pashto',
                'qu': 'Quechua', 'rm': 'Romansh', 'ro': 'Romanian; Moldavian; Moldovan', 'rn': 'Rundi', 'ru': 'Russian',
                'sg': 'Sango', 'sa': 'Sanskrit',
                'si': 'Sinhala; Sinhalese', 'sk': 'Slovak', 'sl': 'Slovenian', 'se': 'Northern Sami',
                'sm': 'Samoan', 'sn': 'Shona', 'sd': 'Sindhi',
                'so': 'Somali', 'st': 'Sotho-Southern', 'es': 'Spanish; Castilian', 'sq': 'Albanian', 'sc': 'Sardinian',
                'sr': 'Serbian', 'ss': 'Swati',
                'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish', 'ty': 'Tahitian', 'ta': 'Tamil', 'tt': 'Tatar',
                'te': 'Telugu', 'tg': 'Tajik', 'tl': 'Tagalog',
                'th': 'Thai', 'bo': 'Tibetan', 'ti': 'Tigrinya', 'to': 'Tonga (Tonga Islands)', 'tn': 'Tswana',
                'ts': 'Tsonga', 'tk': 'Turkmen', 'tr': 'Turkish',
                'tw': 'Twi', 'ug': 'Uighur; Uyghur', 'uk': 'Ukrainian', 'ur': 'Urdu', 'uz': 'Uzbek', 've': 'Venda',
                'vi': 'Vietnamese', 'vo': 'Volapük', 'cy': 'Welsh',
                'wa': 'Walloon', 'wo': 'Wolof', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'za': 'Zhuang; Chuang',
                'zh': 'Chinese', 'zu': 'Zulu'}

    def get_current_time(self):
        now = datetime.now()

        return now.strftime("%H:%M:%S")
