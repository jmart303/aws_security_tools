import get_aws_data

'''
security data for aws roles
'''


def audit_role_data(logger):
    security_role_audit_config = get_aws_data.GetRoles('security_audit', logger)
    security_audit_role = security_role_audit_config.get_role()
    audit_role_config = get_aws_data.GetRoles('audit', logger)
    audit_role = audit_role_config.get_role()
    role_session_name = "AssumeRoleAuditSession"
    audit_credential_data = {
        'security_audit_role': security_audit_role,
        'audit_role': audit_role,
        'role_session_name': role_session_name

    }
    return audit_credential_data


def enforce_role_data(logger):
    security_enforce_role_config = get_aws_data.GetRoles('security_enforce', logger)
    security_enforce_role = security_enforce_role_config.get_role()
    enforce_role_config = get_aws_data.GetRoles('enforce', logger)
    enforce_role = enforce_role_config.get_role()
    role_session_name = "AssumeRoleEnforceSession"
    enforce_credential_data = {
        'security_enforce_role': security_enforce_role,
        'enforce_role': enforce_role,
        'role_session_name': role_session_name

    }
    return enforce_credential_data


def ir_enforce_role_data(logger):
    security_ir_role_config = get_aws_data.GetRoles('security_ir', logger)
    security_ir_role = security_ir_role_config.get_role()
    enforce_ir_role_config = get_aws_data.GetRoles('enforce_ir', logger)
    enforce_ir_role = enforce_ir_role_config.get_role()
    role_session_name = "AssumeRoleEnforceSession"
    ir_enforce_credential_data = {
        'security_ir_enforce_role': security_ir_role,
        'ir_enforce_role': enforce_ir_role,
        'role_session_name': role_session_name

    }
    return ir_enforce_credential_data
