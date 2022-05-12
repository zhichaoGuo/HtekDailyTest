import time

import pytest
import allure
import yaml


#
# def setup_module():
#     print('setup_module')
#
#
# def teardown_module():
#     print('teardown_module')
#
#
# def setup_function():
#     print('setup_function')
#
#
# def teardown_function():
#     print('teardown_function')

#
# @allure.feature("测试feature")
# class TestCall:
#     f = yaml.safe_load(open("demo.yml", encoding='utf-8'))
#
#     # @pytest.mark.parametrize('mac', f["mac"])
#     # @pytest.mark.call
#     # @allure.story("ceshi story")
#     # @pytest.mark.skip
#     # def test_call1(self, mac):
#     #     # dev = queryDevice(mac)
#     #     # start_sip_tool(dev.ip,dev.port)
#     #     # call.send_invite().receive_100_trying().receive_180_ringing().send_200_OK()
#     #     print(mac)
#     #     assert mac == '00:1f:c1:1f:a8:0e'
#
#     def test_class11(self):
#         print('c1 t1')
#         assert 1
#
#     def test_class12(self):
#         print('c1 t2')
#         assert 1
#
#     def setup_class(self):
#         print('setup_class')
#
#     def teardown_class(self):
#         print('teardown_class')
#
#     def setup_method(self):
#         print('setup_method')
#
#     def teardown_method(self):
#         print('teardown_method')
#
#
# class TestClass:
#     def test_calss21(self):
#         print('class2 test1')
#         assert 1
#
#     def test_class22(self):
#         print('class2 test2')
#         assert 1
#
#
# def test_1():
#     print('1')
#     assert 1
#
#
# @pytest.mark.xfail
# def test_2():
#     print('2')
#     assert 1

#
@pytest.mark.parametrize('arg1,arg2,expected',
                         [(1, 1, 2), (2, 2, 4),
                          pytest.param(3, 3, 5,marks=pytest.mark.xfail)])
def test_add(arg1, arg2, expected):
    assert arg1 + arg2 == expected


