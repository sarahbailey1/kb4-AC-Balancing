import pandas as pd

# Load the O365 licensed and allowed user list (this should be the CSV you pulled from O365)
o365_users = pd.read_csv("Y:/Scripts/Python/EGIS/ACkb4/O365_Users.csv")

# Load the KB4 user list (this should be the CSV you pulled from KB4)
kb4_users = pd.read_csv("Y:/Scripts/Python/EGIS/ACkb4/kb4_Users.csv")

# Load the exception list (service accounts) from a CSV file
service_accounts_df = pd.read_csv("Y:/Scripts/Python/EGIS/ACkb4/service_accounts.csv")

# Extract the 'Email' column from the service accounts CSV and convert to lowercase
service_account_emails = service_accounts_df['Email'].str.lower().tolist()

# Clean column names to avoid any leading/trailing spaces or typos
o365_users.columns = o365_users.columns.str.strip()
kb4_users.columns = kb4_users.columns.str.strip()

# Print out the columns to check for correctness
print("O365 Users Columns:", o365_users.columns)
print("KB4 Users Columns:", kb4_users.columns)

o365_users['Licenses'] = o365_users['Licenses'].astype(str).str.strip() 
o365_users['Block credential'] = o365_users['Block credential'].astype(str).str.strip() 

# Convert 'UserPrincipalName' to lowercase in O365 list for case-insensitive comparison
o365_users['UserPrincipalName'] = o365_users['UserPrincipalName'].str.lower()

# Filter O365 users to include only those who are licensed (Licenses is not 'Unlicensed') 
# and whose sign-in is not blocked (Block credential is not 'TRUE') EXCEPT service accounts
filtered_o365_users = o365_users[ 
    (o365_users['Licenses'] != 'Unlicensed') &  # Exclude users with 'Unlicensed'
    (o365_users['Block credential'].str.lower() != 'true') &  # Ensure sign-in is not blocked
    (~o365_users['UserPrincipalName'].isin(service_account_emails))  # Exclude service accounts
]

# Convert the 'Email' column in KB4 users list to lowercase for case-insensitive comparison
kb4_users['Email'] = kb4_users['Email'].str.lower()

# Cross-reference: Find users from combined O365 list who are NOT in the KB4 list
# We'll check if the O365 user email (UserPrincipalName) is not in the KB4 email list (Email)
not_in_kb4 = filtered_o365_users[~filtered_o365_users['UserPrincipalName'].isin(kb4_users['Email'])]

# Output the users who should be in KB4 but aren't
print("Users who should be in KB4 but are not:")
print(not_in_kb4)

# Save the list of users who should be in KB4 but aren't to a new CSV file
not_in_kb4.to_csv(r"Y:/Scripts/Python/EGIS/ACkb4/users_not_in_kb4.csv", index=False)
