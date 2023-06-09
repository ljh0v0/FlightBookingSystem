
# data_base

## 前后端API

### 航线信息
| 方法     | 路径                                             | 描述                 | Success Code | Success Response       |
| -------- | ------------------------------------------------ | -------------------- | ------------ | ---------------------- |
| `GET`    | `/api/core/airline/`                             | 获取获取符合条件的所有航线信息        |           | 航线信息列表           |
| `POST`   | `/api/core/airline/`                             | 创建新航线             |           |成功/失败   |
| `GET`    | `/api/core/airline/{airline_id}/`               | 获取特定航线的信息   |           | flight_id代表的航线信息 |
| `PATCH`  | `/api/core/airline/{airline_id}/`               | 修改特定航线的信息   |           | 成功/失败   |
| `DELETE` | `/api/core/airline/{airline_id}/`               | 删除航线           |          | 成功/失败                     |

#### 详细描述
#### `/api/core/airline_id/`

获取航线列表

**Body**

**必要字段**

无

**可选字段**

| 字段    | 类型   | 说明             |
| ------- | ------ | ---------------- |
|  from   | string | 如果该字段不为空，则返回起点是from城市名的所有航线，输入为城市的名字 e.g. 保山 |
| to      | string | 如果该字段不为空，则返回终点是to城市名的所有航线   |
| airport_id | string | 如果该字段不为空，则返回所有起点/终点为该机场所在城市的航线 输入为机场的名字 e.g. 长水国际机场  |

**返回示例：**

获取所有航线信息 

request:

```json
{
  "count": 2,
  "airlines": [{
            "airline_id": "11,18,24",
            "from": "保山",
            "from_longitude": "99.1729",
            "from_latitude": "25.05753",
            "to": "南昌",
            "to_longitude": "115.9000015258789",
            "to_latitude": "28.864999771118164",
            "height": 483
            },
            {
            "airline_id": "32,41,53,60,68,77,81",
            "from": "烟台",
            "from_longitude": "121.37200164794922",
            "from_latitude": "37.40169906616211",

"to": "沈阳",
            "to_longitude": "123.48300170898438",
            "to_latitude": "41.639801025390625",
            "height": 237
            }
          ]
}
```
return:
failed: 
```json
{
        "success":false,
        "data":{
            "code": "status_code",
            "detailed_error_code": "detailed_code",
            "error_msg": "error_msg"
        }
}
```
创建新航线
```json
{
  "airline_id": "airline_id",
  "from_city": "city_name 中文名字",
  "to_city": "city_name",
  "height": "height"
 }
```

获取特定航线的信息
```json
{
            "airline_id": "11,18,24",
            "from": "保山",
            "from_longitude": "99.1729",
            "from_latitude": "25.05753",
            "to": "南昌",
            "to_longitude": "115.9000015258789",
            "to_latitude": "28.864999771118164",
            "height": 483
    }
```
修改航线信息
```json
 {
            "from_city" :  "保山",
            "to_city" : null,
            "height" : 1234
        }
```

### 城市信息
| 方法     | 路径                                             | 描述                 | Success Code | Success Response       |
| -------- | ------------------------------------------------ | -------------------- | ------------ | ---------------------- |
| `GET`    | `/api/core/city/`                             | 获取所有城市信息        |           | 城市信息列表           |
| `POST`   | `/api/core/city/`                             | 创建新城市             |           |成功/失败   |
| `DELETE` | `/api/core/city/{city_id}/`               | 删除城市           |          | 成功/失败                     |

#### 详细描述
#### `/api/core/city/`

获取城市列表

**Body**

**必要字段**

无

**可选字段**

无

**返回示例：**

获取所有城市信息 

request:

```json
{
  "count": 2,
  "cities": [{
              "id": "BS",
              "name": "保山",
              "longitude": "99.1729",
              "latitude": "25.05753",
              "province": "云南"
            },
            {
              "id": "NC",
              "name": "南昌",
              "longitude": "115.9000015258789",
              "latitude": "28.864999771118164",
              "province": "江西"
            }
          ]
}
```

### 航空公司信息
| 方法     | 路径                                             | 描述                 | Success Code | Success Response       |
| -------- | ------------------------------------------------ | -------------------- | ------------ | ---------------------- |
| `GET`    | `/api/core/company/`                             | 获取所有航空公司信息        |           | 航空公司信息列表           |
| `GET`    | `/api/core/company/{acro_name}/`               | 获取特定航空公司的信息   |           | 公司缩写为acro_name的航空公司信息 |
| `POST`   | `/api/core/company/`                             | 创建航空公司             |           |成功/失败   |
| `DELETE` | `/api/core/company/{acro_name}/`               | 删除航空公司          |          | 成功/失败                     |

