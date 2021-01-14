import requests

class VisWaxGateway:
    @staticmethod
    def fetch_from_fc():
        url_fc = "https://secure.runescape.com/m=forum/sl=0/forums?75,76,378,66118165,goto,1"

        try:
            res_fc = requests.get(url_fc, headers={
                               'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'}, timeout=15)

        except requests.Timeout:
            raise VWGatewayError("Timeout received whilst retrieving data from viswaxfc forum thread")
        except requests.RequestException:
            raise VWGatewayError("Some Error Ocurred whils fetching data from viswaxfc forum thread({str(requests.RequestException)})")

        if res_fc.status_code != 200:
            raise VWGatewayError("Website returned a Non-200 status code")

        return res_fc.text

    @staticmethod
    def fetch_from_alt():
        url_tiamat = "https://secure.runescape.com/m=forum/sl=0/forums?75,76,331,66006366,goto,1"
        try:
            res_tiamat = requests.get(url_tiamat, headers={
                               'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'}, timeout=15)
        except requests.Timeout:
            raise VWGatewayError("Timeout received whilst retrieving data from viswaxfc forum thread")
        except requests.RequestException:
            raise VWGatewayError("Some Error Ocurred whils fetching data from viswaxfc forum thread({str(requests.RequestException)})")

        if res_tiamat.status_code != 200:
            raise VWGatewayError("Website returned a Non-200 status code")
        return res_tiamat.text

class VWGatewayError(Exception):
    pass
