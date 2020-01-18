from apps.db_module import models

def fcat_item(id_list):
    childs = models.Merchant.objects.filter(id__in=id_list).values('merchant__id')
    xin_list = []
    for c in childs:
        xin_list.append(c["merchant__id"])
    return xin_list

def test(id_list):
    lista = id_list
    re_list = []
    while len(lista) > 0:
        xin_list = fcat_item(lista)
        lista = xin_list
        re_list = re_list + lista
    return [i for i in re_list if i != None]


def recursive_child(id_list):
 
    if len(id_list) == 0: #是0的时候，就运算完了
        return []
    childs = models.Merchant.objects.filter(id__in=id_list).values('merchant__id')
    xin_list = []
    for c in childs:
        xin_list.append(c["merchant__id"])
    return id_list + recursive_child(xin_list) 