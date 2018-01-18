
## 1. 获取数据集
选取 从`(121.3261,31.1293)` 到 `(121.6001,31.2830)` 包括的上海市区地图

## 2. 审查数据

### 2.1 获取标签数量


```python
count_tags(out_file)
```




    {'bounds': 1,
    'member': 30181,
    'meta': 1,
    'nd': 374792,
    'node': 299896,
    'note': 1,
    'osm': 1,
    'relation': 839,
    'tag': 164673,
    'way': 43285}



### 2.2 获取属性数量


```python
count_attrs(out_file)
```




    {'changeset': 344020,
    'generator': 1,
    'id': 344020,
    'k': 164673,
    'lat': 299896,
    'lon': 299896,
    'maxlat': 1
    ...}



### 2.3 获取键的数量


```python
keys = count_keys(out_file)
sorted_keys = {k: v for (v, k) in sorted([(value, key) for (key, value) in keys.items()], reverse=True)}
sorted_keys
```



    {'highway': 19484,
    'building': 16050,
    'name': 15198,
    'name:en': 11061,
    'oneway': 5800,
    'height': 5415,
    'building:levels': 4918,
    'source': 4222,
    'addr:housenumber': 3451,
    ...}



### 2.4 捕获异常键名数量


```python
process_map(out_file)
```




    ({'lower': 123654, 'lower_colon': 40448, 'other': 570, 'problemchars': 1},
    {'include_space': 42, 'non_chinese_name': 187})



### 2.5 修补数据中不完善的地方
审查数据其间可以看到：1. 地址名部分头部或者尾部会出现空格 2. 电话号码格式不统一。
于是制作一个fix_values函数进行清理


```python
def fix_values(filename, out_file):
    # 破坏了原有结构
    # TO-DO
    tree = ET.parse(filename)
    # 修补空格
    for element in tree.iterfind('node/tag'):
        if element.attrib['k'] == 'name':
            if include_space.search(element.attrib['v']):
                element.attrib['v'] = element.attrib['v'].strip()
    # 统一电话号码格式
        if element.attrib['k'] == 'phone':
            if len(element.attrib['v'].split(',')) < 2:
                element.attrib['v'] = '+86-021-' + str(element.attrib['v']).replace(' ', '')[-8:]
            else:
                new_list = []
                for i in (element.attrib['v'].split(',')):
                    new_list.append('+86-021-' + str(i).replace(' ', '')[-8:])
                element.attrib['v'] = ', '.join(new_list)
                
    return tree.write(out_file, encoding="utf-8", xml_declaration=True)

fix_values('shanghai.osm', 'cleaned_shanghai.osm')
```

## 3 数据库操作
### 3.1 转换xml为json格式

### 3.2 使用pymongo连结与封装函数
```python
def get_db(db_name):
    # 连结数据库
    from pymongo import MongoClient
    client = MongoClient('127.0.0.1', 27017)
    db = client[db_name]
    return db

db = get_db('shanghai')
```

### 3.3 数据库查询
数据文件大小


    cleaned_shanghai.osm 大小为：71.89m
    cleaned_shanghai.osm.json 大小为：113.35m
    

#### 3.3.1 做出贡献的用户总数


```python
total_id = len(db.map.distinct('created.user'))
total_id
```
    1091

#### 3.3.2 用户做出的贡献数


```python
pipeline1 = [{'$group': {'_id': '$created.user', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}}]
total_contributes = [doc for doc in db.map.aggregate(pipeline1)]
for i in range(5):
    print('用户ID : {0}, 贡献数 : {1}'.format(total_contributes[i]['_id'], total_contributes[i]['count']))
```
    用户ID : zzcolin, 贡献数 : 45760
    用户ID : HWST, 贡献数 : 41547
    用户ID : Koalberry, 贡献数 : 19203
    用户ID : z_i_g_o, 贡献数 : 18178
    用户ID : yangfl, 贡献数 : 15459

#### 3.3.3 文档数量


```python
db.map.find().count()
```
    343181
#### 3.3.4 节点数量


```python
db.map.find({"type":"node"}).count()
```
    299896
#### 3.3.5 途径数量


```python
db.map.find({"type":"way"}).count()
```
    43276
```python
pipeline2 = [{"$match":{"amenity":{"$exists":1}}},
            {"$group":{"_id":"$amenity","count":{"$sum":1}}},
            {"$sort":{"count":-1}},
            {"$limit":10}]
total_contributes1 = [doc for doc in db.map.aggregate(pipeline2)]
total_contributes1
```
## 4. 其他想法 
### 4.1 用户贡献占比

根据之前的结果，独立用户有1091人，但是前10位占据了贡献总量的60%，前20位占据了贡献总量的74%，仅贡献过1条的用户占了0.1%，如图所示为正偏斜分布，造成这样的原因，很可能是用户编辑不够吸引人，除去特别热心的用户，其他人最多只是试试手。


### 4.2 额外的数据探索
#### 4.2.1 最多的设施


```python
pipeline3 = [{"$match": {"amenity": {"$exists":1}}}, 
            {"$group": {"_id": "$amenity", "count":{"$sum": 1}}}, 
            {"$sort": {"count": -1}}, {"$limit": 10}]
db.map.aggregate(pipeline3)
[doc for doc in db.map.aggregate(pipeline3)]
```
    [{'_id': 'restaurant', 'count': 685},
    {'_id': 'cafe', 'count': 256},
    {'_id': 'school', 'count': 243},
    {'_id': 'bank', 'count': 243},
    {'_id': 'parking', 'count': 230},
    {'_id': 'fast_food', 'count': 158},
    {'_id': 'toilets', 'count': 133},
    {'_id': 'bar', 'count': 102},
    {'_id': 'hospital', 'count': 90},
    {'_id': 'fountain', 'count': 64}]

#### 4.2.2 辐射最广的宗教信仰


```python
pipeline4 = [{"$match": {"religion": {"$exists":1}}}, 
            {"$group": {"_id": "$religion", "count":{"$sum": 1}}}, 
            {"$sort": {"count": -1}}, {"$limit": 5}]
db.map.aggregate(pipeline4)
[doc for doc in db.map.aggregate(pipeline4)]
```
    [{'_id': 'christian', 'count': 17},
    {'_id': 'buddhist', 'count': 9},
    {'_id': 'muslim', 'count': 4},
    {'_id': 'taoist', 'count': 3},
    {'_id': 'jewish', 'count': 1}]
#### 4.2.3 电影院数量


```python
pipeline5 = [{"$match":{"amenity":{"$exists":1}, "amenity":"cinema"}},
            {"$project":{"_id":"$name" }},
            {"$sort":{"_id": -1}}]
db.map.aggregate(pipeline5)
[doc for doc in db.map.aggregate(pipeline5)]
```
    [{'_id': '金逸影城'},
    {'_id': '衡山电影院'},
    {'_id': '海艺影城'},
    {'_id': '正大星美影城'},
    {'_id': '曹杨影城'},
    ...
    {},
    {},
    {},
    {},
    {}]
## 5. 数据集改进建议
本项目所使用的数据集不完整，部分属性格式不统一。
**建议**：在前端编辑页面中，把部分字段作为必填项，同时对所填内容进行正则判断，使得格式统一
**预期问题**：如果用户在不熟悉编辑规则的情况下，很容易出现上传编辑错误，需要重新填写，而后产生挫败感，降低积极性。
