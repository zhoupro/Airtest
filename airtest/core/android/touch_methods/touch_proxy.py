# encoding=utf-8
import warnings
from airtest.core.android.constant import TOUCH_METHOD
from airtest.utils.logger import get_logger


LOGGING = get_logger(__name__)


class TouchProxy(object):
    """
    Perform touch operation using ADB touch method
    """
    TOUCH_METHODS = {}

    def __init__(self, touch_method):
        self.touch_method = touch_method

    def __getattr__(self, name):
        if name == "method_name":
            return self.touch_method.METHOD_NAME
        method = getattr(self.touch_method, name, None)
        if method:
            return method
        else:
            raise NotImplementedError("%s does not support %s method" %
                                      (getattr(self.touch_method, "METHOD_NAME", ""), name))

    @classmethod
    def auto_setup(cls, adb, default_method=None, ori_transformer=None, size_info=None, input_event=None):
        """
        Initialize ADB touch method

        Args:
            adb: :py:mod:`airtest.core.android.adb.ADB`
            default_method: 保留参数兼容性

        Returns: TouchProxy object

        Examples:
            >>> dev = Android()
            >>> touch_proxy = TouchProxy.auto_setup(dev.adb)
            >>> touch_proxy.touch((100, 100))

        """
        # 直接使用 ADBTOUCH
        adb_touch = AdbTouchImplementation(adb)
        return TouchProxy(adb_touch)


class AdbTouchImplementation(object):
    METHOD_NAME = TOUCH_METHOD.ADBTOUCH

    def __init__(self, base_touch):
        """
        :param base_touch: :py:mod:`airtest.core.android.adb.ADB`
        """
        self.base_touch = base_touch

    def touch(self, pos, duration=0.01):
        if duration <= 0.01:
            self.base_touch.touch(pos)
        else:
            self.swipe(pos, pos, duration=duration)

    def swipe(self, p1, p2, duration=0.5, *args, **kwargs):
        duration *= 1000
        self.base_touch.swipe(p1, p2, duration=duration)

    def teardown(self):
        pass
