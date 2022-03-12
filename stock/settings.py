#encoding=utf-8

"""
Django settings for stock project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = '/root/zzystock/'



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mg9b1ixn6r&+_@su)_r(qbsr6i5if86*^x0l$ui+lqu+f+&xof'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'st_pool',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'st_pool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'stock.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

#本地数据库
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'stock',
#         'USER': 'root',
#         'PASSWORD': 'lg',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#     }
# }

# 阿里云数据库
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'stock',
#         'USER': 'root',
#         'PASSWORD': 'taobaoke',
#         'HOST': '123.56.231.34',
#         'PORT': '3306',
#     }
# }

#create database stock charset=utf8;


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'


STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'static')

]
#add by zzy   引用  js ,  或者 css   https://www.cnblogs.com/zhzhang/p/6973813.html
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = (
#     ('css', os.path.join(STATIC_ROOT, 'css').replace('\\', '/')),
#     ('js', os.path.join(STATIC_ROOT, 'js').replace('\\', '/')),
#     ('images', os.path.join(STATIC_ROOT, 'images').replace('\\', '/')),
# )

#logging
BASE_LOG_DIR = os.path.join(BASE_DIR, "stock/log")

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename=BASE_LOG_DIR + '/fund.log',
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )

