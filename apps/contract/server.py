from django.db import connection
from contract.models import *


class ProductDB(object):
    """产品表"""
    def query_product_list(self):
        result_db = Product.objects.filter().all()
        return result_db

    def query_product_by_id(self,id):
        result_db = Product.objects.filter(nid=id).first()
        return result_db

    def update_product(self, modify_info):
        is_exist = Product.objects.filter(product=modify_info['name']).first()
        if is_exist:
            raise Exception("该产品已存在")
        Product.objects.filter(nid=modify_info['id']).update(**modify_info)

    def insert_product(self, modify_info):
        is_exist = Product.objects.filter(name=modify_info['name']).first()
        if is_exist:
            raise Exception("该产品已存在")
        Product.objects.create(**modify_info)


class ProductMealDB(object):
    """套餐表"""
    def insert_meal(self, modify_info):
        meal_sql = """insert into product_meal(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        meal_sql = meal_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(meal_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_meal_list(self):
        result_db = ProductMeal.objects.filter().all().order_by("product_id")
        return result_db

    def query_meal_by_id(self,id):
        result_db = ProductMeal.objects.filter(nid=id).first()
        return result_db

    def query_meal_by_product(self, id):
        result_db = ProductMeal.objects.filter(product_id=id).all()
        return result_db

    def update_meal(self, modify_info):
        ProductMeal.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def multi_delete(self, id_list):
        ProductMeal.objects.filter(nid__in=id_list).delete()


class CustomerContractDB(object):
    """客户合同"""

    def insert_contract(self, modify_info):
        contract_sql = """insert into contract_info(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        contract_sql = contract_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(contract_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_contract_list(self):
        result_db = ContractInfo.objects.all().order_by("-nid")
        return result_db

    def query_approved_contract(self):
        result_db = ContractInfo.objects.filter(is_approved=1).all()
        return result_db

    def query_contract_by_belonger(self,belonger):
        result_db = ContractInfo.objects.filter(belonger_id=belonger).all().order_by("-nid")
        return result_db

    def query_contract_by_id(self, nid):
        result_db = ContractInfo.objects.filter(nid=nid).first()
        return result_db

    def query_contract_by_product(self,product_id):
        result_db = ContractInfo.objects.filter(product_id=product_id).all().order_by("-nid")
        return result_db

    def query_contract_by_customer(self,customer_id):
        result_db = ContractInfo.objects.filter(customer_id=customer_id,is_approved=1).all().order_by("-nid")
        return result_db

    def update_contract(self, modify):
        ContractInfo.objects.filter(nid=modify['nid']).update(**modify)

    def multi_delete(self, id_list, delete_status):
        ContractInfo.objects.filter(nid__in=id_list).update(**delete_status)


class ContractAttachDB(object):
    """合同附件表"""
    def query_contract_attachment_list(self):
        result_db = ContractAttach.objects.filter().all()
        return result_db

    def query_contract_attachment(self, id):
        result_db = ContractAttach.objects.filter(contract_id=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            ContractAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            ContractAttach.objects.filter(nid=item['nid']).update(**item)

    def mutil_delete_linkman_attachment(self, id_list):
        ContractAttach.objects.filter(nid__in=id_list).delete()

    def multi_delete_attach_by_linkman_id(self,id_list):
        ContractAttach.objects.filter(contract_id__in=id_list).filter().delete()

    def delete_contract_attachment(self,nid):
        ContractAttach.objects.filter(nid=nid).delete()


class ApproverDB(object):
    """合同审核人"""
    def query_approver_list(self):
        result_db = Approver.objects.all()
        return result_db

    def mutil_update(self, modify_list):
        # 更新或新增
        for item in modify_list:
            is_exist = Approver.objects.filter(approver_id=item["approver_id"])
            if is_exist:
                Approver.objects.filter(approver_id=item["approver_id"]).update(**item)
            else:
                Approver.objects.create(**item)

    def mutil_delete(self,id_list):
        Approver.objects.filter(nid__in=id_list).delete()


class ApproverResultDB(object):
    """合同审核结果"""
    def mutil_insert(self, modify_list):
        for item in modify_list:
            ApproverResult.objects.create(**item)

    def query_record_by_contract(self, contract_id):
        result_db = ApproverResult.objects.filter(contract_id=contract_id).all()
        return result_db

    def query_my_approved_result(self, cid, sid):
        result_db = ApproverResult.objects.filter(contract_id=cid, approver_id=sid).first()
        return result_db


class ApproverRecordDB(object):
    """合同审核记录"""
    def insert_record(self,modify):
        ApproverRecord.objects.create(**modify)

    def query_my_record(self,result_id):
        result_db = ApproverRecord.objects.filter(result_id=result_id).all()
        return result_db

product_db = ProductDB()
product_meal_db = ProductMealDB()
contract_db = CustomerContractDB()
contract_attach_db = ContractAttachDB()
approver_db = ApproverDB()
approver_result_db = ApproverResultDB()
app_record_db=ApproverRecordDB()