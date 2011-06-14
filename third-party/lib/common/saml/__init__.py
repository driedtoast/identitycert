import xml.dom.minidom
import uuid
import time
import hashlib
import M2Crypto
import base64
import StringIO
import logging


import saml.SAMLMessages as SAMLMessages


def log(loglevel, logfilename):
  logging.basicConfig(level=loglevel, format='%(asctime)s %(levelname)s %(message)s',filename=logfilename,filemode='w')




def encodeXml(obj):
  return base64.urlsafe_b64encode(obj.toxml()).replace('=','')

def getBase64EncodedXML(obj):
  base64string = base64.b64encode(str(obj))
  return base64string

def insertEnvelopedSignature(unsignedSAMLResponse, responseId, privatekey):
  doc = xml.dom.minidom.Document()
  signatureElement = doc.createElementNS("http://www.w3.org/2000/09/xmldsig#", "Signature")
  signedInfoElement = doc.createElement("SignedInfo")
  canonicalizationMethodElement = doc.createElement("CanonicalizationMethod")
  canonicalizationMethodElement.setAttribute("Algorithm","http://www.w3.org/2001/10/xml-exc-c14n#")

  signatureMethodElement = doc.createElement("SignatureMethod")
  signatureMethodElement.setAttribute("Algorithm","http://www.w3.org/2000/09/xmldsig#rsa-sha1")

  referenceElement = doc.createElement("Reference")
  referenceElement.setAttribute("URI", "#" + responseId)
 
  transformsElement = doc.createElement("Transforms")
  transformElement1 = doc.createElement("Transform")
  transformElement1.setAttribute("Algorithm","http://www.w3.org/2000/09/xmldsig#enveloped-signature")
 
  transformElement2 = doc.createElement("Transform")
  transformElement2.setAttribute("Algorithm","http://www.w3.org/2001/10/xml-exc-c14n#")
  
  referenceElement.appendChild(transformsElement)
  transformsElement.appendChild(transformElement1)
  transformsElement.appendChild(transformElement2)

  digestMethodElement = doc.createElement("DigestMethod")
  digestMethodElement.setAttribute("Algorithm","http://www.w3.org/2000/09/xmldsig#sha1")
  
  referenceElement.appendChild(digestMethodElement)

  # Perform the actual hashing
  digestValueElement = doc.createElement("DigestValue")
  hash = hashlib.sha1()
  hash.update(unsignedSAMLResponse.toxml())
 
  digestValue = doc.createTextNode(base64.b64encode(hash.digest()))
  digestValueElement.appendChild(digestValue)
  referenceElement.appendChild(digestValueElement)

  signatureValueElement = doc.createElement("SignatureValue")
  m = M2Crypto.RSA.load_key_string(privatekey)
  signature = m.sign(hash.digest(),"sha1")
 
  signatureValueText = doc.createTextNode(base64.b64encode(signature))
  signatureValueElement.appendChild(signatureValueText)

  signatureElement.appendChild(signedInfoElement)
  signatureElement.appendChild(signatureValueElement)
  
  statusElement = unsignedSAMLResponse.getElementsByTagName("Status").item(0)
  
  unsignedSAMLResponse.appendChild(signatureElement)
 
  return unsignedSAMLResponse


def insertCertificate(elementRoot, certificate):
  doc = xml.dom.minidom.Document()

  # Pull the <signature> element
  signatureElement = elementRoot.getElementsByTagName("Signature").item(0)
 
  keyInfoElement = doc.createElement("KeyInfo")
  x509DataElement = doc.createElement("X509Data")
  x509CertificateElement = doc.createElement("X509Certificate")


  # Parse the certificate text into an M2Crypto X509 certificate object
  x509CertObject = M2Crypto.X509.load_cert_string(certificate)

  # Remove the "-----BEGIN CERTIFICATE-----" and "-----END CERTIFICATE-----"
  # and clean up any leading and trailing whitespace
  certificatePEM = x509CertObject.as_pem()
  certificatePEM = certificatePEM.replace("-----BEGIN CERTIFICATE-----","")
  certificatePEM = certificatePEM.replace("-----END CERTIFICATE-----","")
  certificatePEM = certificatePEM.strip()

  x509CertificateText = doc.createTextNode(certificatePEM)

  x509CertificateElement.appendChild(x509CertificateText)
  x509DataElement.appendChild(x509CertificateElement)
  keyInfoElement.appendChild(x509DataElement)
  signatureElement.appendChild(keyInfoElement)

  return elementRoot

  
