terraform {
  required_providers {
    civo = {
      source = "civo/civo"
      version = "0.10.3"
    }
  }
}

variable "TOKEN" {
  type = string
}


provider "civo" {
  token = var.TOKEN
  region = "LON1"
}

resource "civo_kubernetes_cluster" "my-cluster" {
    name = "test"
    region = "LON1"
    applications = "Rancher"
    num_target_nodes = 3
    target_nodes_size = "g3.k3s.xsmall"
}