#### 详细描述
#### `/api/core/company/`

获取航空公司列表

**Body**

**必要字段**

无

**可选字段**

无

**返回示例：**

获取所有航空公司

request:

```json
{
  "count": 2,
  "companies": [{
              "acro_name": "CEA",
              "full_name": "东方航空",
              "icon": "如果有返回icon的url, 否则为null",
              "on_rate": "0.83"
            },
            {
              "acro_name": "BUAA",
              "full_name": "北航",
              "icon": "如果有返回icon的url, 否则为null",
              "on_rate": "0.17"
            }
          ]
}
```

### 航班信息
| 方法     | 路径                                             | 描述                 | Success Code | Success Response       |
| -------- | ------------------------------------------------ | -------------------- | ------------ | ---------------------- |
| `GET`    | `/api/core/flight/`                             | 获取符合条件的所有航班信息        |           | 航班信息列表           |
| `GET`    | `/api/core/flight/{flight_id}/`               | 获取特定航班的信息   |           | 航班编号为flight_id的航班信息 |
| `PATCH`  | `/api/core/flight/{flight_id}/`               | 修改特定航班的信息   |           | 成功/失败   |
| `POST`   | `/api/core/flight/`                             | 创建航班             |           |成功/失败   |
| `DELETE` | `/api/core/flight/{flight_id}/`               | 删除航班          |          | 成功/失败                     |

#### 详细描述
#### `/api/core/flight/`

获取航班列表

**Body**

**必要字段**

无

**可选字段**

| 字段    | 类型   | 说明             |
| ------- | ------ | ---------------- |
|  from   | string | 如果该字段不为空，则返回起点是from城市名的所有航班，中文名字 |
| to      | string | 如果该字段不为空，则返回终点是to城市名的所有航班   |
| date      | date | 如果该字段不为空，则返回出发日期date的所有航班   |
| company | string | 如果该字段不为空，则返回该航空公司的航线，简写   |
```json
{           
                "from": "保山",
                "to": null,
                "date":"2020-10-10",
                "company" : "BUAA"
                }
```

**返回示例：**

获取所有航班信息 

request:

```json
{
  "count": 2,
  "flights": [{
            "flight_id": "东航MU5100",
            "current_status": "等待",
            "airport": "东方航空",
            "airplane": "空客330",
            "depart_time": "07:00",
            "from": "首都T2",
            "arrive_time": "09:12",
            "to": "上海虹桥",
            "left_c_tickets": "89",
      	    "left_p_tickets": "89",

            "airline" : "所属航线",
            "on_time": "是否准时",
            "date": "2020-10-10",
            "eprice": 100,
            "cprice":100
            },
            {
            "flight_id": "东航MU5100",
            "current_status": "等待",
            "airport": "东方航空",
            "airplane": "空客330",
            "depart_time": "07:00",
            "from": "首都T2",
            "arrive_time": "09:12",
            "to": "上海虹桥",
            "left_c_tickets": "89",
      	    "left_p_tickets": "89",

            "airline" : "所属航线",
            "on_time": "是否准时",
            "date": "2020-10-10",
            "eprice": 100,
            "cprice":100
            }
          ]
}
```

initial
``` json
 {
            "flight_id": "东航MU5100",
            "current_status": "等待",
            "airport": "东方航空",
            "airplane": "pid",
            "depart_time": "07:00",
            "from": "首都T2",
            "arrive_time": "09:12",
            "to": "上海虹桥",
            "left_c_tickets": "89",
      	    "left__tickets": "89",

            "airline" : "所属航线",
            "on_time": "是否准时",
            "date": "2020-10-10",
            "eprice": 100,
            "cprice":100
        }
```
说明：
- 机场为中文名字全程
- airline 为 airline对应的id，e.g. 18.11.24

patch
```json
         {
            "current_status": "等待",
            "depart_time": "07:00",
            "arrive_time": "09:12",
            "eprice": 100,
            "cprice":100
        }
```
### 机场信息
| 方法     | 路径                                             | 描述                 | Success Code | Success Response       |
| -------- | ------------------------------------------------ | -------------------- | ------------ | ---------------------- |
| `GET`    | `/api/core/airport/`                             | 获取符合条件的所有机场信息        |           | 机场信息列表           |
| `GET`    | `/api/core/airport/{airport_id}`               | 获取特定机场的信息   |           | 机场编号为airport_id的航班信息 |
| `POST`   | `/api/core/airport/`                             | 创建机场            |           |成功/失败   |
| `DELETE` | `/api/core/airport/{airport_id}`               | 删除机场          |          | 成功/失败                     |

