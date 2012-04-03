# Intro

Mailinator is a service which lets you use anonymous emails for free. This
module is a scraper for the website which lets you avoid the hassle of checking
for updates to see if your desired email has arrived.

```python
import mailinator
mailinator.get_newest_mail('my_username', time_delta=5)
```

The above code will refresh the `my_username@mailinator.com` mailbox until an
email arrives with a timestamp within the last five minutes.

Additionally, you can view all of the mail for a particular mailbox:

```python
import mailinator
emails = mailinator.get_mail('my_username')
[email.preview_subject for email in emails]
```

Returns something like the following

```python
['Trends Overview Part III: Consumer',
 'Find Your RV at MyRVLink.com...',
 'pete@sogetthis.com Breitling Discount-74',
 'Delighting Customers with Virtual Call A',
 'Re: [Grinder-use] grinder-use Digest, Vo']
```

# Install

```
pip install mailinator
```
