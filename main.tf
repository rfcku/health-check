
locals {
  owner        = "qualcom-task"
  kube_config  = "~/.kube/config"
  kube_context = "docker-desktop"
}

provider "kubernetes" {
  config_path    = local.kube_config
  config_context = local.kube_context
}

provider "helm" {
  kubernetes {
    config_path    = local.kube_config
    config_context = local.kube_context
  }
}

resource "kubernetes_namespace" "namespace" {
  metadata {
    name = local.owner
  }
}

resource "helm_release" "kafka" {
  name      = "kafka"
  chart     = "./helm/strimzi-kafka-operator-0.45.0.tgz"
  namespace = kubernetes_namespace.namespace.metadata.0.name

  set {
    name  = "replicas"
    value = 1
  }
  set {
    name  = "topics[0].name"
    value = "health_checks_topic"
  }
  depends_on = [kubernetes_namespace.namespace]
}

resource "kubernetes_manifest" "kafka-nodepool" {
  provider   = kubernetes
  manifest   = yamldecode(file("./manifest/kafka/nodepool.yml"))
  depends_on = [helm_release.kafka]
}

resource "kubernetes_manifest" "kafka-cluster" {
  provider   = kubernetes
  manifest   = yamldecode(file("./manifest/kafka/cluster.yml"))
  depends_on = [helm_release.kafka, kubernetes_manifest.kafka-nodepool]
}

resource "helm_release" "prometheus-stack" {
  name      = "prometheus-stack"
  chart     = "./helm/kube-prometheus-stack-68.3.2.tgz"
  namespace = kubernetes_namespace.namespace.metadata.0.name
}

resource "kubernetes_manifest" "kafka-app" {
  for_each = fileset("./manifest/app", "*.yml")
  manifest = yamldecode(file("./manifest/app/${each.value}"))
}

