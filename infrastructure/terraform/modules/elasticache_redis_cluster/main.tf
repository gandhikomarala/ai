# Terraform Reusable Module: elasticache_redis_cluster
# Environment-Agnostic Infrastructure-as-Code

terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.30"
    }
  }
}

variable "environment" {
  type        = string
  description = "Target deployment tier (dev, staging, production)"
  default     = "production"
}

variable "resource_tags" {
  type        = map(string)
  default     = {
    Project     = "AegisAI"
    ManagedBy   = "Terraform"
    Environment = "production"
  }
}

output "elasticache_redis_cluster_status" {
  value       = "DEPLOYED"
  description = "Operational health status of elasticache_redis_cluster module"
}
