import json
import os
import uuid
from django.core import serializers
from django.shortcuts import render, HttpResponse
from task.forms.form import TaskForm, PerformForm
from .server import task_db, task_tag_db, task_attachment_db,task_review_db,staff_db,performence_db
from .utils import build_attachment_info, build_tags_info, build_reviewer_info, compare_json

# Create your views here.


def task_assign(request):

    tid = request.GET.get("tid", None)
    query_sets = task_db.query_task_by_tid(tid)

    return render(request, "task/task_assign.html", {"query_sets": query_sets})

def task_search(request):
    filters = request.GET
    task_type_id = int(filters.get("s", 0))
    # 根据分类和关键字去筛选
    if task_type_id > 0:
        # 先根据分类去筛选
        query_sets = task_db.query_task_by_type(task_type_id)
    else:
        query_sets=task_db.query_task_lists()
    return render(request, "task/task_assign_center.html", {"query_sets": query_sets, 'task_type_id': task_type_id})


def task_detail(request):
    tid = request.GET.get("tid", None)
    if tid:
        query_sets = task_db.query_task_by_tid(tid)
        return render(request, 'task/task_detail.html', {"query_sets": query_sets})


def publish_task(request):
    method = request.method
    if method == "GET":
        return render(request, "task/task_edit.html", {"tid": 0})
    else:
        ret = {"status": False, "data": "", "message": ""}
        form = TaskForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            # 获取标签并删除
            tags = data.get("tags", None)
            tag_list = tags.split("|")
            data.pop("tags")
            # 获取附件并删除
            attachment = data.get("attachment", None)
            data.pop("attachment")
            # 获取审核人并删除
            reviewers = data.get("reviewers", None)
            data.pop("reviewers")
            if data:
                try:
                    tid = task_db.insert_task(data)
                    # 如果任务插入成功
                    if tid:
                        # 插入标签
                        tags_list = build_tags_info(tid, tag_list)
                        task_tag_db.mutil_insert_tag(tags_list)
                        # 插入附件
                        attachment_list = build_attachment_info(tid, attachment)
                        task_attachment_db.mutil_insert_attachment(attachment_list)
                        # 插入审核人
                        reviewers_list = build_reviewer_info(tid, reviewers)
                        task_review_db.mutil_insert_reviewer(reviewers_list)
                        ret["status"] = True
                except Exception as e:
                    print(e)
                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def task_edit(request):
    method = request.method
    if method == "GET":
        tid = request.GET.get("tid", None)
        if tid:
            # 获取任务信息及其标签信息、附件信息、审核人
            task_info = task_db.query_task_by_tid(tid)
            task_tag_info = task_tag_db.query_task_tag_by_tid(tid)
            task_attachment_info = task_attachment_db.query_task_attachment_by_tid(tid)
            task_reviewer_info = task_review_db.query_task_reviewer_by_tid(tid)
            return render(request, 'task/task_edit.html',
                      {"tid": tid,
                       "task_info": task_info,
                       "task_tag_info": task_tag_info,
                       "task_attachment_data": task_attachment_info,
                       "task_reviewer_info": task_reviewer_info}
                          )
        return HttpResponse(json.dumps({"status": "False", "message": "找不到相关信息"}))
    else:
        ret = {"status": False, "data": "", "message": ""}
        form = TaskForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            #获取任务id
            tid=data.get("tid", None)
            # 获取标签并删除
            tags = data.get("tags", None)
            data.pop("tags")
            tag_list = list(json.loads(tags))
            # 获取附件并删除
            attachment = data.get("attachment", None)
            data.pop("attachment")
            attachment_list = list(json.loads(attachment))
            # 获取审核人并删除
            reviewers = data.get("reviewers", None)
            reviewers_list = list(json.loads(reviewers))
            data.pop("reviewers")
            if tid:
                try:
                    # 更新任务
                    task_db.update_task(data)
                    # 更新标签
                    tags_record = task_tag_db.query_task_tag_by_tid(tid)
                    # 数据对比
                    insert_tag, update_tag, delete_tag_id = compare_json(tags_record, tag_list, "ttid")
                    if insert_tag:
                        task_tag_db.mutil_insert_tag(insert_tag)
                    if update_tag:
                        task_tag_db.mutil_update_tag(update_tag)
                    if delete_tag_id:
                        task_tag_db.mutil_delete_tag(delete_tag_id)
                    # 更新附件
                    att_record = task_attachment_db.query_task_attachment_by_tid(tid)
                    # 数据对比
                    insert_att, update_att, delete_id_att = compare_json(att_record, attachment_list, "tamid")
                    if insert_att:
                        task_attachment_db.mutil_insert_attachment(insert_att)
                    if update_att:
                        task_attachment_db.mutil_update_attachment(update_att)
                    if delete_id_att:
                        task_attachment_db.mutil_delete_task_attachment(delete_id_att)
                    # 更新审核人
                    reviewer_record = task_review_db.query_task_reviewer_by_tid(tid)
                    insert_review, update_review, delete_id_review = compare_json(reviewer_record, reviewers_list, 'sid')
                    if insert_review:
                        task_review_db.mutil_insert_reviewer(insert_review)
                    if update_review:
                        task_review_db.mutil_update_reviewer(update_review)
                    if delete_id_review:
                        task_review_db.mutil_delete_reviewer(delete_id_review)
                    ret['status'] = True
                except Exception as e:
                    print(e)
                    ret["message"] = False
        return HttpResponse(json.dumps(ret))


