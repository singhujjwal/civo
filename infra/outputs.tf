output "domain_output" {
  value = data.civo_dns_domain_name.domain.name
}

output "domain_id_output" {
  value = data.civo_dns_domain_name.domain.id
}

output "instance_sizes" {
  value = data.civo_instances_size.large.sizes
}


output "kubeconfig" {
  value = civo_kubernetes_cluster.my-cluster.kubeconfig
}


