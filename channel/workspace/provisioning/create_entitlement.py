# Copyright 2021 Google LLC
#
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

# [START_EXCLUDE]
"""Google Workspace Provisioning codelab.

Instructions for this codelab can be found on this page:
https://cloud.google.com/channel/docs/codelabs/workspace/provisioning
"""
# [END_EXCLUDE]

import argparse

from google.cloud import channel
from google.cloud.channel_v1 import types
from google.cloud.channel_v1.services.cloud_channel_service.client import CloudChannelServiceClient
from google.oauth2 import service_account
from google.protobuf.any_pb2 import Any

# The maximum duration in seconds for RPCs to wait before timing out
TIMEOUT = 60


def main(account_name: str, admin_user: str, customer_domain: str, key_file: str) -> None:
    client = create_client(admin_user, key_file)

    offer = select_offer(client, account_name)

    check_exists(client, account_name, customer_domain)

    customer = create_customer(client, account_name, customer_domain)

    entitlement = create_entitlement(client, customer, offer)

    # [START channel_get_admin_sdk_customer_id]
    customer_id = customer.cloud_identity_id
    print(customer_id)
    # [END channel_get_admin_sdk_customer_id]

    suspend_entitlement(client, entitlement)

    transfer_entitlement(client, customer, entitlement)

    delete_customer(client, customer)


def create_client(admin_user: str, key_file: str) -> CloudChannelServiceClient:
    """Creates the Channel Service API client

    Returns:
      The created Channel Service API client
    """
    # [START channel_create_client]

    # Set up credentials with user impersonation
    credentials = service_account.Credentials.from_service_account_file(
      key_file, scopes=["https://www.googleapis.com/auth/apps.order"])
    credentials_delegated = credentials.with_subject(admin_user)

    # Create the API client
    client = channel.CloudChannelServiceClient(credentials=credentials_delegated)

    print("=== Created client")
    # [END channel_create_client]

    return client


def select_offer(client: CloudChannelServiceClient, account_name: str) -> types.offers.Offer:
    """Selects a Workspace offer.

    Returns:
      A Channel API Offer for Workspace
    """
    # [START channel_select_offer]
    request = channel.ListOffersRequest(parent=account_name)
    offers = client.list_offers(request)

    # For the purpose of this codelab, the code lists all offers and selects
    # the first offer for Google Workspace Business Standard on an Annual
    # plan. This is needed because offerIds vary from one account to another,
    # but this is not a recommended model for your production integration
    sample_offer = "Google Workspace Business Standard"
    sample_plan = types.offers.PaymentPlan.COMMITMENT
    selected_offer = None
    for offer in offers:
        if offer.sku.marketing_info.display_name == sample_offer and \
          offer.plan.payment_plan == sample_plan:
            selected_offer = offer
            break

    print("=== Selected offer")
    print(selected_offer)
    # [END channel_select_offer]

    return selected_offer


def check_exists(client: CloudChannelServiceClient, account_name: str, customer_domain: str) -> None:
    """Determine if customer already has a cloud identity.

    Raises:
      Exception: if the domain is already in use
    """
    # [START channel_check_exists]
    # Determine if customer already has a cloud identity
    request = channel.CheckCloudIdentityAccountsExistRequest(
      parent=account_name, domain=customer_domain)

    response = client.check_cloud_identity_accounts_exist(request)

    if response.cloud_identity_accounts:
        raise Exception(
          "Cloud identity already exists. Customer must be transferred. " +
          "Out of scope for this codelab")
    # [END channel_check_exists]


def create_customer(client: CloudChannelServiceClient, account_name: str, customer_domain: str) -> Any:
    """Create the Customer resource, with a cloud identity.

    Args:
      customer_domain: primary domain used by the customer]

    Returns:
      The created Channel API Customer
    """
    # [START channel_create_customer]
    # Create the Customer resource
    request = channel.CreateCustomerRequest(
        parent=account_name,
        customer={
            "org_display_name": "Acme Corp",
            "domain": customer_domain,
            "org_postal_address": {
                "address_lines": ["1800 Amphibious Blvd"],
                "postal_code": "94045",
                "region_code": "US"
            }
        })
    # Distributors need to also pass the following field for the `customer`
    # "channel_partner_id": channel_partner_link_id

    customer = client.create_customer(request)

    print("=== Created customer")
    print(customer)
    # [END channel_create_customer]

    # [START channel_provision_cloud_identity]
    cloud_identity_info = channel.CloudIdentityInfo(
        alternate_email="john.doe@gmail.com", language_code="en-US")

    admin_user = channel.AdminUser(
        given_name="John", family_name="Doe", email="admin@" + customer_domain)

    cloud_identity_request = channel.ProvisionCloudIdentityRequest(
        customer=customer.name,
        cloud_identity_info=cloud_identity_info,
        user=admin_user)

    # This call returns a long-running operation.
    operation = client.provision_cloud_identity(cloud_identity_request)

    # Wait for the long-running operation and get the result.
    customer = operation.result(TIMEOUT)

    print("=== Provisioned cloud identity")
    # [END channel_provision_cloud_identity]

    return customer


