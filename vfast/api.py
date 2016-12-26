# encoding: utf8
import hashlib
from django.shortcuts import redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import logging, logging.handlers
import time, os, json
from settings import *


def encry_password(password, salt='salt'):
    string = password+salt
    return hashlib.new('md5',string).hexdigest()


def auth_login(func):
    def wrapper(request, *args, **kwargs):
        try:
            username = request.session.get('username', None)
            if not username:
                return redirect('/login/')
            return func(request, *args, **kwargs)
        except:
            pass
    return wrapper


def require_role(role='1'):
    def _deco(func):
        def __deco(request, *args, **kwargs):
            request.session['pre_url'] = request.path
            if role != request.session['role']:
                return HttpResponse(json.dumps({'errmsg': '权限不够'},ensure_ascii=False))
            return func(request, *args, **kwargs)
        return __deco
    return _deco


def auth_login(func):
    def inner(request, *args, **kwargs):
        role = request.session.get('role', None)
        if not role:
            return redirect('/login/')
        return func(request, *args, **kwargs)
    return inner


class ConcurrentDayRotatingFileHandler(logging.handlers.BaseRotatingHandler):
    def __init__(self, filename, encoding=None, delay=False):
        logging.handlers.BaseRotatingHandler.__init__(self, filename, 'a', encoding, delay)
        self.day = time.strftime('%Y-%m-%d', time.localtime())

    def shouldRollover(self, record):
        now_day = time.strftime('%Y-%m-%d', time.localtime())
        if self.stream is None:
            self.stream = self._open()
        if now_day == self.day:
            return False
        return True

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        rotate_log = "%s.%s" % (self.baseFilename, self.day)
        if not os.path.exists(rotate_log):
            os.rename(self.baseFilename, rotate_log)
        self.day = time.strftime('%Y-%m-%d', time.localtime())

        if not self.delay:
            self.stream = self._open()


def set_logging(log_path, log_level='error'):
    def add_handler(log_name, formatter, level, logger=None):
        if not logger:
            return
        log_handler = ConcurrentDayRotatingFileHandler(log_name)
        log_formatter = logging.Formatter(formatter)
        log_handler.setFormatter(log_formatter)
        logger.addHandler(log_handler)
        logger.setLevel(level)

    LOG_LEVELS = {
                  'critical': logging.CRITICAL, 'error': logging.ERROR,
                  'warning': logging.WARNING, 'info': logging.INFO,
                  'debug': logging.DEBUG
                 }

    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    log_name = os.path.join(log_path, 'record.log')
    logger = logging.getLogger('record')
    formatter = '%(message)s'
    add_handler(log_name, formatter, logging.DEBUG, logger)

    log_name = os.path.join(log_path, 'service.log')
    logger = logging.getLogger()
    formatter = '%(asctime)s %(levelname)s %(process)d %(thread)d %(filename)s-%(funcName)s:%(lineno)d %(message)s'
    add_handler(log_name, formatter, LOG_LEVELS.get(log_level.lower(), logging.ERROR), logger)


def write_log(user, msg):
    logging.getLogger('record').debug('%s %s %s' % (int(time.time()), user, msg))

