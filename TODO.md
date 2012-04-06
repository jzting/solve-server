TODO
----
- make sure all tests pass
- diesel, fork_child, thread? proxy?
        
URLS
----
http://static.iminlikewithyou.com/drawsomething/wordlist.csv
http://static.iminlikewithyou.com/drawsomething/version.json
http://omgpop.com/mobile_controller/server_time?app_name=drawmythingmobile&device_id=febdf20f41749583987a0f086a8b7cc1b99c5d69&signature=f53b8082e0d2f44dc76c109b76620bd3&sku=paid&

WIRESHARK
---------
en1
not ether broadcast and not ether multicast


STRATEGY
--------
1. Find word length via number of # blanks, # blanks + # blues in guess row, or # red letters
2. Find all letters
3. Detect word

OPTIMIZATIONS
-------------
- reduce number of loops. right now average is 21 (*fastmatch) (alpha is 23.4 loops)
- reduce number of possible results?

- based on guessed number of letters, use specified letter distribution/order?
- print out non-word letters and try to guess distribution/generation
- merge nonword and word letter order by proportionate frequency

FUTURE
------  
- research iAP
  - remove ads  
  - use keychain to keep track of # lookups?
- decrement lookup counter if lookup succeeded

DONE
----
x crop to only use letters (25% faster)
x downsample uploaded crops to 10% quality (< 20K)
x reduce required accuracy to 90%
x scroll down to camera roll
x test dns drawsolver.jzlabs.com
x test concurrency on server
  x blocks at app server,  load balance with ec2 if needed
x will resizing to 2x still match? (no)
x cut out all blues again with padding FUUUUUU
x check screenshot size: if width is not 320 or 640, show error message
x pass hi/lo flag to post
x version=hi/lo
xrequest_id= uuid
x token= hmac(uuid + shared secret)
x add error messages on server side (no results found)
x message for need internet error
x hmac
x add appirater
  x show on the next launch after 5 successful solves
  x add flurry
    x log time to solve, total time taken, rtt
    x log fails w/ filename
    x log 410s w/ timestamp  
  x add ads
    x greystripe for interstitials
    x iad for banners    
x fullscreen (no status bar)
x new buttons with down states
x analyzing animation
x error analyzing state
x custom font for words