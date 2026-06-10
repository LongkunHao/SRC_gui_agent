#!/usr/bin/env bash
# Central configuration for all infrastructure scripts.
#
# Edit these values once — every script in infra/setup/ sources this file.
# Environment variables override any value set here.

# AWS region for all resources
MM_REGION="${AWS_REGION:-us-east-1}"

# S3 bucket for evaluation results and HTML dashboard
MM_S3_BUCKET="${MM_S3_BUCKET:-mirror-mirror-results}"

# IAM role and instance profile name attached to EC2 instances
MM_IAM_ROLE="${MM_IAM_ROLE:-mirror-mirror-ec2}"

# Security group name (SSH-only, auto-created in default VPC)
MM_SECURITY_GROUP="${MM_SECURITY_GROUP:-mm-pipeline}"

# EC2 instance type
MM_INSTANCE_TYPE="${MM_INSTANCE_TYPE:-m5.4xlarge}"

# AWS project tag used to discover/teardown instances
MM_PROJECT_TAG="${MM_PROJECT_TAG:-mirror-mirror}"
