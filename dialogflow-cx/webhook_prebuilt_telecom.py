# Copyright 2022, Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" handle_webhook will return the correct fullfilment response depending on the tag that is sent in the request"""
# [START dialogflow_cx_v3_webhook_prebuilt_telecom]
import copy
import logging


def cxPrebuiltAgentsTelecom(request):
    logging.info("Cloud Function:" + "Invoked cloud function from Dialogflow")
    request_dict = request.get_json()

    # Get the parameters in current page
    parameter_info_list = request_dict["pageInfo"]["formInfo"]["parameterInfo"]
    parameter_dict = {}
    for parameter_info in parameter_info_list:
        key = parameter_info["displayName"]
        parameter_dict[key] = parameter_info["value"]

    # Get the tag
    tag = request_dict["fulfillmentInfo"]["tag"]

    # BEGIN detectCustomerAnomaly
    if tag == "detectCustomerAnomaly":
        logging.info(tag + " was triggered.")
        phone_number = parameter_dict["phone_number"]
        bill_state = parameter_dict["bill_state"]
        parameters = copy.deepcopy(parameter_dict)
        bill_amount = None
        product_line = None
        anomaly_detect = "false"
        purchase = "The Godfather"
        purchase_amount = 9.99
        total_bill_amount = 64.33
        bill_without_purchase = 54.34
        updated_parameters = {}

        month_name, first_of_month, last_month_name = get_date_details(bill_state)
        logging.info(month_name, first_of_month, last_month_name)

        # Getting the month name based on the bill state - current or previous
        # For example, if the current month is December, we get the values as
        # December, December 1st, November

        # Only 999999 will have anomaly detection
        if str(phone_number) == "999999":
            anomaly_detect = "true"
            product_line = "phone"
            purchase = "device protection"
            updated_parameters["product_line"] = product_line
            updated_parameters["bill_month"] = month_name
            updated_parameters["last_month"] = last_month_name

        # If bill hike amount is given - we just add it to the total bill
        if "bill_amount" in parameters:
            bill_amount = parameters["bill_amount"]
            purchase_amount = bill_amount["amount"]
            total_bill_amount = 54.34 + purchase_amount

        # Adding the updated session parameters to the new parameters json
        updated_parameters["anomaly_detect"] = anomaly_detect
        updated_parameters["purchase"] = purchase
        updated_parameters["purchase_amount"] = purchase_amount
        updated_parameters["bill_without_purchase"] = bill_without_purchase
        updated_parameters["total_bill"] = total_bill_amount
        updated_parameters["first_month"] = first_of_month

        res = {"sessionInfo": {"parameters": updated_parameters}}

    # BEGIN validatePhoneLine
    elif tag == "validatePhoneLine":
        logging.info(tag + " was triggered.")
        phone = parameter_dict["phone_number"]
        phone_line_verified = "false"
        line_index = None
        domestic_coverage = "false"
        covered_lines = ["5555555555", "5105105100", "1231231234", "9999999999"]

        # Loop over the covered lines array
        for index, line in enumerate(covered_lines):
            # For each phone line in the array, check if the last 4 digits are
            # included in the string. when true, update the line_index variable
            if phone == line:
                line_index = index
                logging.info("This is the index " + str(line_index))

        # Only 9999999999 will fail
        if line_index == 3:
            phone_line_verified = "false"
        else:
            phone_line_verified = "true"

        # Only 1231231234 will have domestic coverage
        if line_index == 2:
            domestic_coverage = "true"
        else:
            domestic_coverage = "false"

        res = {
            "sessionInfo": {
                "parameters": {
                    "phone_line_verified": phone_line_verified,
                    "domestic_coverage": domestic_coverage,
                }
            }
        }

    # BEGIN cruisePlanCoverage
    elif tag == "cruisePlanCoverage":
        logging.info(tag + " was triggered.")
        port = parameter_dict["destination"]
        port_is_covered = None
        # Sample list of covered cruise ports.
        covered_ports = [
            "mexico",
            "canada",
            "anguilla",
        ]

        if port.lower() in covered_ports:
            port_is_covered = "true"
        else:
            port_is_covered = "false"

        res = {
            "sessionInfo": {
                "parameters": {
                    "port_is_covered": port_is_covered,
                }
            }
        }

    # BEGIN internationalCoverage
    elif tag == "internationalCoverage":
        logging.info(tag + " was triggered.")
        destination = parameter_dict["destination"]
        coverage = None
        # Sample list of covered international monthly destinations.
        covered_by_monthly = [
            "anguilla",
            "australia",
            "brazil",
            "canada",
            "chile",
            "england",
            "france",
            "india",
            "japan",
            "mexico",
            "russia",
            "singapore",
        ]
        # Sample list of covered international daily destinations.
        covered_by_daily = [
            "anguilla",
            "australia",
            "brazil",
            "canada",
            "chile",
            "england",
            "france",
            "india",
            "japan",
            "mexico",
            "singapore",
        ]
        if (
            destination.lower() in covered_by_monthly
            and destination.lower() in covered_by_daily
        ):
            coverage = "both"
        elif (
            destination.lower() in covered_by_monthly
            and destination.lower() not in covered_by_daily
        ):
            coverage = "monthly_only"
        elif (
            destination.lower() not in covered_by_monthly
            and destination.lower() not in covered_by_daily
        ):
            coverage = "neither"
        else:
            # This should never happen, because covered_by_daily is a subset of
            # covered_by_monthly
            coverage = "daily_only"

        res = {
            "sessionInfo": {
                "parameters": {
                    "coverage": coverage,
                }
            }
        }

    # BEGIN cheapestPlan
    elif tag == "cheapestPlan":
        logging.info(tag + " was triggered.")
        trip_duration = parameter_dict["trip_duration"]
        monthly_cost = None
        daily_cost = None
        suggested_plan = None

        # Can only suggest cheapest if both are valid for location.

        # When trip is longer than 30 days, calculate per-month cost (example $
        # amounts). Suggest monthly plan.
        if trip_duration > 30:
            monthly_cost = (int(trip_duration / 30)) * 70
            daily_cost = trip_duration * 10
            suggested_plan = "monthly"

        # When trip is <= 30 days, but greater than 6 days, calculate monthly
        # plan cost and daily plan cost. Suggest monthly b/c it is the cheaper
        # one.
        elif trip_duration <= 30 and trip_duration > 6:
            monthly_cost = 70
            daily_cost = trip_duration * 10
            suggested_plan = "monthly"

        # When trip is <= 6 days, calculate daily plan cost. Suggest daily
        # plan.
        elif trip_duration <= 6 and trip_duration > 0:
            monthly_cost = 70
            daily_cost = trip_duration * 10
            suggested_plan = "daily"

        else:
            # This should never happen b/c trip_duration would have to be
            # negative
            suggested_plan = "null"

        res = {
            "sessionInfo": {
                "parameters": {
                    "monthly_cost": monthly_cost,
                    "daily_cost": daily_cost,
                    "suggested_plan": suggested_plan,
                }
            }
        }

    # Default Case
    else:
        res = None
        logging.info(f'{"default case called"}')

    # Returns json
    return res


# Get the current month, first day of current month and last month values
# based on today's date
def get_date_details(bill_state):
    from datetime import date
    from dateutil.relativedelta import relativedelta

    monthNames = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    today = date.today()
    # index starts with 0
    first_month_name = monthNames[(today.month - 1)]
    firstDay = today.replace(day=1)
    first_day_str = str(firstDay)

    last_month_name = monthNames[(today.month - 1) - 1]
    last_month_first_day_str = str(
        today.replace(day=1, month=(today - relativedelta(months=1)).month)
    )
    second_last_month_name = monthNames[(today.month - 1) - 2]
    if bill_state == "current":
        return [first_month_name, first_day_str, last_month_name]
    else:
        return [last_month_name, last_month_first_day_str, second_last_month_name]


# [END dialogflow_cx_v3_webhook_prebuilt_telecom]
