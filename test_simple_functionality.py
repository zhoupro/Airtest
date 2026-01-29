#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单的功能测试 - 验证截图和触摸功能
使用模拟对象进行测试，无需实际设备
"""

import unittest
from unittest.mock import Mock, patch
import tempfile
import os


class TestSimpleFunctionality(unittest.TestCase):
    """简单功能测试"""

    def test_screenshot_functionality(self):
        """测试截图功能"""
        from airtest.core.android.cap_methods.adbcap import AdbCap
        
        # 创建模拟的 ADB 对象
        mock_adb = Mock()
        mock_adb.snapshot.return_value = b"fake_screenshot_data"
        
        # 创建 ADBCAP 实例
        adbcap = AdbCap(mock_adb)
        
        # 测试获取截图
        frame = adbcap.get_frame()
        self.assertIsNotNone(frame)
        
        # 验证 ADB snapshot 被调用
        mock_adb.snapshot.assert_called_once()

    def test_touch_functionality(self):
        """测试触摸功能"""
        from airtest.core.android.touch_methods.touch_proxy import AdbTouchImplementation
        
        # 创建模拟的 ADB 对象
        mock_adb = Mock()
        
        # 创建 ADBTOUCH 实现
        adb_touch = AdbTouchImplementation(mock_adb)
        
        # 测试触摸
        adb_touch.touch((100, 200))
        
        # 验证 ADB touch 被调用
        mock_adb.touch.assert_called_once_with((100, 200))
        
        # 测试滑动
        adb_touch.swipe((100, 200), (300, 400), duration=1.0)
        
        # 验证 ADB swipe 被调用
        mock_adb.swipe.assert_called_once_with((100, 200), (300, 400), duration=1000.0)

    def test_touch_proxy_auto_setup(self):
        """测试 TouchProxy 自动设置"""
        from airtest.core.android.touch_methods.touch_proxy import TouchProxy
        
        # 创建模拟的 ADB 对象
        mock_adb = Mock()
        
        # 测试自动设置
        touch_proxy = TouchProxy.auto_setup(mock_adb)
        
        # 验证返回的是 TouchProxy 实例
        self.assertIsInstance(touch_proxy, TouchProxy)
        
        # 验证方法名称
        self.assertEqual(touch_proxy.method_name, "ADBTOUCH")

    def test_screen_proxy_auto_setup(self):
        """测试 ScreenProxy 自动设置"""
        from airtest.core.android.cap_methods.screen_proxy import ScreenProxy
        
        # 创建模拟的 ADB 对象
        mock_adb = Mock()
        mock_adb.snapshot.return_value = b"fake_data"
        
        # 测试自动设置
        screen_proxy = ScreenProxy.auto_setup(mock_adb)
        
        # 验证返回的是 ScreenProxy 实例
        self.assertIsInstance(screen_proxy, ScreenProxy)
        
        # 验证方法名称
        self.assertEqual(screen_proxy.method_name, "ADBCAP")

    def test_adb_cap_snapshot(self):
        """测试 ADBCAP 快照功能"""
        from airtest.core.android.cap_methods.adbcap import AdbCap
        from airtest.core.android.constant import SDK_VERISON_ANDROID7
        from airtest import aircv
        
        # 创建模拟的 ADB 对象
        mock_adb = Mock()
        mock_adb.sdk_version = SDK_VERISON_ANDROID7 + 1  # 高于 Android 7
        mock_adb.snapshot.return_value = b"fake_screenshot_data"
        
        # 模拟 aircv.utils.string_2_img 返回值
        with patch('airtest.core.android.cap_methods.adbcap.aircv.utils.string_2_img') as mock_string_2_img:
            mock_image = Mock()
            mock_string_2_img.return_value = mock_image
            
            # 创建 ADBCAP 实例
            adbcap = AdbCap(mock_adb)
            
            # 测试快照
            snapshot = adbcap.snapshot()
            self.assertIs(mock_image, snapshot)
            
            # 验证被调用
            mock_adb.snapshot.assert_called_once()
            mock_string_2_img.assert_called_once_with(b"fake_screenshot_data")


if __name__ == '__main__':
    unittest.main()