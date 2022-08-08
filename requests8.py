import requests
import time
from lxml import etree
import re

def req4data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers)
    return response


def getPageInfo():
    url = "https://gz.fang.anjuke.com/loupan/all/p{}/"
    name_list = []
    addr_list1 = []
    addr_list2 = []
    addr_list3 = []
    price_list = []
    layout_list = []
    square_list = []
    pricetype_list = []
    tag_list = []
    tag_panel_list1 = []
    tag_panel_list2 = []
    for i in range(1, 31):
        newurl = url.format(i)
        response = req4data(newurl)
        # response.content.decode("utf-8")
        print(len(response.text))
        html_pages = etree.HTML(response.text)
        div_item_mod = html_pages.xpath('//div[@class="item-mod "]')
        for item in div_item_mod:
            lp_name = item.xpath('.//a[@class="lp-name"]/span/text()')
            addr = item.xpath('.//a[@class="address"]/span/text()')
            house_type = item.xpath(
                './/a[@class="huxing"]/span[not(@class)]/text()')  # 户型有多个span，要拆分,详见
            # https://blog.csdn.net/u014096024/article/details/48337961/
            price_type = item.xpath('.//a[@class="favor-pos"]/p[@class="price"]/text()')
            price = item.xpath('.//a[@class="favor-pos"]//span/text()')
            house_sqare = item.xpath('.//a[@class="huxing"]//span[@class="building-area"]/text()')
            tag = item.xpath('.//a[@class="tags-wrap"]/div/span[@class="tag"]/text()')
            tag_panel = item.xpath('.//a[@class="tags-wrap"]/div/i/text()')
            # 以结果集方式存储
            if len(lp_name) != 0:
                name_list.append(lp_name[0].strip())
            else:
                name_list.append('')

            if len(addr) != 0:
                # 下面是进行楼盘地址处理 目标：将地址栏[]内的地址拆分成两个，重新进行存储  而[]后面的地址新增详细地址
                pattern = re.compile('[\[].*[\]]')
                pattern2 = re.compile('\].*')
                tmpaddrlist = re.search(pattern, addr[0]).group().replace('[', '').replace(']', '').strip().split(
                    sep=' ')
                addr_list1.append(tmpaddrlist[0])
                addr_list2.append(tmpaddrlist[1])
                addr_list3.append(re.search(pattern2, addr[0]).group().replace(']', '').replace(' ', '').strip())

            else:
                addr_list1.append('')
                addr_list2.append('')
                addr_list3.append('')
            # 价格这边，如果有均价/总价，获取的是均价/总价，如果没有均价/总价，获取的是周边均价，如果都没有，那就是空;先转成整型
            if len(price) != 0:
                price_list.append(price[0].strip())
            else:
                price_list.append('')
            # 下面是对楼盘的处理，由于上面re写的时候出了问题，所以周边均价的housetype获取不到，但这并不妨碍我们用排除法把它加上去
            if len(price_type) != 0:
                pricetype_list.append(price_type[0].strip())
            else:
                if len(price) != 0:
                    pricetype_list.append('周边均价')
                else:
                    pricetype_list.append('')
            tmp_string = ''
            if len(house_type) != 0:
                for h in house_type:
                    tmp_string += h.strip() + ";"
                layout_list.append(tmp_string)
            else:
                layout_list.append('')
            tmp_string2 = ''
            if len(tag) != 0:
                for t in tag:
                    tmp_string2 += t.strip() + ";"
                tag_list.append(tmp_string2)
            else:
                tag_list.append('')

            # 下面是square处理 目标：把建筑面积：和 ㎡去掉

            if len(house_sqare) != 0:
                square_list.append(house_sqare[0].strip().replace('建筑面积：', '').replace('㎡', ''))
            else:
                square_list.append('')
            if len(tag_panel) != 0:
                tag_panel_list1.append(tag_panel[0])
                tag_panel_list2.append(tag_panel[1])
            else:
                tag_panel_list1.append('')
                tag_panel_list2.append('')
        time.sleep(1)
    pass
    # 以字典方式存储
    data_dict = {
        'name': name_list,
        'price': price_list,
        'square': square_list,
        'layout': layout_list,
        'price_type': pricetype_list,
        'address1': addr_list1,
        'address2': addr_list2,
        'address3': addr_list3,
        'selling_status': tag_panel_list1,
        'house_type': tag_panel_list2,
        'tag': tag_list,
    }
    return data_dict
