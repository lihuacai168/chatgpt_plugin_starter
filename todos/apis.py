# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: 花菜
# @File: apis.py.py
# @Time : 2023/7/5 23:31
# @Email: lihuacai168@gmail.com
import json
import os
from typing import List

from django.conf import settings
from django.http import FileResponse, HttpResponse, JsonResponse
from ninja import Router
from pydantic import BaseModel

router = Router()


class Todo(BaseModel):
    id: int
    task: str


_TODOS = []


@router.get("/todos", response=List[Todo])
def get_todos(request):
    return _TODOS


@router.post("/todos", response=Todo)
def add_todo(request, todo: Todo):
    _TODOS.append(todo.dict())
    return todo


@router.delete("/todos/{id}")
def delete_todo(request, id: int):
    global _TODOS
    _TODOS = [todo for todo in _TODOS if todo["id"] != id]
    return {"detail": "Todo deleted."}


@router.get("/openapi.yaml")
def openapi_spec(request):
    openapi_yaml = os.path.join(settings.BASE_DIR, "openapi.yaml")
    with open(openapi_yaml, "r", encoding="utf-8") as f:
        data = f.read()
    return HttpResponse(data, content_type="text/yaml")


# @router.get("/plugin/manifest.json")
# def plugin_manifest(request):
#     # Replace with the actual path to your manifest.json file
#     return FileResponse("/path/to/your/manifest.json")


@router.get("/plugin/logo.png")
def plugin_logo(request):
    # Replace with the actual path to your logo.png file
    logo_file_path = os.path.join(settings.BASE_DIR, "assets", "logo.png")
    with open(logo_file_path, "rb") as f:
        image_data = f.read()
    return HttpResponse(image_data, content_type="image/png")


@router.get("/.well-known/ai-plugin.json")
def plugin_manifest(request):
    ai_plugin_json = os.path.join(settings.BASE_DIR, ".well-known", "ai-plugin.json")
    with open(ai_plugin_json) as f:
        text = f.read()
    d = json.loads(text)
    return JsonResponse(d, safe=False)
