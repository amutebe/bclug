
############################DEFINE USER GROUPS#####################################################
def is_ManagementRepresentative(user):
    return user.groups.filter(name='ManagementRepresentative').exists()

def is_TopManager(user):
    return user.groups.filter(name='TopManager').exists()

def is_Auditor(user):
    return user.groups.filter(name='Auditor').exists()


def is_Executive(user):
    return user.groups.filter(name='Executive').exists()


#########################################DEFINE DATA GROUPS FOR INDIVIDUAL RECORDS#####################################################################
def is_Operations(user):
    return user.groups.filter(name='Operations').exists()

def is_Technical(user):
    return user.groups.filter(name='Technical').exists()

def is_Accounts(user):
    return user.groups.filter(name='Accounts').exists()

def is_Administration(user):
    return user.groups.filter(name='Administration').exists()

def is_Marketing(user):
    return user.groups.filter(name='Marketing').exists()


############################################GET LOGGEDIN USER DATA GROUP#######################################################################

def my_data_group(user):
    if user.groups.filter(name='Operations').exists():
        return "Operations"
    elif user.groups.filter(name='Marketing').exists():
        return "Marketing"
    elif user.groups.filter(name='Administration').exists():
        return "Administration"
    elif user.groups.filter(name='Technical').exists():
        return "Technical"
    elif user.groups.filter(name='Accounts').exists():
        return "Accounts"
