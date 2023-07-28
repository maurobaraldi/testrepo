import datetime
import json
import os
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen
import urllib
import xml

from jinja2 import Environment, FileSystemLoader


RSS_LIST = [
    {'uri': 'multicoin.capital', 'path': '/rss.xml', 'name': 'Multicoin Capital'},
    {'uri': 'blog.ethereum.org', 'path': '/en/feed.xml', 'name': 'Ethereum Blog'},
    {'uri': 'decrypt.co', 'path': '/feed', 'name': 'Decrypt'},
    {'uri': 'www.bitdegree.org', 'path': '/crypto/news/rss', 'name': 'Crypto News Alerts - Bitcoin, Ethereum & Cryptocurrency News'},
    {'uri': 'u.today', 'path': '/rss', 'name': 'U.Today'},
    {'uri': 'blog.aragon.org', 'path': '/rss/', 'name': "Aragon's Blog "}, 
    {'uri': 'nowpayments.io', 'path': '/blog/feed', 'name': 'NOWPayments'},
    {'uri': 'blockchain.news', 'path': '/rss', 'name': 'Blockchain News'},
    {'uri': 'cointelegraph.com', 'path': '/rss', 'name': 'Cointelegraph.com News'},
    {'uri': 'bitcoinmagazine.com', 'path': '/.rss/full/', 'name': 'Bitcoin Magazine - Bitcoin News, Articles and Expert Insights'},
    {'uri': 'bitcoinist.com', 'path': '/feed/', 'name': 'Bitcoinist.com'},
    {'uri': 'www.coinspeaker.com', 'path': '/news/feed/', 'name': 'News | Coinspeaker'},
    {'uri': 'cryptopotato.com', 'path': '/feed/', 'name': 'CryptoPotato'},
    {'uri': 'cryptobriefing.com', 'path': '/feed/', 'name': 'Crypto Briefing'},
    {'uri': 'medium.com', 'path': '/feed/coinmonks', 'name': 'Coinmonks - Medium'},
    {'uri': 'medium.com', 'path': '/feed/@cointradeIndia', 'name': 'Stories by CointradeIndia on Medium'},
    {'uri': 'news.bitcoin.com', 'path': '/feed/', 'name': 'Bitcoin News'},
    {'uri': 'hackernoon.com', 'path': '/tagged/cryptocurrency/feed', 'name': 'Hacker Noon - cryptocurrency'},
    {'uri': 'blog.bitfinex.com', 'path': '/feed/', 'name': 'Bitfinex blog'},
    {'uri': 'cryptoslate.com', 'path': '/feed/', 'name': 'CryptoSlate'},
    {'uri': 'blog.bitmex.com', 'path': '/feed/', 'name': 'BitMEX Blog'},
    {'uri': 'coincheckup.com', 'path': '/blog/feed/', 'name': 'CoinCheckup Blog – Cryptocurrency News, Articles & Resources'},
    {'uri': 'bitcoinik.com', 'path': '/feed/', 'name': 'Bitcoinik'},
    {'uri': 'coinchapter.com', 'path': '/feed/', 'name': 'CoinChapter'},
    {'uri': 'coingeek.com', 'path': '/feed/', 'name': 'CoinGeek'},
    {'uri': 'blog.coinjar.com', 'path': '/rss/', 'name': 'Bitcoin & Cryptocurrency Blog - Official CoinJar Blog'},
    {'uri': 'cryptosrus.com', 'path': '/feed/', 'name': 'CryptosRus'},
    {'uri': 'boxmining.com', 'path': '/feed/', 'name': 'Boxmining'},
    {'uri': 'cryptoadventure.com', 'path': '/feed/', 'name': 'Crypto Adventure'},
    {'uri': 'bitpinas.com', 'path': '/feed/', 'name': 'BitPinas'},
    {'uri': 'www.trustnodes.com', 'path': '/feed', 'name': 'Trustnodes'},
    {'uri': 'www.bitcoinmarketjournal.com', 'path': '/feed/', 'name': 'Bitcoin Market Journal'},
    {'uri': 'coinrevolution.com', 'path': '/feed/', 'name': 'Coinrevolution'},
    {'uri': 'bitcoinnews.com', 'path': '/feed/', 'name': 'Bitcoin News'},
    {'uri': 'coinidol.com', 'path': '/rss2/', 'name': 'CoinIdol.com News'},
    {'uri': 'themerkle.com', 'path': '/feed/', 'name': 'The Merkle News'},
    {'uri': 'www.livebitcoinnews.com', 'path': '/feed/', 'name': 'Live Bitcoin News'},
    {'uri': 'alexablockchain.com', 'path': '/feed/', 'name': 'AlexaBlockchain'},
    {'uri': 'blockmanity.com', 'path': '/feed/', 'name': 'Blockmanity'},
    {'uri': 'blog.coinfabrik.com', 'path': '/feed/', 'name': 'CoinFabrik Blog'},
    {'uri': 'coinscribble.com', 'path': '/feed/', 'name': 'Coinscribble'},
    {'uri': 'medium.com', 'path': '/feed/buyucoin-talks', 'name': 'BuyUcoin Talks - Medium'},
    {'uri': 'cryptodisrupt.com', 'path': '/feed/', 'name': 'CryptoDisrupt'},
    {'uri': 'www.forbes.com', 'path': '/crypto-blockchain/feed/', 'name': 'Forbes - Crypto & Blockchain'},
    {'uri': 'themarketscompass.substack.com', 'path': '/feed', 'name': "The Market's Compass Technical View"}, 
    {'uri': 'blog.kraken.com', 'path': '/feed/', 'name': 'Kraken Blog'},
    {'uri': 'ambcrypto.com', 'path': '/feed/', 'name': 'AMBCrypto'},
    {'uri': 'bitpay.com', 'path': '/blog/rss/', 'name': 'The BitPay Blog'},
    {'uri': 'dailyhodl.com', 'path': '/feed/', 'name': 'The Daily Hodl'},
    {'uri': 'www.crypto-news-flash.com', 'path': '/feed/', 'name': 'Crypto News Flash'},
    {'uri': 'www.cryptela.com', 'path': '/blog-rss', 'name': 'Blog RSS feed'},
    {'uri': 'www.cryptonewsz.com', 'path': '/feed/', 'name': 'CryptoNewsZ'},
    {'uri': 'blog.liquid.com', 'path': '/rss.xml', 'name': 'Liquid Blog'},
    {'uri': 'zycrypto.com', 'path': '/feed/', 'name': 'ZyCrypto'},
    {'uri': 'www.financemagnates.com', 'path': '/cryptocurrency/feed/', 'name': 'CryptoCurrency – Finance Magnates | Financial and business news'},
    {'uri': 'cryptomining-blog.com', 'path': '/feed/', 'name': 'Crypto Mining Blog'},
    {'uri': 'thecryptobasic.com', 'path': '/feed/', 'name': 'The Crypto Basic'},
    {'uri': 'coinsutra.com', 'path': '/blog/feed/', 'name': 'CoinSutra Blog: Cryptocurrency Guides & Tutorials – CoinSutra – Bitcoin Community'},
    {'uri': 'webscrypto.com', 'path': '/feed/', 'name': 'WebsCrypto'},
    {'uri': 'komodoplatform.com', 'path': '/en/blog/rss/', 'name': 'Komodo Platform Blog | En'},
    {'uri': 'ciphertrace.com', 'path': '/feed/', 'name': 'CipherTrace – The Blockchain Security Company'},
    {'uri': 'thenewscrypto.com', 'path': '/feed/', 'name': 'TheNewsCrypto – Blockchain & Cryptocurrency News Media | Crypto Guide'},
    {'uri': 'dailycoin.com', 'path': '/feed/', 'name': 'DailyCoin'},
    {'uri': 'blockonomi.com', 'path': '/feed/', 'name': 'Blockonomi'},
    {'uri': 'bravenewcoin.com', 'path': '/news/rss', 'name': 'BNC insights feed'},
    {'uri': 'coindoo.com', 'path': '/feed/', 'name': 'Coindoo'},
    {'uri': 'e-cryptonews.com', 'path': '/feed/', 'name': 'E-Crypto News'},
    {'uri': 'thebitcoinnews.com', 'path': '/feed/', 'name': 'The Bitcoin News – Blockchain and Bitcoin News'},
    {'uri': 'nulltx.com', 'path': '/feed/', 'name': 'NullTX'},
    {'uri': 'www.bitrates.com', 'path': '/feed/rss', 'name': 'Bitrates.com Feed'},
    {'uri': 'crypto.news', 'path': '/feed/', 'name': 'crypto.news'},
    {'uri': 'coinjournal.net', 'path': '/feed/', 'name': 'CoinJournal: Latest Bitcoin, Ethereum & Crypto News'},
    {'uri': 'cryptoticker.io/en', 'path': '/feed/', 'name': 'CryptoTicker'},
    {'uri': 'www.coolwallet.io/news', 'path': '/feed/', 'name': 'News Archives - CoolWallet'},
    {'uri': 'blocktelegraph.io', 'path': '/feed/', 'name': 'Block Telegraph'},
    {'uri': 'coinstats.app/blog', 'path': '/feed/', 'name': 'CoinStats Blog'},
    {'uri': 'coinpedia.org', 'path': '/feed/', 'name': 'Coinpedia Fintech News'},
    {'uri': 'stealthex.io/blog', 'path': '/feed/', 'name': 'StealthEX'},
    {'uri': 'cryptonews.com.au', 'path': '/feed/', 'name': ' Crypto News Australia '},
    {'uri': 'crypto-academy.org', 'path': '/feed/', 'name': 'Crypto Academy'}
]

