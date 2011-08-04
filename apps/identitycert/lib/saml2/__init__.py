import saml as SAML
import time, logging
import lib.xml as xml
import jwt


class SamlService(object):
    
    def __init__(self):
        pass
    
    def buildAssertion(self,username, audience, clientid, callback):
        ## assertion = issue instant, id xmlns = urn:oasis:names:tc:SAML:2.0:assertion
        ## name id / subject
        ## subject confirmationdata - method= urn:oasis:names:tc:SAML:2.0:cm:bearer, notOnorAfter = exp time, recipient = callback
        ## condition / audience restriction - audence = audience
        ## auth statement - authninstant = currenttime
        ##     auth contextclassref =  urn:oasis:names:tc:SAML:2.0:ac:classes:X509
        subject = SAML.Subject(username,"urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",'urn:oasis:names:tc:SAML:2.0:cm:bearer',callback)
        authStatement = SAML.AuthenticationStatement(subject,None)
        notBefore = time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
        notOnOrAfter = time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime(time.time() + 5))
        conditions = SAML.Conditions(notBefore, notOnOrAfter,audience)
        return SAML.Assertion(authStatement, clientid, conditions)
    ## encodes in base 64 url
    def encodeAssertion(self,assertion, privatekey, certificate):
        #result = xml.signXml(assertion.getXMLNode(certificate).toxml(), privatekey, certificate,'#'+assertion.assertionUUID)
        #return jwt.base64url_encode(result)
        node=assertion.sign(privatekey,certificate)
        return SAML.encodeXml(node)


service = SamlService()