# sample code 
```
cleaned_df = clean_public_domains(df, email_col_name='user_email')
```
# sample output
```
Total email addresses: 65657
Number of public domain types found: 41
Total public domain emails: 4414

Counts for each public domain:
gmail.com           2706
yahoo.com            577
aol.com              326
hotmail.com          155
sbcglobal.net        103
outlook.com           99
bellsouth.net         97
att.net               60
verizon.net           55
msn.com               54
live.com              24
icloud.com            17
ymail.com             16
optonline.net         13
charter.net           11
me.com                11
windstream.net        10
earthlink.net         10
embarqmail.com         8
ameritech.net          8
bresnan.net            7
roadrunner.com         6
midconetwork.com       6
ptd.net                6
centurylink.net        4
swbell.net             3
comporium.net          3
wyoming.com            3
rocketmail.com         2
bellsouth.com          2
juno.com               2
yahoo.cm               1
mail.com               1
aim.com                1
knology.net            1
suddenlink.net         1
epix.net               1
cs.com                 1
my.com                 1
contractor.net         1
usa.com                1
Name: domain, dtype: int64
```

graph TD
    A[Initialize Repository<br>`git init`] --> B[Clone Repository<br>`git clone <url>`]
    B --> C[Create/Checkout Branch<br>`git branch` / `git checkout <branch>`]
    C --> D[Modify Files]
    D --> E[Stage Changes<br>`git add <file>`]
    E --> F[Commit Changes<br>`git commit -m "message"`]
    F --> G[Push to Remote Repository<br>`git push`]
    G --> H[Pull from Remote Repository<br>`git pull`]
    H --> C
    D --> I[View Commit History<br>`git log`]
    E --> J[Unstage Changes<br>`git reset HEAD <file>`]
    F --> K[Revert Changes<br>`git revert <commit>`]
    G --> L[Merge Changes<br>`git merge <branch>`]
    L --> C

