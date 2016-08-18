from tldextract import extract

subdomain, maindomain, tld = extract("a.jcirocktown.org.in")
print(subdomain,maindomain,tld)