def create_entitlement(client: CloudChannelServiceClient, customer: types.customers.Customer, selected_offer: types.offers.Offer) -> Any:
    """Create the Channel API Entitlement.

    Args:
      customer: a Customer resource
      selected_offer: an Offer

    Returns:
      The created Entitlement
    """
    # [START channel_create_entitlement]
    request = channel.CreateEntitlementRequest(
        parent=customer.name,
        entitlement={
            "offer": selected_offer.name,
            # Setting 5 seats for this Annual offer
            "parameters": [{
                "name": "num_units",
                "value": {
                    "int64_value": 5
                }
            }],
            "commitment_settings": {
                "renewal_settings": {
                    # Setting renewal settings to auto renew
                    "enable_renewal": True,
                    "payment_plan": "COMMITMENT",
                    "payment_cycle": {
                        "period_type": "YEAR",
                        "duration": 1
                    }
                }
            },
            # A string of up to 80 characters.
            # We recommend an internal transaction ID or
            # identifier for this customer in this field.
            "purchase_order_id": "A codelab test"
        })

    # This call returns a long-running operation.
    operation = client.create_entitlement(request)

    # Wait for the long-running operation and get the result.
    entitlement = operation.result(TIMEOUT)

    print("=== Created entitlement")
    print(entitlement)
    # [END channel_create_entitlement]

    return entitlement


def suspend_entitlement(client: CloudChannelServiceClient, entitlement: types.entitlements.Entitlement) -> Any:
    """Suspend the Channel API Entitlement.

    Args:
      entitlement: an Entitlement to suspend

    Returns:
      The suspended Entitlement
    """
    # [START channel_suspend_entitlement]
    request = channel.SuspendEntitlementRequest(name=entitlement.name)

    # This call returns a long-running operation.
    operation = client.suspend_entitlement(request)

    # Wait for the long-running operation and get the result.
    result = operation.result(TIMEOUT)

    print("=== Suspended entitlement")
    print(result)
    # [END channel_suspend_entitlement]

    return result


def transfer_entitlement(client: CloudChannelServiceClient, customer: types.customers.Customer, entitlement: types.entitlements.Entitlement) -> Any:
    """Transfer the Channel API Entitlement to Google.

    Args:
      entitlement: an Entitlement to transfer

    Returns:
      google.protobuf.Empty on success
    """
    # [START channel_transfer_entitlement]
    request = channel.TransferEntitlementsToGoogleRequest(
      parent=customer.name,
      entitlements=[entitlement])

    # This call returns a long-running operation.
    operation = client.transfer_entitlements_to_google(request)

    # Wait for the long-running operation and get the result.
    result = operation.result(TIMEOUT)

    print("=== Transfered entitlement")
    print(result)
    # [END channel_transfer_entitlement]

    return result


def delete_customer(client: CloudChannelServiceClient, customer: types.customers.Customer) -> None:
    """Delete the Customer.

    Args:
      customer: a Customer to delete
    """
    # [START channel_delete_customer]
    request = channel.DeleteCustomerRequest(name=customer.name)

    client.delete_customer(request)

    print("=== Deleted customer")
    # [END channel_delete_customer]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
      description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--account_name', required=True, help='The resource name of the reseller account. Format: accounts/{account_id}.')
    parser.add_argument('--admin_user', required=True, help='The email address of a reseller domain super admin (preferably of your Test Channel Services Console).')
    parser.add_argument('--customer_domain', required=True, help='The end customer''s domain. If you run this codelab on your Test Channel Services Console, make sure the domain follows domain naming conventions.')
    parser.add_argument('--key_file', required=True, help='The path to the JSON key file generated when you created a service account.')

    args = parser.parse_args()

    main(args.account_name, args.admin_user, args.customer_domain, args.key_file)
