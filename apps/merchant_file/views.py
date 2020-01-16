from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework import status, mixins, generics, viewsets,filters
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework import filters

import uuid
import jwt
import base64
import time,datetime
import random
from django.core.cache import cache

from werkzeug.security import generate_password_hash, check_password_hash


# Create your views here.
