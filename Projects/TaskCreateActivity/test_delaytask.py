# SPDX-FileCopyrightText: 2021-2022 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: CC0-1.0

import pytest
from pytest_embedded import Dut

@pytest.mark.esp32s3
@pytest.mark.generic
def test_basic_expect(dut: Dut):
    dut.expect('HOLA\n',timeout=10)
