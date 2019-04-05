# DNS setup


There are two ways to setup your DNS:

 - Using your root DNS project to manage your domains
 - Using delegation, to smaller DNS projects

In this document, we will teach you both ways, so you can choose what fits better for you.

##Prerequisites

Before you start, you will need:

 - An domain already created
 - A DNS project with a managed zone, you can follow [this](https://cloud.google.com/dns/quickstart) documentation to create
 - Roles

## 1 - One zone, one DNS project

This step assumes that you already have a DNS project with a Managed Zone configured on this project.

## 1.1 - Setup variables

```bash
export dns_zone="gcpsecdemo"
export dns_project_id="gcpsec-dns-control"
export main_domain="googlecloudsecuritydemo.com"
export new_domain="cscc-qb".main_domain
export EXTERNAL_IP=<load_balancer_ip>
```

## 1.2 - Use your account with roles

```bash
gcloud config set account <your_account>
```

## 1.3 - Enable dns

```bash
gcloud services enable dns.googleapis.com --project $dns_project_id
```

 ## 1.4.1 - Add your A record pointing the URL to your IP

```bash
# start dns transaction
gcloud dns record-sets transaction start \
-z=${dns_zone_name} \
--project ${dns_project_id}

# update a record
gcloud dns record-sets transaction add \
--zone ${dns_zone_name} \
--ttl 300 \
--name "${custom_domain}." \
--type A "${EXTERNAL_IP}"

# execute dns transaction
gcloud dns record-sets transaction execute \
-z=${dns_zone_name} \
--project ${dns_project_id}
```

## 2 Delegating zones

This step assumes that you already have a DNS project with a Managed Zone configured on this project. This example consider 3 levels.

## 1.1 - Setup variables

```bash
export root_dns_project_id=gcpsec-dns-control
export root_dns_zone_name=gcpsecdemo
export dns_project_id=dev-gcpsec-dns-control
export dashless_domain="dashless.googlecloudsecuritydemo.com"
export querybuilder_domain="querybuilder.${dashless_domain}"
export dashless_dns_zone="dashless-gcp-sec"
export querybuilder_dns_zone="qbdashless-gcp-sec"
```

## 2.2 - Use account with roles for your low level project

```bash
gcloud config set account <your_account>
```

## 10.3 - Enable dns

```bash
gcloud services enable dns.googleapis.com --project $dashless_dns_zone
```

## 2.4 - Setup dashless

## 2.4.1 - Create dashless zone

```bash
gcloud dns managed-zones create \
--dns-name="${dashless_domain}." \
--description="${dashless_domain} A zone" \
"${dashless_dns_zone}" \
--project ${dns_project_id}
```

## 2.4.2 - Retrieve nameservers for dashless zone

```bash
gcloud dns managed-zones describe "${dashless_dns_zone}" \
--project ${dns_project_id}
```

## 2.5 - Setup NS delegation of dashless on root domain

## 2.5.1 - Use account with roles for the project with the main zone

```bash
gcloud config set account <your_account>
```

## 2.5.2 - Delegate nameserver

```bash
export ns_prefix="ns-cloud-b"
# start dns transaction
gcloud dns record-sets transaction start \
-z=${root_dns_zone_name} \
--project ${root_dns_project_id}

# update add nameserver record
gcloud dns record-sets transaction add \
--zone ${root_dns_zone_name} \
--ttl 300 \
--name "${dashless_domain}." \
--type NS \
"${ns_prefix}1.googledomains.com." \
"${ns_prefix}2.googledomains.com." \
"${ns_prefix}3.googledomains.com." \
"${ns_prefix}4.googledomains.com."

# execute dns transaction
gcloud dns record-sets transaction execute \
-z=${root_dns_zone_name} \
--project ${root_dns_project_id}
```

## 2.6 - Setup NS delegation on dashless domain

## 2.6.1 - Use joonix net account

```bash
gcloud config set account joaog@gcp-sec-demo-org.joonix.net
```

## 2.6.2 - Create querybuilder zone

```bash
gcloud dns managed-zones create \
--dns-name="${querybuilder_domain}." \
--description="${querybuilder_domain} A zone" \
"${querybuilder_dns_zone}" \
--project ${dns_project_id}
```

## 2.6.3 - Retrieve DNS nameservers

```bash
gcloud dns managed-zones describe "${querybuilder_dns_zone}" \
--project ${dns_project_id}
```

## 2.6.4 - Setup NS delegation on dashless domain

```bash
export ns_prefix="ns-cloud-c"
# start dns transaction
gcloud dns record-sets transaction start \
-z=${dashless_dns_zone} \
--project ${dns_project_id}

# update add nameserver record
gcloud dns record-sets transaction add \
--zone ${dashless_dns_zone} \
--ttl 300 \
--name "${querybuilder_domain}." \
--type NS \
"${ns_prefix}1.googledomains.com." \
"${ns_prefix}2.googledomains.com." \
"${ns_prefix}3.googledomains.com." \
"${ns_prefix}4.googledomains.com."

# execute dns transaction
gcloud dns record-sets transaction execute \
-z=${dashless_dns_zone} \
--project ${dns_project_id}
```