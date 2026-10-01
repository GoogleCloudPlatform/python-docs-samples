# Google Cloud VPC: Get Google APIs and Services IP Ranges

This sample shows how to retrieve Google's public IP range feeds and compute the IP address ranges (CIDRs) used exclusively for Google APIs and default domain services (such as `*.googleapis.com`).

It calculates the IP set difference `(goog.json - cloud.json)` to separate default Google API domains from customer Google Cloud resource IPs, which is useful for configuring VPC firewall rules, custom routing, and [Private Google Access](https://cloud.google.com/vpc/docs/private-google-access).

## Setup

1. Create and activate a Python virtual environment:

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

2. Install the dependencies needed to run the sample:

    ```bash
    pip install -r requirements.txt
    ```

## How to Run

Run the sample script directly with Python:

```bash
python get_google_ip_ranges.py
```

### Example Output

```text
Fetched https://www.gstatic.com/ipranges/goog.json (published: 2026-08-11T13:04:46.50592)
Fetched https://www.gstatic.com/ipranges/cloud.json (published: 2026-08-11T13:04:46.50592)
IP ranges for Google APIs and services default domains:
8.8.4.0/24
8.8.8.0/24
8.35.200.0/21
...
2600:1900::/34
2600:1901:1::/48
```

## Testing

### Run Tests with Pytest

1. Install test dependencies:

    ```bash
    pip install -r requirements-test.txt
    ```

2. Run the test suite:

    ```bash
    pytest
    ```

### Run Tests and Linting with Nox

This sample uses [Nox](https://github.com/wntrblm/nox) for automated testing and linting.

1. Install `nox`:

    ```bash
    pip install nox
    ```

2. Run code style linting:

    ```bash
    nox -s lint
    ```

3. Run code formatting with Black:

    ```bash
    nox -s blacken
    ```

4. Run tests against a specific Python version:

    ```bash
    nox -s py-3.13
    ```

## References

* [Google Cloud Sample Authoring Guide](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/AUTHORING_GUIDE.md)
* [Private Google Access Configuration](https://cloud.google.com/vpc/docs/configure-private-google-access#ip-addr-defaults)
* [Google IP Address Ranges](https://cloud.google.com/vpc/docs/private-google-access#ip-addr-defaults)