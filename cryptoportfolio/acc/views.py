from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import PortfolioForm, TransactionForm
from .models import Portfolio, Cryptocoin
from django.views.generic import DetailView
from requests import Request, Session
import json
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


def acc_home(request):
    user = request.user.username
    news = get_news()
    portfolio = Portfolio.objects.filter(owner=user)
    info = []
    for i in portfolio:
        coins = get_coin_list(i.id)
        statistic = get_portf_statistic(coins)
        info.append(
            {
                'portfolio': i,
                'statistic': statistic[0]
            }
        )

    return render(request, 'acc/acc_home.html', {'portfolio': info, 'news': news})


def acc_create(request):
    user = request.user.username
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = user
            post.save()
            return HttpResponseRedirect('/acc')
    else:
        form = PortfolioForm()
    form = PortfolioForm()
    context = {'form': form}
    return render(request, 'acc/acc_create.html', context)


class PortfDetailView(DetailView):
    model = Portfolio
    template_name = 'acc/portfolio.html'
    context_object_name = 'portfolio'


def portfolio(request, pk):
    portfolio_ = Portfolio.objects.filter(id=pk)
    coins = get_coin_list(pk)
    statistic = get_portf_statistic(coins)
    data = data_for_diagramm(statistic[0]['price'], coins)
    return render(request, 'acc/portfolio.html',
                  {'portfolio': portfolio_[0], 'coins': coins, 'statistic': statistic[0]})


def transaction(request, pk):
    portfolio_ = Portfolio.objects.filter(id=pk)
    portfolio = portfolio_[0]
    error = ''
    if (portfolio.owner != request.user.username):
        return render(request, 'acc/error.html')
    cryptocoins = Cryptocoin.objects.filter(idPortfolio=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            coin = Cryptocoin()
            coin.amount = -1
            flag = 0
            for i in cryptocoins:
                if i.name == post.name:
                    coin = i
            if coin.amount == -1:
                coin.idPortfolio = portfolio
                coin.name = post.name
                coin.amount = 0
                coin.avgBuyPrice = 0

            if (post.transType == 0):
                if (post.amount > 0):
                    coin.avgBuyPrice = (coin.avgBuyPrice * coin.amount + post.amount * post.price) / (
                            coin.amount + post.amount)
                    coin.amount += post.amount
                else:
                    flag = 1
                    error = 'Нельзя купить отрицательное число монет :/'
            else:
                if post.amount > coin.amount:
                    flag = 1
                    error = 'Вы не можете продать больше, чем у вас есть :/'
                coin.amount -= post.amount
            if flag == 0:
                coin.save()
                return HttpResponseRedirect(f'/acc/{pk}')
    else:
        form = TransactionForm()
    form = TransactionForm
    context = {'form': form, 'error': error}
    return render(request, 'acc/transaction.html', context)


def getPricesApi():
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    parameters = {
        'slug': 'bitcoin,ethereum,tether,dogecoin,solana,bnb',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'c9fab09c-be10-4e6e-b8c3-1501ac01ba2a',
    }
    keys = ['1', '825', '74', '5426', '1839', '1027']
    session = Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    answer = []
    for i in keys:
        answer.append({
            'symbol': json.loads(response.text)['data'][i]['symbol'],
            'price': json.loads(response.text)['data'][i]['quote']['USD']['price'],
            'change_24h': json.loads(response.text)['data'][i]['quote']['USD']['percent_change_24h'],
            'change_7d': json.loads(response.text)['data'][i]['quote']['USD']['percent_change_7d'],
            'change_30d': json.loads(response.text)['data'][i]['quote']['USD']['percent_change_30d'],
            'image_url': 'https://s2.coinmarketcap.com/static/img/coins/64x64/' + i + '.png'
        })
    return answer


def get_news():
    url = 'https://coinmania.com/news/'
    request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urlopen(request_site).read()
    soup = BeautifulSoup(html, 'html.parser')
    news = soup.find_all('article')
    results = []

    for item in news:
        title = item.find('h2').get_text()
        # print('title:', title)
        href = item.a.get("href")
        # print('href:', href)
        desc = item.find('p').get_text()
        # print('description:', desc)
        image = item.find('div', class_='col d-flex justify-content-md-end order-1 order-md-2').find('img')
        if (image != None):
            image = image.get('src')
        # print('image', image)
        results.append({'title': title, 'href': href, 'description': desc, 'picture': image})
    return results


def get_portf_statistic(cryptocoins):
    statistic = []
    price_total = 0
    price_24h = 0
    price_7d = 0
    for i in cryptocoins:
        price = i['price']
        amount = i['amount']
        change_24h = i['change_24h']
        change_7d = i['change_7d']
        price_total += price * amount
        price_24h += ((change_24h / 100) + 1) * price * amount
        price_7d += ((change_7d / 100) + 1) * price * amount
    if (price_total != 0 and price_7d != 0 and price_24h != 0):
        change_24h = round(((price_24h / price_total) - 1) * 100, 2)
        change_7d = round(((price_7d / price_total) - 1) * 100, 2)
    else:
        change_24h = 0
        change_7d = 0
    statistic.append(
        {'price': round(price_total, 2), 'change_24h': round(change_24h, 2), 'change_7d': round(change_7d)})
    return statistic


def get_coin_list(pk):
    prices = getPricesApi()
    cryptocoins_ = Cryptocoin.objects.filter(idPortfolio=pk)
    statistic = []
    for i in cryptocoins_:
        if i.amount != 0:
            price = 'Not Found'
            change_24h = 'Not Found'
            change_7d = 'Not Found'
            change_30d = 'Not Found'
            profit = 'Not Found'
            for j in prices:
                if j['symbol'] == i.name:
                    price = round(j['price'], 2)
                    change_24h = round(j['change_24h'], 2)
                    change_7d = round(j['change_7d'], 2)
                    change_30d = round(j['change_30d'], 2)
                    image_url=j['image_url']
                    profit = round((float(price) - i.avgBuyPrice) * i.amount, 2)
                    break
            if(price!='Not Found'):
                statistic.append(
                    {
                        "name": i.name,
                        "price": price,
                        "assets": i.amount * price,
                        "change_24h": change_24h,
                        "change_7d": change_7d,
                        "change_30d": change_30d,
                        "amount": i.amount,
                        "avgBuyPrice": round(i.avgBuyPrice, 2),
                        "profit": profit,
                        "image_url": image_url
                    }
                )
    return statistic


def data_for_diagramm(total, coins):
    data = []
    for i in coins:
        data.append({
            'name': i['name'],
            'share': i['assets'] / total
        })
    return data