class Conditions(object):
  
  def __init__(self, notBefore=None, notOnOrAfter=None, audience=None):

    if(notBefore == None):
      self.notBefore = time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
    else:
      self.notBefore = notBefore
        
    if(notOnOrAfter == None):
      self.notOnOrAfter = time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime(time.time() + 60))
    else:
      self.notOnOrAfter = notOnOrAfter
    self.audience=audience
    
  def __str__(self):
    return self.getXML()

  def getXML(self):
    return self.getXMLNode().toxml()

  def getXMLNode(self):
    doc = xml.dom.minidom.Document()
    conditionsElement = doc.createElement("Conditions")
    conditionsElement.setAttribute("NotBefore", self.notBefore)
    conditionsElement.setAttribute("NotOnOrAfter", self.notOnOrAfter)
    if(self.audience != None):
      audienceRestrictElement = doc.createElement("AudienceRestriction")
      audienceElement  = doc.createElement("Audience")
      audienceElement.appendChild(doc.createTextNode(self.audience))
      audienceRestrictElement.appendChild(audienceElement)
      conditionsElement.appendChild(audienceRestrictElement)
      
    return conditionsElement    
    
    
class AuthenticationStatement(object):

  def __init__(self, subject, authInstant):

    self.subject = subject
    # If there is no authentication instant specified default to the current time
    if(authInstant == None):
      self.authInstant = time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
    else:
      self.authInstant = authInstant

  def __str__(self):
    return self.getXML()

  def getXML(self):
    return self.getXMLNode().toxml()

  def getXMLNode(self):
    doc = xml.dom.minidom.Document()  
    authenticationStatementElement = doc.createElement("AuthnStatement")
    authenticationStatementElement.setAttribute("AuthnInstant", self.authInstant)     
    return authenticationStatementElement
  def getSubject(self):
    return self.subject.getXMLNode()
    


# The Subject class specifies who the assertion is about
class Subject(object):
                
  def __init__(self, name, nameidformat,confirmationMethod=None,recipient=None,notOnOrAfter=None):
    self.name = name
    self.set_nameidformat(nameidformat)
    self.confirmationMethod = confirmationMethod
    self.recipient = recipient
    if(notOnOrAfter == None):
      self.notOnOrAfter = time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime(time.time() + 60))
    else:
      self.notOnOrAfter = notOnOrAfter

  def __str__(self):
    return self.getXML()

  def getXML(self):
    return self.getXMLNode().toxml()

  def getXMLNode(self):
    doc = xml.dom.minidom.Document()
    subjectElement = doc.createElement("Subject")
    
    # <NameIdentifier>
    nameIDElement = doc.createElement("NameIdentifier")
    nameIDElement.setAttribute("Format",self.nameidformat)
    nameIDText = doc.createTextNode(self.name)
    nameIDElement.appendChild(nameIDText)
    
    subjectConfirmationElement = doc.createElement("SubjectConfirmation")
    if (self.confirmationMethods != None):
      subjectConfirmationElement.setAttribute("Method",confirmationMethod)
    if (self.recipient != None):
      subjectConfirmData = doc.createElement("SubjectConfirmationData")
      subjectConfirmData.setAttribute("Recipient",self.recipient)
      subjectConfirmData.setAttribute("NotOnOrAfter",self.notOnOrAfter)
      subjectConfirmationElement.appendChild(subjectConfirmData)
    subjectElement.appendChild(nameIDElement)
    subjectElement.appendChild(subjectConfirmationElement)
  
    return subjectElement


  # nameidformat property
  def get_nameidformat(self):
    return self._nameidformat
  
  def set_nameidformat(self, value):
    validNameIDFormats = ["urn:oasis:names:tc:SAML:1.0:nameid-format:unspecified",
                          "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",
                          "urn:oasis:names:tc:SAML:1.1:nameid-format:X509SubjectName",
                          "urn:oasis:names:tc:SAML:1.1:nameid-format:WindowsDomainQualifiedName"]

    # Double check to see if the person entered a valid nameid-format                      
    if value not in validNameIDFormats:
      logging.warning("The nameidformat supplied is not valid. Valid formats are: " + str(validNameIDFormats))
    
    # Set the nameid format anyway for flexibility
    self._nameidformat = value
    
  def del_nameidformat(self):
    del self._nameidformat

  
  # Instance variables
  nameidformat = property(get_nameidformat, set_nameidformat, del_nameidformat,
                          "This is the urn:oasis:names:tc:SAML:1.0:nameid-format property")
        
 
 
 
 
 
