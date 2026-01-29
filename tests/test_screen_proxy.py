# encoding=utf-8
from airtest.core.android.android import Android
from airtest.core.android.cap_methods.screen_proxy import ScreenProxy
from airtest.aircv.utils import string_2_img
from numpy import ndarray
import unittest
import warnings
warnings.simplefilter("always")


class TestScreenProxy(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dev = Android()
        cls.dev.rotation_watcher.get_ready()

    def test_setup(self):
        # 测试默认的初始化
        screen_proxy = ScreenProxy.auto_setup(self.dev.adb,
                                              rotation_watcher=self.dev.rotation_watcher,
                                              display_id=self.dev.display_id,
                                              ori_function=lambda: self.dev.display_info)
        self.assertIsNotNone(screen_proxy)
        screen_proxy.teardown_stream()

    def test_snapshot(self):
        # 只测试 ADBCAP 方法
        cap_method = ScreenProxy.SCREEN_METHODS["ADBCAP"](self.dev.adb)
        screen_proxy = ScreenProxy(cap_method)
        img = screen_proxy.snapshot()
        self.assertIsInstance(img, ndarray)
        screen_proxy.teardown_stream()

    def test_cap_method(self):
        # 只支持 ADBCAP
        self.assertIn("ADBCAP", ScreenProxy.SCREEN_METHODS.keys())

    @classmethod
    def tearDownClass(cls):
        cls.dev.rotation_watcher.teardown()
