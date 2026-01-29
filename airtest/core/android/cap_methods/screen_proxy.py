# -*- coding: utf-8 -*-
from collections import OrderedDict
from airtest.core.error import AdbError, ScreenError
from airtest.core.android.cap_methods.base_cap import BaseCap
from airtest.utils.logger import get_logger


LOGGING = get_logger(__name__)


class ScreenProxy(object):
    """
    Perform screen operation according to the specified method
    """
    SCREEN_METHODS = OrderedDict()

    def __init__(self, screen_method):
        self.screen_method = screen_method

    def __getattr__(self, name):
        if hasattr(self.screen_method, name):
            return getattr(self.screen_method, name, None)
        elif name == "method_name":
            return self.screen_method.__class__.__name__.upper()
        else:
            raise NotImplementedError("%s does not support \'%s\' method" %
                                      (getattr(self.screen_method, "METHOD_NAME", ""), name))

    def __setattr__(self, name, value):
        if name == "screen_method":
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(self.screen_method, name, value)

    @classmethod
    def register_method(cls, name, method_class):
        cls.SCREEN_METHODS[name] = method_class

    @classmethod
    def check_frame(cls, cap_method):
        """
        Test whether a frame of image can be obtained correctly

        测试能否正确获取一帧图像

        Args:
            cap_method: :py:mod:`airtest.core.android.cap_methods.base_cap.BaseCap`

        Returns:

        """
        try:
            cap_method.get_frame()
        except (AdbError, ScreenError) as e:
            if isinstance(e, AdbError):
                LOGGING.error(repr(e.stdout))
                LOGGING.error(repr(e.stderr))
            else:
                LOGGING.error(e)
            LOGGING.error("%s setup up failed!" % cap_method.__class__.__name__)
            return False
        else:
            return True

    @classmethod
    def auto_setup(cls, adb, default_method=None, *args, **kwargs):
        """
        Initialize ADB screenshot method

        初始化 ADB 截图方法

        Args:
            adb: :py:mod:`airtest.core.android.adb.ADB`
            default_method: 保留参数兼容性

        Returns: ScreenProxy object

        Examples:
            >>> dev = Android()
            >>> screen_proxy = ScreenProxy.auto_setup(dev.adb)
            >>> screen_proxy.get_frame()

        """
        # 直接使用 ADBCAP，不再尝试其他方法
        from airtest.core.android.cap_methods.adbcap import AdbCap
        screen = AdbCap(adb, *args, **kwargs)
        if cls.check_frame(screen):
            return ScreenProxy(screen)
        # 如果 ADBCAP 不可用，抛出异常
        raise ScreenError("ADB screenshot method is not available")


def register_screen():
    # 只注册 ADBCAP 作为截图方法
    from airtest.core.android.cap_methods.adbcap import AdbCap
    ScreenProxy.SCREEN_METHODS["ADBCAP"] = AdbCap


register_screen()