#### 详细描述
#### `/api/core/airport/`

获取机场列表

**Body**

**必要字段**

`airport_name` 中文名字
`city_name` 中文名字

**返回示例：**

获取所有机场信息 

request:

```json
{
  "count": 2,
  "airports": [{
                  "airport_id": "1",
                  "airport_name": "长水国际机场",
                  "city": "昆明",
                  "start_time": "2012-06-28(日期格式可以自行规定)",
                  "location": "云南省昆明市官渡区长水村"
              },
              {
                  "airport_id": "2",
                  "airport_name": "大兴国际机场",
                  "city": "北京",
                  "start_time": "2019-09-15",
                  "location": "中国北京市大兴区/河北省廊坊市"
              },
          ]
}
```
说明：
- init时，城市信息写中文全名


### 用户个人信息
| 方法     | 路径                                             | 描述                 | Success Code | Success Response       |
| -------- | ------------------------------------------------ | -------------------- | ------------ | ---------------------- |
| `GET`    | `/api/core/user/`                             | 获取所有用户信息        |           | 用户信息列表           |
| `GET`    | `/api/core/user/{phone}/`               | 获取特定用户的信息   |           | user_id对应的用户信息 |
| `PATCH`  | `/api/core/user/check`                              | 修改特定用户的信息   |           | 成功/失败   |
| `POST`   | `/api/core/user/`                             | 创建用户             |           |成功/失败   |
| `DELETE` | `/api/core/user/{phone}/`                              | 删除用户          |          | 成功/失败                     |

#### 详细描述
#### `/api/core/user/{user_id}/`

获取用户信息

**Body**

**必要字段**

无

**可选字段**

**返回示例：**

获取用户信息 

request:

```json
{
  "userInfo": {
                    "id": "532502200006150012",
                    "sex": "女",
                    "birth": "2000-06-15",
                    "upor": "北京",
                    "name": "柳嘉禾",
                    "phone": "13988261194",
                }
}
```

### 出行记录信息
| 方法     | 路径                                             | 描述                 | Success Code | Success Response       |
| -------- | ------------------------------------------------ | -------------------- | ------------ | ---------------------- |
| `GET`    | `/api/core/trip_record/`                             | 获取出行记录信息        |           | 出行记录信息列表           |
| `POST`   | `/api/core/trip_record/`                             | 创建出行记录            |           |成功/失败   |
| `DELETE` | `/api/core/trip_record/`                              | 删除出行记录          |          | 成功/失败                     |

#### 详细描述
#### `/api/core/trip_record/{user_id}/`

获取用户出行记录列表

**Body**

**必要字段**

无

**可选字段**

| 字段    | 类型   | 说明             |
| ------- | ------ | ---------------- |
|  user_id   | string | 如果该字段不为空，则返回该用户的出行记录信息 |

**返回示例：**

获取用户出行记录列表 

request:

```json
{
  "count": 2,
  "trip_reocrds": [
                    {
                        "flight_id":"东航MU5100",
                        "depart_time": "07:00",
                        "from": "首都T2",
                        "arrive_time": "09:12",
                        "to": "上海虹桥",
                        "seat_id": "12A",
                        "ticket_type": "经济舱",
                        "gate": "10",
                        "price": 620,
                        "person_id": "132312312313213123",
                        "sale_time": "2020-11-21",
                        "phone": "13988261194",
                        "detail": ""
                    },
                    {
                        "flight_id":"东航MU5100",
                        "depart_time": "07:00",
                        "from": "首都T2",
                        "arrive_time": "09:12",
                        "to": "上海虹桥",
                        "seat_id": "12A",
                        "ticket_type": "经济舱",
                        "gate": "10",
                        "price": 620,
                        "person_id": "12313213123123123",
                        "sale_time": "2020-11-21",
                        "phone": "13988261194",
                        "detail": ""
                    },
                ]
}
```
init
```json
{
            "flight_id": "东航MU5100",
            "seat_id": "11A",
            "ticket_type": "经济舱",
            "gate": "A",
            "price": "100",
            "sale_time": "2000-10-10",
            "detail": "hahahahahah"
        }
```
这里gate输入gateID，然后我这里会根据flight找到airport去搞登机口，所以只需要确定gateID就ok。
#### 注册
url: 'register'

json:
``` json
{
                    "id": "12312312313123123123",
                    "sex": "女",
                    "birth": "2000-06-15",
                    "upor": "北京",
                    "name": "柳嘉禾",
                    "phone": "13988261194",
                    "password": "123456"
                }
```
#### 登录
url: 'login'

json:
``` json
{
"username": "13988261194",
"password": "123456"
}
```

