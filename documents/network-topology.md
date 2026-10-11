# Network Topology

## VPC layout
One production VPC (`10.20.0.0/16`) in a single AWS region, spread across three availability zones.
- **Public subnets** (one per zone): Application Load Balancer and NAT gateways.
- **Private application subnets**: EKS worker nodes.
- **Private data subnets**: RDS, ElastiCache, MSK, Elasticsearch. Only reachable from application subnets.

## Traffic rules
- Inbound internet traffic reaches only the load balancer and CloudFront.
- Nodes reach the internet through one NAT gateway per zone (see the NAT gateway runbook).
- VPC endpoints for S3, ECR, Secrets Manager and CloudWatch keep that traffic off the NAT gateway.
- Security groups are defined per service in Terraform; data stores accept connections only from the security groups of the services that need them.

## DNS
- Public zones in Route 53 (`www`, `api`, `m`).
- Private hosted zone `internal` for data stores (for example `orders-db.internal`).
- Inside the cluster, CoreDNS resolves `*.svc.cluster.local` and forwards everything else to the VPC resolver.

## Connectivity to the corporate network
The admin portal and internal tools are reachable only through the corporate VPN via a separate internal load balancer.