class Assertion(object):
  
  def __init__(self, authStatement, issuer, conditions):
    self.authStatement = authStatement
    self.issuer = issuer
    self.conditions = conditions    
    self.assertionUUID = str(uuid.uuid4())
    self.issueInstant = time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
    
  def __str__(self):
    return self.getXML()

  def getXML(self):
    return self.getXMLNode().toxml()

  def getXMLNode(self,certificate=None):
  
    doc = xml.dom.minidom.Document()
    assertionElement = doc.createElementNS("urn:oasis:names:tc:SAML:2.0:assertion", "Assertion")

    # MajorVersion [required]
    assertionElement.setAttribute("Version","2.0")

    # AssertionID [required]
    assertionElement.setAttribute("ID", self.assertionUUID )

    # Issuer [required]
    issuerElement = doc.createElement("Issuer")
    issuerText = doc.createTextNode(self.issuer)
    issuerElement.appendChild(issuerText)
    assertionElement.appendChild(issuerElement)
    assertionElement.appendChild(self.authStatement.getSubject())

    # Assertions must have a time in which they were issued/created
    assertionElement.setAttribute("IssueInstant", self.issueInstant )

    assertionElement.appendChild(self.conditions.getXMLNode())
    authNode = self.authStatement.getXMLNode()
    if(certificate != None):
      authContext = doc.createElement("AuthnContext")
      authContextRef = doc.createElement("AuthnContextClassRef")
      authContextRef.appendChild(doc.createTextNode("urn:oasis:names:tc:SAML:2.0:ac:classes:X509"))
      authContext.appendChild(authContextRef)
      authNode.appendChild(authContext)
    assertionElement.appendChild(authNode)

    return assertionElement
  def sign(self,privateKey,certificate):
    xmlNode = self.getXMLNode(certificate)
    # If a private key was specified sign the response
    if ( privateKey != None ):
      xmlNode = insertEnvelopedSignature(xmlNode,self.assertionUUID,privateKey)
   
    # Add a certificate if it was specified
    if ( certificate != None ):
      xmlNode = insertCertificate(xmlNode,certificate)

    return xmlNode



class Response(object):

  def __init__(self, assertion, privatekey=None, certificate=None):
    self.assertion = assertion
    self.privatekey = privatekey
    self.certificate = certificate
    self.responseID = str(uuid.uuid4())
  
  def __str__(self):
    return self.getXML()

  def getXML(self):
    return self.getXMLNode().toxml()

  def getXMLNode(self):

    doc = xml.dom.minidom.Document()
    responseElement = doc.createElementNS("urn:oasis:names:tc:SAML:1.0:protocol", "Response")
    responseElement.setAttribute("MajorVersion","1")
    responseElement.setAttribute("MinorVersion","1")

    # There is no Recipient in SAML 1.1?
    # responseElement.setAttribute("Recipient", "http://www.visa.com/affwebservices/public/samlcc" )

    responseElement.setAttribute("ResponseID", self.responseID )
    responseElement.setAttribute("IssueInstant", time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()))

    statusElement = doc.createElement("Status")
    statusCodeElement = doc.createElement("StatusCode")
    statusCodeElement.setAttribute("Value","Success")
    statusElement.appendChild(statusCodeElement)

    responseElement.appendChild(statusElement)
    responseElement.appendChild(self.assertion.getXMLNode())
    
    
    # If a private key was specified sign the response
    if ( self.privatekey != None ):    
      responseElement = insertEnvelopedSignature(responseElement,self.responseID,self.privatekey)    
    
    # Add a certificate if it was specified
    if ( self.certificate != None ):
      responseElement = insertCertificate(responseElement,self.certificate)
        
    return responseElement


  def certificate(self, cert):
    self.x509certificate = cert
    # Can add checks later for the certificate
    # from OpenSSL import crypto   
    #cert = crypto.X509()
    #x509 = crypto.load_certificate(crypto.FILETYPE_PEM,certString)
    #print x509.get_issuer()
    #print x509.get_subject()