#### 登出
url: 'logout'

json:
```json
{
}
```
### 加权限
url: 'permission'

json:
``` json
{
"phone":"1398826114"
}
```
### 机场统计信息

历史准点率
url: api\core\airport\ontime

json:
``` json
{
  "on_time_rate":88.08(float)
}
```

航司航班占比
url: api\core\airport\cpn

request：
```json
{
  "airport_id": "长水国际机场"
}
```

json:
``` json
{
  "count":6,
  "companies": [
                        {"value": 335(int,航班总数), "name": '中国国际航空'},
                        {"value": 310, "name": '东方航空'},
                        {"value": 234, "name": '南方航空'},
                        {"value": 135, "name": '海南航空'},
                        {"value": 1548, "name": '山东航空'}
                ],
}
```

今日航班流量
url: api\core\airport\flow

``` json
{
  "flight_flow": [
                    4,
                    2,
                    1,
                    0,
                    0,
                    0,
                    5,
                    9,
                    10,
                    17,
                    23,
                    27,
                    20,
                    14,
                    17,
                    18,
                    24,
                    20,
                    16,
                    12,
                    10,
                    6,
                    7,
                    4
                ](24个int，分别表示每小时的航班数)
}
```
创建飞机
```json
 {
    "pid" = "1",
    "attTime" = "1",
    "mileage" = "1",
    "ownedCpn" = "BUAA",
    "type" = "播音747"
    "price" = "1",
    "voyCnt" = "1",
    "seatCnt" = "1"
        }
```
创建登机口
```json
         {
    "depId" : "A",
    "airId" : "长水国际机场"
        }
```









---

工作人员url

### 出行记录信息

| 方法   | 路径                | 描述                 | Success Code | Success Response |
| ------ | ------------------- | -------------------- | ------------ | ---------------- |
| `GET`  | `/api/core/worker   | 获取所有机组人员     |              | 获取的人员信息   |
| `POST` | `/api/core/worker   | 创建机组人员         |              | 成功/失败        |
| `GET`  | `/api/core/relation | 获取flight对应的人员 |              | 获取的人员信息   |
| `POST` | `/api/core/relation | 创建关系             |              | 成功/失败        |

#### 详细描述

#### `/api/core/worker`

**获取所有机组人员信息**

```json
{
  "count": 2,
  "workers": [{
                "person_id": "123123", # 电话号码
                "fly_time": "123",
                "company": "东方航空",
                "emp_date": "2020-12-12",
                "pos" : "机长"
            },
            {
                "person_id": "123123",
                "fly_time": "123",
                "company": "东方航空",
                "emp_date": "2020-12-12",
                "pos" : "机长"
            }
          ]
}
```







#### 详细描述

#### `/api/core/worker`

**创建机组人员**

request:

```json
{
            "person_id": "123123", # 电话号码
            "fly_time": "123",
            "company": "东方航空",
            "emp_date": "2020-12-12",
            "pos" : "机长",
            "type" : "pilot"
            #pilot; steward
        }
```

type只能选择pilot 和 steward 确定创建类型（如果错误则返回错误告知type错误）

company为简写



#### 详细描述

#### `/api/core/relation`

**获取对应flight的机组人员**

request：(parameter)

```
"flight" : "MU235_1"
```



返回data

```json
 
{
  "count": 2,
  "workers": [{
                "person_id": "1101032000000000000", # 电话号码
                "fly_time": "123",
                "company": "东方航空",
                "emp_date": "2020-12-12",
                "pos" : "机长"
            },
            {
                "person_id": "1101032000000000000",
                "fly_time": "123",
                "company": "东方航空",
                "emp_date": "2020-12-12",
                "pos" : "机长"
            }
          ]
}
```





#### 详细描述

#### `/api/core/relation`

**创建对应flight的机组人员**

request:

```json
{
    "type" : "pilot", #pilot and steward
    "person_id": "123456", #phone
    "flight": "MU123_2" #flight_id
}
```

type 同创建worker， 只能为pilot 和 steward



### 数据库配置

```python
# 基本配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 数据库引擎
        'NAME': 'flight_ticket_system', # 数据库名
        'USER': 'root', # 账号
        'PASSWORD': '123456', # 密码
        'HOST': '127.0.0.1', # HOST
        'POST': 3306, # 端口
    }
}
```

**创建数据库(before makemigrations)**

```sql
create database flight_ticket_system character set utf8;
```

### django 后台配置

**创建超级用户**

```python
python manage.py createsuperuser
```

```python
Username: data_base
Password: data123456
```

### django 运行

端口(暂定)：8080

```python
python manage.py runserver 8080
```

管理端url: http://127.0.0.1:8080/admin/