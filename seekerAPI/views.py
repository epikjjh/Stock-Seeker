from django.db import models, connection
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from seekerAPI.models import Stock
import yfinance as yf


class SeekView(APIView):
    renderer_classes = (JSONRenderer, )

    def check_data(self, code):
        data = Stock.objects.filter(code=code).order_by('date')
        if not data:
            return None
        latest = yf.Ticker(code).history('1d')
        if latest.empty or latest.index[0] != data.last().date:
            return None
        return data

    def save_data(self, code, data):
        oldest = data.index[0]
        last_price = 0.0
        for date, price in data[::-1].items():
            if Stock.objects.filter(code=code, date=date).count():
                break
            if price != price:
                price = last_price
            last_price = price
            stock = Stock(code=code, date=date, price=price)
            stock.save()
        Stock.objects.filter(code=code, date__lt=oldest).delete()
        data = Stock.objects.filter(code=code).order_by('date')
        return data

    def get_stock_data(self, code):
        data = yf.Ticker(code).history('180d')
        if data.empty:
            return None
        data = data['Close']

        return data

    def get_max_profit(self, data):
        buy_val = data[0].price
        ret_buy_date = buy_date = sell_date = data[0].date
        max_profit = 0
        for cur in data:
            if cur.price - buy_val > max_profit:
                max_profit = cur.price - buy_val
                sell_date = cur.date
                ret_buy_date = buy_date
            elif buy_val > cur.price:
                buy_val = cur.price
                buy_date = cur.date
        return ret_buy_date, sell_date, max_profit

    def get(self, request):
        code = request.query_params.get('code').upper()
        data = self.check_data(code)
        if data is None:
            data = self.get_stock_data(code)
            if data is None:
                return Response({'buy date': "Wrong code",
                                 'sell date': "Wrong code", 'profit': 0.0})
            data = self.save_data(code, data)
        buy_date, sell_date, profit = self.get_max_profit(data)
        content = {'buy date': buy_date,
                   'sell date': sell_date, 'profit': profit}
        return Response(content)
