from elasticsearch_dsl import connections, analyzer, token_filter, Document, Text, Integer, GeoPoint, Float, Object

connections.create_connection(hosts=["193.112.33.124"])


class ZiroomDoc(Document):
    id = Text()
    # 价格
    price = Integer()
    # 城市
    city = Text()
    # 位置
    address = Text()
    # 经纬度
    location = GeoPoint()
    # 标题
    title = Text()
    # 户型
    house_type = Text()
    # 面积
    area = Float()
    # 朝向
    orientation = Text()
    # 楼层
    floor = Integer()
    # 最高楼层
    top_floor = Integer()
    # 标签
    tags = Text(multi=True)
    # 图片
    image_urls = Text(multi=True)
    # 房屋配置
    deploy = Object()
    # url
    url = Text()
    # 交通
    traffic = Text()
    # 室友
    chums = Object(multi=True)
    # 付款方式
    payment = Object(multi=True)
    # 推荐
    recommend = Object(multi=True)
    # 活动
    activity = Object(multi=True)
    # 空气检测
    air_part = Object()
    # 视频
    vr_video = Object()

    class Index:
        name = 'hrent'

    class DocType:
        name = 'ziroom'


if __name__ == '__main__':
    ZiroomDoc.init()

