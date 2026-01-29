# -*- coding: utf-8 -*-
import os
import time
import threading
import traceback
from airtest.utils.snippet import reg_cleanup, is_exiting, on_method_ready
from airtest.utils.logger import get_logger
from airtest.core.android.constant import ORI_METHOD
LOGGING = get_logger(__name__)


class RotationWatcher(object):
    """
    RotationWatcher class - now uses ADB method only
    """

    def __init__(self, adb, ori_method=ORI_METHOD.ADB):
        self.adb = adb
        self.ow_callback = []
        self.ori_method = ori_method
        self._t = None
        self._t_kill_event = threading.Event()
        self.current_orientation = None
        reg_cleanup(self.teardown)

    @on_method_ready('start')
    def get_ready(self):
        pass

    def install(self):
        """
        RotationWatcher uses ADB method, no installation needed

        Returns:
            None

        """
        # RotationWatcher now uses ADB method, no JAR file needed
        pass

    def uninstall(self):
        """
        Uninstall RotationWatcher package

        Returns:
            None

        """
        # RotationWatcher now uses ADB method, no JAR file to uninstall
        pass

    def teardown(self):
        self._t_kill_event.set()
        self.ow_callback = []
        setattr(self, "_start_ready", None)

    def start(self):
        """
        Start the RotationWatcher daemon thread

        Returns:
            initial orientation

        """
        # RotationWatcher now always uses ADB method
        self.ori_method = ORI_METHOD.ADB

        def _refresh_by_adb():
            ori = self.adb.getDisplayOrientation()
            return ori

        def _run(kill_event):
            while not kill_event.is_set():
                ori = _refresh_by_adb()
                if self.current_orientation == ori:
                    time.sleep(3)
                    continue
                    
                if ori is not None:
                    LOGGING.info('update orientation %s->%s' % (self.current_orientation, ori))
                    self.current_orientation = ori
                    if is_exiting():
                        self.teardown()
                    for cb in self.ow_callback:
                        try:
                            cb(ori)
                        except:
                            LOGGING.error("cb: %s error" % cb)
                            traceback.print_exc()

        self.current_orientation = _refresh_by_adb()

        self._t = threading.Thread(target=_run, args=(self._t_kill_event, ), name="rotationwatcher")
        self._t.daemon = True
        self._t.start()

        return self.current_orientation

    def reg_callback(self, ow_callback):
        """
        Register callback for orientation changes

        Args:
            ow_callback: callback function

        Returns:
            None

        """
        """方向变化的时候的回调函数，参数一定是ori，如果断掉了，ori传None"""
        if ow_callback not in self.ow_callback:
            self.ow_callback.append(ow_callback)


class XYTransformer(object):
    """
    transform the coordinates (x, y) by orientation (upright <--> original)
    """
    @staticmethod
    def up_2_ori(tuple_xy, tuple_wh, orientation):
        """
        Transform the coordinates upright --> original

        Args:
            tuple_xy: coordinates (x, y)
            tuple_wh: screen width and height
            orientation: orientation

        Returns:
            transformed coordinates (x, y)

        """
        x, y = tuple_xy
        w, h = tuple_wh

        if orientation == 1:
            x, y = w - y, x
        elif orientation == 2:
            x, y = w - x, h - y
        elif orientation == 3:
            x, y = y, h - x
        return x, y

    @staticmethod
    def ori_2_up(tuple_xy, tuple_wh, orientation):
        """
        Transform the coordinates original --> upright

        Args:
            tuple_xy: coordinates (x, y)
            tuple_wh: screen width and height
            orientation: orientation

        Returns:
            transformed coordinates (x, y)

        """
        x, y = tuple_xy
        w, h = tuple_wh

        if orientation == 1:
            x, y = y, w - x
        elif orientation == 2:
            x, y = w - x, h - y
        elif orientation == 3:
            x, y = h - y, x
        return x, y