import imaplib
import xoauth
import siteConfig

conn=imaplib.IMAP4_SSL("imap.googlemail.com");
oAuthConsumer       = xoauth.OAuthEntity(siteConfig.consumerKey, siteConfig.consumerSecret)
oAuthAccess = xoauth.OAuthEntity('1/DJmkp2hONVLXF0-9ZESc9jzAJEA0dZmtqwxwIWo-EAM', 'UTNrwt9RP+1Y3ybb3GWPT1MZ')
oauthstr=xoauth.GenerateXOauthString(oAuthConsumer, oAuthAccess, 'mail2naresh@gmail.com', 'IMAP', None, None, None)
conn.authenticate('XOAUTH', lambda x: oauthstr)
conn.select('INBOX')
conn.search(None, None)