FAILS = [
    {'uri': 'cryptoshrypto.com', 'path': '/feed/', 'name': []}, 
    {'uri': 'www.newsbtc.com', 'path': '/feed/', 'name': "NewsBTC", "schema": True}, 
    {'uri': '99bitcoins.com', 'path': '/feed/', 'name': "99 Bitcoins", "schema": True},
    {'uri': 'cryptoverze.com', 'path': '/feed/', 'name': 'Cryptoverze'},
    {'uri': 'blog.buyucoin.com', 'path': '/feed/', 'name': 'BuyUcoin Blog'},
]

LOCAL = False

articles = []

def parse_date(date, days=0):
    '''
    Parse date from str to datetime obj.
    
    date: date as str format.
    days: since days ago news.
    '''
    #import pdb; pdb.set_trace()
    _date = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S')
    if _date.date() >= (datetime.datetime.now() - datetime.timedelta(days=days)).date():
        return date

if LOCAL is False:
    for i in RSS_LIST[:20]:
        uri = f"https://{i['uri']}{i['path']}"
        request = Request(uri, headers={'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'})
        try:
            with urlopen(request) as r:
                rss = r.read().decode("utf8")
        except urllib.error.HTTPError:
            print(uri)

        try:
            tree = ET.fromstring(rss)
        except xml.etree.ElementTree.ParseError:
            import pdb; pdb.set_trace()
        result = {}
        result['source'] = i['name']
        result['uri'] = i['uri']
        result['items'] = []
        items = tree.find('channel').findall('item')

        try:
            for item in items:
                #if parse_date(item.find('pubDate').text[:25], 2):
                result['items'].append({
                    'language': tree.find('channel').find('language').text if tree.find('channel').find('language') else "",
                    'title': item.find('title').text,
                    'link': item.find('link').text,
                    'date': parse_date(item.find('pubDate').text[:25], 2),
                })
        except (ET.ParseError, AttributeError, TypeError) as _:
            print('URI error:', uri)
        
        articles.append(result)

    with open('./result.json', 'w') as f:
        f.write(json.dumps(articles))
else:
    with open('./result.json') as f:
        articles = json.loads(f.read())

print(len(articles))
env = Environment(loader = FileSystemLoader(searchpath = os.path.join(os.path.dirname(os.path.abspath(__file__)))))
template = env.get_template("template_test.html")

with open('index.html', 'w') as t:
    t.write(template.render(articles=articles))
