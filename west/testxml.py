from xml.dom import minidom
s="""<?xml version="1.0" encoding="gb2312"?>
<property>
<returncode>500</returncode>
<returnmsg><![CDATA[此域名已经被其他用户注册了! ]]></returnmsg>
<info>
</info>
</property>"""

doc = minidom.parseString(s)
root = doc.documentElement

returncode = root.getElementsByTagName("returncode")

print(returncode[0].childNodes[0].nodeValue)