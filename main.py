# import modules
import boto3
from datetime import datetime

# code
noOfDays=90

client=boto3.client('iam')
unUsedUser=[]
unsedDate=[]

response=client.list_users()
lst_users = response['Users']
for i in lst_users:
    if 'PasswordLastUsed' in i.keys():
        date1 = datetime.strptime(i['PasswordLastUsed'].strftime('%d-%m-%Y'),'%d-%m-%Y')
        date2 = datetime.strptime(datetime.now().strftime("%d-%m-%Y"),'%d-%m-%Y') 
        datediff = date2 - date1
        print(f'user: {i["UserName"]} has the key age : {datediff.days} days')
        
        if datediff.days > noOfDays:
            response = client.list_access_keys(UserName=i['UserName'])
            userkey=[eachkey['AccessKeyId'] for eachkey in response['AccessKeyMetadata']]
            print(userkey)
            for key in userkey:
                response = client.update_access_key(
                    UserName=i['UserName'],
                    AccessKeyId=key,
                    Status='Inactive'
                )
            print("Access Keys deactivated due to user Inactivity.")
    else:
        unUsedUser.append(i['UserName'])
        date1 = datetime.strptime(i['CreateDate'].strftime('%d-%m-%Y'),'%d-%m-%Y')
        date2 = datetime.strptime(datetime.now().strftime("%d-%m-%Y"),'%d-%m-%Y')
        datediff=date2 - date1
        unsedDate.append(datediff.days)
        # print(f"Unused user {i['UserName']} created before: ",datediff.days, "Days.")

unused_usr = dict(zip(unUsedUser,unsedDate))
print("\nUnused users are : {'username','age in dayes'}\n",unused_usr)