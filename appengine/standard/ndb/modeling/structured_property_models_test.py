# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test classes for code snippet for modeling article."""

import structured_property_models as models


def test_phone_numbers(testbed):
    # Create one Contact entity with 2 phone numbers.
    scott = models.Contact(name='scott')
    scott.phone_numbers.append(
        models.PhoneNumber(phone_type='home',
                           number='(650) 555 - 2200'))
    scott.phone_numbers.append(
        models.PhoneNumber(phone_type='mobile',
                           number='(650) 555 - 2201'))
    scott.put()

    # make sure there are 2 numbers, you can expect the order is preserved.
    assert len(scott.phone_numbers) == 2
    assert scott.phone_numbers[0].phone_type == 'home'
    assert scott.phone_numbers[0].number == '(650) 555 - 2200'
    assert scott.phone_numbers[1].phone_type == 'mobile'
    assert scott.phone_numbers[1].number == '(650) 555 - 2201'

    # filer scott's phone numbers by type
    home_numbers = [phone_number for phone_number in scott.phone_numbers
                    if phone_number.phone_type == 'home']
    assert len(home_numbers) == 1
    assert home_numbers[0].number == '(650) 555 - 2200'

    # delete scott's mobile phone
    mobile_numbers = [phone_number for phone_number in scott.phone_numbers
                      if phone_number.phone_type == 'mobile']
    assert len(mobile_numbers) == 1
    lost_phone = mobile_numbers[0]
    scott.phone_numbers.remove(lost_phone)

    # Updates the entity (resending all its properties over the wire).
    scott.put()

    # make sure there's no mobile phone of scott
    scott = scott.key.get()
    assert len(scott.phone_numbers) == 1
    assert scott.phone_numbers[0].phone_type == 'home'
    assert scott.phone_numbers[0].number == '(650) 555 - 2200'
