#### 数据验证api

调用
```
from filter import Filter
```

ip验证
```
def test_ip():
    test_ip_dict = {
    "ip": "91.229.79.184",
    "apt_organization": [],
    "category": [],
    "disclosure_time": "2019-10-12",
    "reference": "https://redqueen.tj-un.com/IntelDetails.html?id=77133903f14c4a02b0e89cb8da9ba256",
    "subscribe_vendor": "天际友盟",
    "verify": []
    }
    test = Filter(test_ip_dict)
    print(test.check_ioc())
```

url、domain验证
```
def test_domain():
    test_domain_dict = {
    "domain": "https://justin.drinkeatgood.space/api/V1/public/",
    "apt_organization": [],
    "category": [],
    "disclosure_time": "2019-10-12",
    "reference": "https://redqueen.tj-un.com/IntelDetails.html?id=77133903f14c4a02b0e89cb8da9ba256",
    "subscribe_vendor": "天际友盟",
    "verify": []
    }
    test = Filter(test_domain_dict)
    print(test.check_ioc())
```

mail验证
```
def test_mail():
    test_email_dict = {
    "email": "amado_buckner627@first.scoldly.com",
    "apt_organization": [],
    "category": [],
    "disclosure_time": "2019-10-12",
    "reference": "https://redqueen.tj-un.com/IntelDetails.html?id=77133903f14c4a02b0e89cb8da9ba256",
    "subscribe_vendor": "天际友盟",
    "verify": []
    }
    test = Filter(test_email_dict)
    print(test.check_ioc())
```

hash 验证
```
def test_hash():
    test_hash_dict = {
    "file_name": "",
    "md5": "",
    "sha1": "2ae861406a7d516b0539c409851cf7f3c8a9716a",
    "sha256": "",
    "file_type": "",
    "file_size": None,
    "file_names": [],
    "apt_organization": [],
    "category": [],
    "disclosure_time": "2019-10-12",
    "reference": "https://redqueen.tj-un.com/IntelDetails.html?id=77133903f14c4a02b0e89cb8da9ba256",
    "subscribe_vendor": "天际友盟",
    "verify": []
    }
    test = Filter(test_hash_dict)
    test.check_ioc()
    print(test.check_dict)
```

返回结果如result.json所示


#### redis处理数据

send调用
```
from RedisHelper import send_ioc

test_domain_dict = {
    "domain": "https://justin.drinkeatgood.space/api/V1/public/",
    "apt_organization": [],
    "category": [],
    "disclosure_time": "2019-10-12",
    "reference": "https://redqueen.tj-un.com/IntelDetails.html?id=77133903f14c4a02b0e89cb8da9ba256",
    "subscribe_vendor": "天际友盟",
    "verify": []
    }
send_ioc(test_domain_dict)
```

recive调用
```
from RedisHelper import deal_ioc
deal_ioc()
```
