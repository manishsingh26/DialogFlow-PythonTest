
import simplejson as json
import os
from flask import Flask
from flask import request
from flask import make_response

# Defining Flask app globally.
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():

    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json; charset=utf-8'
    return r


def makeWebhookResult(req):

    if req.get('queryResult').get('action') != 'interest':
        return {}

    result = req.get('queryResult')
    parameters = result.get('parameters')
    zone = parameters.get('Bank_Name')

    bank = {
        'ICICI': '5.67',
        'SBI': '6.67',
        'IDBI': '7.67',
        'HDFC': '8.67'
    }

    speech = 'The interest rate of ' + zone + ' is ' + str(bank[zone])
    print("")
    return {
        "speech": speech,
        "displayText": speech,
        "data": None,
        "contextOut": None,
        "source": "BankInterestRates"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print('Starting app on port: %d' % port)
    app.run(debug=True, port=port, host='0.0.0.0')
