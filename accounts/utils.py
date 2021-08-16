from django import forms
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
        return "4"
    elif user.groups.filter(name='Marketing').exists():
        return "005"
    elif user.groups.filter(name='Administration').exists():
        return "001"
    elif user.groups.filter(name='Technical').exists():
        return "11"
    elif user.groups.filter(name='Accounts').exists():
        return "12"
    else:
        return ""

###################RESTRICTS UPLOAD SIZE TO 10MBS#################################
def validate_file_size(value):
    filesize= value.size
    #print("PRINT FILESIZE",filesize)
    
    if filesize > 10485760:
        #print("PRINT FILESIZE two",filesize)
        raise forms.ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value