aws_region     = "eu-central-1"
aws_account_id = "111122223333"
db_identifier  = "customer-prod"

# Target key after annual rotation. Applying this change forces RDS replacement
# because aws_db_instance.kms_key_id is a ForceNew attribute.
kms_key_id = "arn:aws:kms:eu-central-1:111122223333:key/aaaaaaaa-bbbb-cccc-dddd-000000000002"

engine         = "postgres"
engine_version = "15.4"
instance_class = "db.r6g.large"