def task_delete(request):
    ret={'status': '', "data": "","message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        # 删除任务
        task_db.multi_delete_task(id_list)
        # 删除附件
        task_attachment_db.multi_delete_attach_by_tid(id_list)
        # 删除标签
        task_tag_db.mutil_delete_tag_by_tid(id_list)
        ret['status'] = True
    except Exception as e:
        print(e)
        ret["message"] = "删除失败"
    return HttpResponse(json.dumps(ret))


def department_staff(request):
    ret = {"status": False, "data": '',"message": ''}
    dpid = request.POST.get("dpid", None)
    if dpid:
        try:
            dp_staff_list = staff_db.query_staff_by_department_id(dpid)
            # 序列化queryset对象
            dp_staff_list = serializers.serialize("json", dp_staff_list)
            ret['status'] = True
            ret["data"] = dp_staff_list
        except Exception as e:
            ret["message"] = "出错了"
    else:
        ret["message"] = "请选择相应的部门"
    return HttpResponse(json.dumps(ret))


def attachment_upload(request):
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    try:
        # 获取文件对象
        file_obj = request.FILES.get("file")
        raw_name = file_obj.name
        if not file_obj:
            pass
        else:
            file_name = str(uuid.uuid4())
            file_path = os.path.join("static/upload/task", file_name)
            with open(file_path, "wb") as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
            ret["status"] = True
            ret["data"]['path'] = file_path
            ret["data"]['name'] = raw_name
    except Exception as e:
        ret["summary"] = str(e)
    return HttpResponse(json.dumps(ret))


def performence_display(request):
    query_sets = performence_db.query_performence_list()

    return render(request, "task/performence.html", {"query_sets": query_sets})


def performence_edit(request):
    method = request.method
    print(method)
    if method == "GET":
        pid = request.GET.get("pid", None)
        # 有则为编辑 ,无则添加
        if pid:
            performence_obj = performence_db.query_performence_by_pid(pid)
        else:
            pid = 0
            performence_obj = []
        return render(request, 'task/performence_edit.html', {"performence_obj": performence_obj, "pid": pid})
    else:
        form = PerformForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            pid = request.POST.get("pid", None)
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if pid:
                print(pid)
                try:
                    performence_db.update_performence(data)
                    ret['status'] = True
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
            else:
                try:
                    performence_db.insert_performence(data)
                    ret['status'] = True
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
        else:

            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))

def performence_delete(request):
    ret = {'status': '', "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        performence_db.mutil_delete_performence(id_list)
        ret['status']=True
    except Exception as e:
        print(e)
        ret['message'] = '删除失败'
    return HttpResponse(json.dumps(ret))