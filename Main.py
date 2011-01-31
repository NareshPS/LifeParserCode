#A portion of this code is taken from http://code.google.com/p/yjl/source/browse/Python/snippet/gmail-xoauth.py

import email
import email.header
import imaplib
import sys

# http://google-mail-xoauth-tools.googlecode.com/svn/trunk/python/xoauth.py
import xoauth

scope = 'https://mail.google.com/'
consumer = xoauth.OAuthEntity('www.algorithm.cs.sunysb.edu', 'NQt5F+kzh3iFIgxYvTZ8E0wW')
imap_hostname = 'imap.googlemail.com'

# How many messages will be fetched for listing?
MAX_FETCH = 20


try:
    import config
except ImportError:
    class Config():
        pass
    config = Config()

def get_access_token():
    request_token = xoauth.GenerateRequestToken(
        consumer, scope, nonce=None, timestamp=None,
        google_accounts_url_generator=config.google_accounts_url_generator
        )
    
    oauth_verifier = raw_input('Enter verification code: ').strip()
    print oauth_verifier
    try:
        access_token = xoauth.GetAccessToken(
            consumer, request_token, oauth_verifier, config.google_accounts_url_generator)
    except ValueError:
        # Could indicate failure of authentication because verifier is incorrect
        print 'Incorrect verification code?'
        sys.exit(1)
    return access_token


def main():  
    # Checking user email and access token
    if not hasattr(config, 'user') or not hasattr(config, 'access_token'):
        config.user = raw_input('Please enter your email address: ')
        config.google_accounts_url_generator = xoauth.GoogleAccountsUrlGenerator(config.user)
        access_token = get_access_token()
        config.access_token = {'key': access_token.key, 'secret': access_token.secret}
        # XXX save token, this is not a good way, I'm too lazy to use something
        # like shelve.
        f = open('config.py', 'w')
        f.write('user = %s\n' % repr(config.user))
        f.write('access_token = %s\n' % repr(config.access_token))
        f.close()
        print '\n\nconfig.py written.\n\n'
    
    config.google_accounts_url_generator = xoauth.GoogleAccountsUrlGenerator(config.user)
    access_token = xoauth.OAuthEntity(config.access_token['key'], config.access_token['secret'])
    
    # Generate xoauth string
    class ImBad():
        # I'm bad because I'm going to shut xoauth's mouth up. So you won't see these debug messages:
        # signature base string:
        # GET&https%3A%2F%2Fmail.google.com%2Fmail%2Fb%2Flivibetter%40gmail.com%...
        #
        # xoauth string (before base64-encoding):
        # GET https://mail.google.com/mail/b/livibetter@gmail.com/IMAP/ oauth_co...
        def write(self, msg): pass
    sys.stdout = ImBad()
    xoauth_string = xoauth.GenerateXOauthString(
        consumer, access_token, config.user, 'IMAP',
        xoauth_requestor_id=None, nonce=None, timestamp=None)
    sys.stdout = sys.__stdout__
    
    # Get unread/unseen list
    imap_conn = imaplib.IMAP4_SSL(imap_hostname)
    # imap_conn.debug = 4
    imap_conn.authenticate('XOAUTH', lambda x: xoauth_string)
    #print imap_conn.list()
    # Set readonly, so the message won't be set with seen flag
    imap_conn.select('[Gmail]/All Mail', readonly=True)
    typ, data = imap_conn.search(None, 'ALL')
    unreads = data[0].split()
    print '%d message(s).' % len(unreads)
    ids = ','.join(unreads[:MAX_FETCH])
    print ids
    if ids:
        typ, mailHeader = imap_conn.fetch(ids, '(RFC822.HEADER)')
        
        idList  = ids.split(',')
        mailIdx = 1
        
        for item in mailHeader:
            if isinstance(item, tuple):
                typ, mailText   = imap_conn.fetch(mailIdx, '(RFC822.TEXT)')
                print 'Mail Contents: %s' % (mailText[ 0 ][ 1 ])
                raw_header = item[1]
                header  = email.message_from_string(raw_header)
                print header
                # Some email's header are encoded, for example: '=?UTF-8?B?...'
                print 'FROM:%s SUBJECT:%s' % (
                    email.header.decode_header(header['from'])[0][0],
                    email.header.decode_header(header['subject'])[0][0],
                    )
                mailIdx += 1

    imap_conn.close()
    imap_conn.logout()

if __name__ == '__main__':
    main()