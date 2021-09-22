# Copyright 2021 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import launch
import launch_testing

import pytest


@pytest.fixture(scope='module')
def order():
    print('once')
    yield []
    print('end')


@launch_testing.pytest.fixture(scope='module', params=['asd', 'bsd'])
def launch_description(request):
    return launch.LaunchDescription([
        launch_testing.util.KeepAliveProc(),
        launch_testing.actions.ReadyToTest(),
    ]), request.param


# TODO(ivanpauno)
# We cannot get variables from the dictionary returned by launch_description
# because we're removing the fixture before running the tests.
# Maybe we can delete this feature, and use generators/asyncgens.
# @pytest.mark.launch_testing(fixture=launch_description, shutdown=True)
# def test_after_shutdown(order, launch_service, launch_description):
#     param = launch_description[1]
#     order.append(f'test_after_shutdown[{param}]')
#     assert launch_service._is_idle()
#     assert launch_service.event_loop is None


@pytest.mark.launch_testing(fixture=launch_description)
async def test_case_1(order, launch_description):
    param = launch_description[1]
    order.append(f'test_case_1[{param}]')
    assert True


@pytest.mark.launch_testing(fixture=launch_description)
def test_case_2(order, launch_description):
    param = launch_description[1]
    order.append(f'test_case_2[{param}]')
    assert True


@pytest.mark.launch_testing(fixture=launch_description)
def test_case_3(order, launch_service, launch_description):
    param = launch_description[1]
    order.append(f'test_case_3[{param}]')
    yield
    assert launch_service._is_idle()
    assert launch_service.event_loop is None
    order.append(f'test_case_3[{param}][shutdown]')


@pytest.mark.launch_testing(fixture=launch_description)
async def test_case_4(order, launch_service, launch_description):
    param = launch_description[1]
    order.append(f'test_case_4[{param}]')
    yield
    assert launch_service._is_idle()
    assert launch_service.event_loop is None

    order.append(f'test_case_4[{param}][shutdown]')


# @pytest.mark.launch_testing
# def test_should_be_skipped():
#     assert True


def test_order(order):
    assert order == [
        'test_case_1[asd]',
        'test_case_2[asd]',
        'test_case_3[asd]',
        'test_case_4[asd]',
        # 'test_after_shutdown[asd]',
        'test_case_3[asd][shutdown]',
        'test_case_4[asd][shutdown]',
        'test_case_1[bsd]',
        'test_case_2[bsd]',
        'test_case_3[bsd]',
        'test_case_4[bsd]',
        # 'test_after_shutdown[bsd]',
        'test_case_3[bsd][shutdown]',
        'test_case_4[bsd][shutdown]',
    ]
