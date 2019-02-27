from elasticsearch_dsl import connections, Document, Date, Text, Integer, GeoPoint, Float, Object

connections.create_connection(hosts=["193.112.33.124"])


class BaixingDoc(Document):
    id = Text()
    url = Text()
    # 价格
    price = Integer()
    # 城市
    city = Text()
    # 位置
    address = Text()
    # 更新时间
    update_date = Date()
    # 经纬度
    location = GeoPoint()
    # 标题
    title = Text()
    # 户型
    house_type = Text()
    # 出租类型
    rent_type = Text()
    # 装修类型
    decorate = Text()
    # 面积
    area = Float()
    # 朝向
    orientation = Text()
    # 更新时间
    update_date = Date()
    # 楼层
    floor = Text()
    # 最高层
    top_floor = Integer()
    # 标签
    tags = Text(multi=True)
    # 图片
    image_urls = Text(multi=True)

    class Index:
        name = 'hrent'

    class Meta:
        doc_type = 'baixing'


if __name__ == '__main__':
    BaixingDoc.init()
