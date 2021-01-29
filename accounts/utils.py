def is_ManagementRepresentative(user):
    return user.groups.filter(name='ManagementRepresentative').exists()

def is_TopManager(user):
    return user.groups.filter(name='TopManager').exists()

def is_Auditor(user):
    return user.groups.filter(name='Auditor').exists()