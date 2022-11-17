#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# flake8: noqa

# <IMPORTS/>


# <INGREDIENT create_firewall_rule />

# <INGREDIENT delete_firewall_rule />

# <INGREDIENT get_firewall_rule />

# <INGREDIENT list_firewall_rules />

# <INGREDIENT patch_firewall_priority />

if __name__ == "__main__":
    import google.auth
    import google.auth.exceptions

    try:
        default_project_id = google.auth.default()[1]
        print(f"Using project {default_project_id}.")
    except google.auth.exceptions.DefaultCredentialsError:
        print(
            "Please use `gcloud auth application-default login` "
            "or set GOOGLE_APPLICATION_CREDENTIALS to use this script."
        )
    else:
        import uuid

        rule_name = "firewall-sample-" + uuid.uuid4().hex[:10]
        print(f"Creating firewall rule {rule_name}...")
        # The rule will be created with default priority of 1000.
        create_firewall_rule(default_project_id, rule_name)
        try:
            print("Rule created:")
            print(get_firewall_rule(default_project_id, rule_name))
            print("Updating rule priority to 10...")
            patch_firewall_priority(default_project_id, rule_name, 10)
            print("Rule updated: ")
            print(get_firewall_rule(default_project_id, rule_name))
            print(f"Deleting rule {rule_name}...")
        finally:
            delete_firewall_rule(default_project_id, rule_name)
        print("Done.")
