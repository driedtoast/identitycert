#!/usr/bin/python
#
# Copyright (C) 2007 SIOS Technology, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Contains objects used with SAML-2."""

__author__ = 'tmatsuo@sios.com (Takashi MATSUO)'

"""Contains classes representing Metadata elements.

  Module objective: provide data classes for Metadata
  constructs. These classes hide the XML-ness of Saml and provide a
  set of native Python classes to interact with.

"""

try:
  from xml.etree import cElementTree as ElementTree
except ImportError:
  try:
    import cElementTree as ElementTree
  except ImportError:
    from elementtree import ElementTree

import saml2
from saml2 import saml
import xmldsig as ds

MD_NAMESPACE = 'urn:oasis:names:tc:SAML:2.0:metadata'
MD_TEMPLATE = '{urn:oasis:names:tc:SAML:2.0:metadata}%s'
XMLENC_NAMESPACE = 'http://www.w3.org/2001/04/xmlenc#'

class Extensions(saml2.SamlBase):
  """The md:Extensions element"""

  _tag = 'Extensions'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()

def ExtensionsFromString(xml_string):
  return saml2.CreateClassFromXMLString(Extensions, xml_string)

class localizedName(saml2.SamlBase):
  """The md:localizedName abstract type"""
  _tag = 'localizedName'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()
  _attributes['{http://www.w3.org/XML/1998/namespace}lang'] = 'lang'

  def __init__(self, lang=None, text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for localizedName

    Args:
      lang: xml:lang attribute
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    self.lang = lang
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

def localizedNameFromString(xml_string):
  return saml2.CreateClassFromXMLString(localizedName, xml_string)

class localizedURI(saml2.SamlBase):
  """The md:localizedURI abstract type"""
  _tag = 'localizedURI'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()
  _attributes['{http://www.w3.org/XML/1998/namespace}lang'] = 'lang'

  def __init__(self, lang=None, text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for localizedURI

    Args:
      lang: xml:lang attribute
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    self.lang = lang
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

def localizedURIFromString(xml_string):
  return saml2.CreateClassFromXMLString(localizedURI, xml_string)


class OrganizationName(localizedName):
  """The md:OrganizationName element"""
  _tag = 'OrganizationName'
  _namespace = MD_NAMESPACE
  _children = localizedName._children.copy()
  _attributes = localizedName._attributes.copy()

  def __init__(self, lang=None, text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for OrganizationName

    Args:
      lang: xml:lang attribute
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    localizedName.__init__(self, lang=lang)
    
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}


def OrganizationNameFromString(xml_string):
  return saml2.CreateClassFromXMLString(OrganizationName, xml_string)


class OrganizationDisplayName(localizedName):
  """The md:OrganizationDisplayName element"""
  _tag = 'OrganizationDisplayName'
  _namespace = MD_NAMESPACE
  _children = localizedName._children.copy()
  _attributes = localizedName._attributes.copy()

  def __init__(self, lang=None, text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for OrganizationDisplayName

    Args:
      lang: xml:lang attribute
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    localizedName.__init__(self, lang=lang)
    
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}


def OrganizationDisplayNameFromString(xml_string):
  return saml2.CreateClassFromXMLString(OrganizationDisplayName, xml_string)


class OrganizationURL(localizedURI):
  """The md:OrganizationURL element"""
  _tag = 'OrganizationURL'
  _namespace = MD_NAMESPACE
  _children = localizedURI._children.copy()
  _attributes = localizedURI._attributes.copy()

  def __init__(self, lang=None, text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for OrganizationURL

    Args:
      lang: xml:lang attribute
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    localizedURI.__init__(self, lang=lang)
    
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}


def OrganizationURLFromString(xml_string):
  return saml2.CreateClassFromXMLString(OrganizationURL, xml_string)


class Organization(saml2.SamlBase):
  """The md:Organization base type"""

  _tag = 'Organization'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()
  _children['{%s}Extensions' % MD_NAMESPACE] = ('extensions', Extensions)
  _children['{%s}OrganizationName' % MD_NAMESPACE] = (
    'organization_name', [OrganizationName])
  _children['{%s}OrganizationDisplayName' % MD_NAMESPACE] = (
    'organization_display_name', [OrganizationDisplayName])
  _children['{%s}OrganizationURL' % MD_NAMESPACE] = (
    'organization_url', [OrganizationURL])
  child_order = ['extensions', 'organization_name',
                 'organization_display_name', 'organization_url']

  def __init__(self, extensions=None, organization_name=None,
               organization_display_name=None, organization_url=None,
               text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for Organization

    Args:
      extensions: Extensions element
      organization_name: OrganizationName elements
      organization_display_name: OrganizationDisplayName elements
      organization_url: OrganizationURL elements
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    self.extensions = extensions
    self.organization_name = organization_name or []
    self.organization_display_name = organization_display_name or []
    self.organization_url = organization_url or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

def OrganizationFromString(xml_string):
  return saml2.CreateClassFromXMLString(Organization, xml_string)
  

class Endpoint(saml2.SamlBase):
  """The md:Endpoint base type"""

  _tag = 'Endpoint'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()
  _attributes['Binding'] = 'binding'
  _attributes['Location'] = 'location'
  _attributes['ResponseLocation'] = 'response_location'

  def __init__(self, binding=None, location=None, response_location=None,
               text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for Endpoint

    Args:
      binding: Binding attribute
      location: Location attribute
      reseponse_location: ResponseLocation attribute
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    self.binding = binding
    self.location = location
    self.response_location = response_location
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

def EndpointFromString(xml_string):
  return saml2.CreateClassFromXMLString(Endpoint, xml_string)


class IndexedEndpoint(Endpoint):
  """The md:IndexedEndpoint base type"""

  _tag = 'IndexedEndpoint'
  _namespace = MD_NAMESPACE
  _children = Endpoint._children.copy()
  _attributes = Endpoint._attributes.copy()
  _attributes['index'] = 'index'
  _attributes['isDefault'] = 'is_default'

  def __init__(self, binding=None, location=None, response_location=None,
               index=None, is_default=None,
               text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for IndexedEndpoint

    Args:
      binding: Binding attribute
      location: Location attribute
      reseponse_location: ResponseLocation attribute
      index: index attribute
      is_default: isDefault attribute
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    Endpoint.__init__(self, binding=binding, location=location,
                      response_location=response_location)
    self.index = index
    self.is_default = is_default
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

def IndexedEndpointFromString(xml_string):
  return saml2.CreateClassFromXMLString(IndexedEndpoint, xml_string)

  
class Company(saml2.SamlBase):
  """The md:Company element"""

  _tag = 'Company'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()

def CompanyFromString(xml_string):
  return saml2.CreateClassFromXMLString(Company, xml_string)


class GivenName(saml2.SamlBase):
  """The md:GivenName element"""

  _tag = 'GivenName'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()

def GivenNameFromString(xml_string):
  return saml2.CreateClassFromXMLString(GivenName, xml_string)


class SurName(saml2.SamlBase):
  """The md:SurName element"""

  _tag = 'SurName'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()

def SurNameFromString(xml_string):
  return saml2.CreateClassFromXMLString(SurName, xml_string)


class EmailAddress(saml2.SamlBase):
  """The md:EmailAddress element"""

  _tag = 'EmailAddress'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()

def EmailAddressFromString(xml_string):
  return saml2.CreateClassFromXMLString(EmailAddress, xml_string)


class TelephoneNumber(saml2.SamlBase):
  """The md:TelephoneNumber element"""

  _tag = 'TelephoneNumber'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()

def TelephoneNumberFromString(xml_string):
  return saml2.CreateClassFromXMLString(TelephoneNumber, xml_string)


class ContactPerson(saml2.SamlBase):
  """The md:ContactPerson element"""

  _tag = 'ContactPerson'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()
  _attributes['contactType'] = 'contact_type'
  _children['{%s}Extensions' % MD_NAMESPACE] = ('extensions', Extensions)
  _children['{%s}Company' % MD_NAMESPACE] = ('company', Company)
  _children['{%s}GivenName' % MD_NAMESPACE] = ('given_name', GivenName)
  _children['{%s}SurName' % MD_NAMESPACE] = ('sur_name', SurName)
  _children['{%s}EmailAddress' % MD_NAMESPACE] = (
    'email_address', [EmailAddress])
  _children['{%s}TelephoneNumber' % MD_NAMESPACE] = (
    'telephone_number', [TelephoneNumber])
  _child_order = ['extensions', 'company', 'given_name', 'sur_name',
                  'email_address', 'telephone_number']

  def __init__(self, extensions=None, contact_type=None, company=None,
               given_name=None, sur_name=None, email_address=None,
               telephone_number=None,
               text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for ContactPerson

    Args:
      contact_type: contactType attribute
      extensions: Extensions element
      company: Company element
      given_name: GivenName element
      sur_name: SurName element
      email_address: EmailAddress elements
      telephone_number: TelephoneNumber elements
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """
    
    self.contact_type = contact_type
    self.extensions = extensions
    self.company = company
    self.given_name = given_name
    self.sur_name = sur_name
    self.email_address = email_address or []
    self.telephone_number = telephone_number or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

def ContactPersonFromString(xml_string):
  return saml2.CreateClassFromXMLString(ContactPerson, xml_string)


class AdditionalMetadataLocation(saml2.SamlBase):
  """The md:AdditionalMetadataLocation element"""

  _tag = 'AdditionalMetadataLocation'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()
  _attributes['namespace'] = 'namespace'

  def __init__(self, namespace=None, text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for AdditionalMetadataLocation

    Args:
      namespace: namespace attribute
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """
    
    self.namespace = namespace
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

def AdditionalMetadataLocationFromString(xml_string):
  return saml2.CreateClassFromXMLString(AdditionalMetadataLocation, xml_string)

  
class KeySize(saml2.SamlBase):
  """The xmlenc:KeySize element"""

  _tag = 'KeySize'
  _namespace = XMLENC_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()

def KeySizeFromString(xml_string):
  return saml2.CreateClassFromXMLString(KeySize, xml_string)


class OAEPparams(saml2.SamlBase):
  """The xmlenc:OAEPparams element"""

  _tag = 'OAEPparams'
  _namespace = XMLENC_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()

def OAEPparamsFromString(xml_string):
  return saml2.CreateClassFromXMLString(OAEPparams, xml_string)


class EncryptionMethod(saml2.SamlBase):
  """The md:EncryptionMethod element"""

  _tag = 'EncryptionMethod'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()
  _attributes['Algorithm'] = 'algorithm'
  _children['{%s}KeySize' % XMLENC_NAMESPACE] = ('key_size', KeySize)
  _children['{%s}OAEPparams' % XMLENC_NAMESPACE] = ('oaep_params', OAEPparams)
  _children['{%s}DigestMethod' % ds.DS_NAMESPACE] = (
    'digest_method', ds.DigestMethod)
  _child_order = ['key_size', 'oaep_params', 'digest_method']

  def __init__(self, algorithm=None, key_size=None, digest_method=None,
               oaep_params=None, text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for EncryptionMethod

    Args:
      algorithm: Algorithm attribute
      key_size: KeySize Element
      digest_method: DigestMethod Element
      oaep_params: OAEPparams Element
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """
    
    self.algorithm = algorithm
    self.key_size = key_size
    self.digest_method = digest_method
    self.oaep_params = oaep_params
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

def EncryptionMethodFromString(xml_string):
  return saml2.CreateClassFromXMLString(EncryptionMethod, xml_string)


class KeyDescriptor(saml2.SamlBase):
  """The md:KeyDescriptor element"""

  _tag = 'KeyDescriptor'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()
  _attributes['use'] = 'use'
  _children['{%s}KeyInfo' % ds.DS_NAMESPACE] = ('key_info', ds.KeyInfo)
  _children['{%s}EncryptionMethod' % MD_NAMESPACE] = (
    'encryption_method', [EncryptionMethod])
  _child_order = ['key_info', 'encryption_method']

  def __init__(self, use=None, key_info=None, encryption_method=None,
               text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for KeyDescriptor

    Args:
      use: use attribute
      key_info: KeyInfo element
      encryption_method: EncryptionMethod elements
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """
    
    self.use = use
    self.key_info = key_info
    self.encryption_method = encryption_method or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

def KeyDescriptorFromString(xml_string):
  return saml2.CreateClassFromXMLString(KeyDescriptor, xml_string)


class RoleDescriptor(saml2.SamlBase):
  """The md:RoleDescriptor element"""

  _tag = 'RoleDescriptor'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()
  _attributes['ID'] = 'id'
  _attributes['validUntil'] = 'valid_until'
  _attributes['cacheDuration'] = 'cache_duration'
  _attributes['protocolSupportEnumeration'] = 'protocol_support_enumeration'
  _attributes['errorURL'] = 'error_url'
  _children['{%s}Signature' % ds.DS_NAMESPACE] = ('signature', ds.Signature)
  _children['{%s}Extensions' % MD_NAMESPACE] = ('extensions', Extensions)
  _children['{%s}KeyDescriptor' % MD_NAMESPACE] = (
    'key_descriptor', [KeyDescriptor])
  _children['{%s}Organization' % MD_NAMESPACE] = ('organization', Organization)
  _children['{%s}ContactPerson' % MD_NAMESPACE] = (
    'contact_person', [ContactPerson])
  _child_order = ['signature', 'extensions', 'key_descriptor', 'organization',
                  'contact_person']

  def __init__(self, id=None, valid_until=None, cache_duration=None,
               protocol_support_enumeration=None, error_url=None,
               signature=None, extensions=None, key_descriptor=None,
               organization=None, contact_person=None,
               text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for RoleDescriptor

    Args:
      id: ID attribute
      valid_until: validUntil attribute
      cache_duration: cacheDuration attribute
      protocol_support_enumeration: protocolSupportEnumeration attribute
      error_url: errorURL attribute
      signature: ds:Signature element
      extensions: Extensions element
      key_descriptor: KeyDescriptor elements
      organization: Organization element
      contact_person: ContactPerson elements
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """
    self.id = id
    self.valid_until = valid_until
    self.cache_duration = cache_duration
    self.protocol_support_enumeration = protocol_support_enumeration
    self.error_url = error_url
    self.signature = signature
    self.extensions = extensions
    self.key_descriptor = key_descriptor or []
    self.organization = organization
    self.contact_person = contact_person or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
  
def RoleDescriptorFromString(xml_string):
  return saml2.CreateClassFromXMLString(RoleDescriptor, xml_string)


class ArtifactResolutionService(IndexedEndpoint):
  """The md:ArtifactResolutionService element"""
  _tag = 'ArtifactResolutionService'

def ArtifactResolutionServiceFromString(xml_string):
  return saml2.CreateClassFromXMLString(ArtifactResolutionService, xml_string)


class AssertionConsumerService(IndexedEndpoint):
  """The md:AssertionConsumerService element"""
  _tag = 'AssertionConsumerService'

def AssertionConsumerServiceFromString(xml_string):
  return saml2.CreateClassFromXMLString(AssertionConsumerService, xml_string)


class SingleLogoutService(Endpoint):
  """The md:SingleLogoutService element"""
  _tag = 'SingleLogoutService'

def SingleLogoutServiceFromString(xml_string):
  return saml2.CreateClassFromXMLString(SingleLogoutService, xml_string)


class ManageNameIDService(Endpoint):
  """The md:ManageNameIDService element"""
  _tag = 'ManageNameIDService'

def ManageNameIDServiceFromString(xml_string):
  return saml2.CreateClassFromXMLString(ManageNameIDService, xml_string)


class NameIDFormat(saml2.SamlBase):
  """The md:NameIDFormat element"""
  
  _tag = 'NameIDFormat'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()

def NameIDFormatFromString(xml_string):
  return saml2.CreateClassFromXMLString(NameIDFormat, xml_string)


class SSODescriptor(RoleDescriptor):
  """The md:SSODescriptor element"""

  _tag = 'SSODescriptor'
  _namespace = MD_NAMESPACE
  _children = RoleDescriptor._children.copy()
  _attributes = RoleDescriptor._attributes.copy()
  _children['{%s}ArtifactResolutionService' % MD_NAMESPACE] = (
    'artifact_resolution_service', [ArtifactResolutionService])
  _children['{%s}SingleLogoutService' % MD_NAMESPACE] = (
    'single_logout_service', [SingleLogoutService])
  _children['{%s}ManageNameIDService' % MD_NAMESPACE] = (
    'manage_name_id_service', [ManageNameIDService])
  _children['{%s}NameIDFormat' % MD_NAMESPACE] = (
    'name_id_format', [NameIDFormat])

  _child_order = ['signature', 'extensions', 'key_descriptor', 'organization',
                  'contact_person', 'artifact_resolution_service',
                  'single_logout_service', 'manage_name_id_service',
                  'name_id_format']

  def __init__(self, id=None, valid_until=None, cache_duration=None,
               protocol_support_enumeration=None, error_url=None,
               signature=None, extensions=None, key_descriptor=None,
               organization=None, contact_person=None,
               artifact_resolution_service=None,
               single_logout_service=None, manage_name_id_service=None,
               name_id_format=None,
               text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for SSODescriptor

    Args:
      id: ID attribute
      valid_until: validUntil attribute
      cache_duration: cacheDuration attribute
      protocol_support_enumeration: protocolSupportEnumeration attribute
      error_url: errorURL attribute
      signature: ds:Signature element
      extensions: Extensions element
      key_descriptor: KeyDescriptor elements
      organization: Organization element
      contact_person: ContactPerson elements
      artifact_resolution_service: ArtifactResolutionService elements
      single_logout_service: SingleLogoutService elements
      manage_name_id_service: ManageNameIDService elements
      name_id_format: NameIDFormat elements
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """
    RoleDescriptor.__init__(self, id=id, valid_until=valid_until,
      cache_duration=cache_duration,
      protocol_support_enumeration=protocol_support_enumeration,
      error_url=error_url, signature=signature, extensions=extensions,
      key_descriptor=key_descriptor, organization=organization,
      contact_person=contact_person)

    self.artifact_resolution_service = artifact_resolution_service or []
    self.single_logout_service = single_logout_service or []
    self.manage_name_id_service = manage_name_id_service or []
    self.name_id_format = name_id_format or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

def SSODescriptorFromString(xml_string):
  return saml2.CreateClassFromXMLString(SSODescriptor, xml_string)


class SingleSignOnService(Endpoint):
  """The md:SingleSignOnService element"""
  _tag = 'SingleSignOnService'

def SingleSignOnServiceFromString(xml_string):
  return saml2.CreateClassFromXMLString(SingleSignOnService, xml_string)


class NameIDMappingService(Endpoint):
  """The md:NameIDMappingService element"""
  _tag = 'NameIDMappingService'

def NameIDMappingServiceFromString(xml_string):
  return saml2.CreateClassFromXMLString(NameIDMappingService, xml_string)


class AssertionIDRequestService(Endpoint):
  """The md:AssertionIDRequestService element"""
  _tag = 'AssertionIDRequestService'

def AssertionIDRequestServiceFromString(xml_string):
  return saml2.CreateClassFromXMLString(AssertionIDRequestService, xml_string)


class AttributeProfile(saml2.SamlBase):
  """The md:AttributeProfile element"""
  
  _tag = 'AttributeProfile'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()

def AttributeProfileFromString(xml_string):
  return saml2.CreateClassFromXMLString(AttributeProfile, xml_string)


class IDPSSODescriptor(SSODescriptor):
  """The md:IDPSSODescriptor element"""

  _tag = 'IDPSSODescriptor'
  _namespace = MD_NAMESPACE
  _children = SSODescriptor._children.copy()
  _attributes = SSODescriptor._attributes.copy()
  _attributes['WantAuthnRequestsSigned'] = 'want_authn_requests_signed'
  _children['{%s}SingleSignOnService' % MD_NAMESPACE] = (
    'single_sign_on_service', [SingleSignOnService])
  _children['{%s}NameIDMappingService' % MD_NAMESPACE] = (
    'name_id_mapping_service', [NameIDMappingService])
  _children['{%s}AssertionIDRequestService' % MD_NAMESPACE] = (
    'assertion_id_request_service', [AssertionIDRequestService])
  _children['{%s}AttributeProfile' % MD_NAMESPACE] = (
    'attribute_profile', [AttributeProfile])
  _children['{%s}Attribute' % saml.SAML_NAMESPACE] = (
    'attribute', [saml.Attribute])

  _child_order = ['signature', 'extensions', 'key_descriptor', 'organization',
                  'contact_person', 'artifact_resolution_service',
                  'single_logout_service', 'manage_name_id_service',
                  'name_id_format', 'single_sign_on_service',
                  'name_id_mapping_service', 'assertion_id_request_service',
                  'attribute_profile', 'attribute']

  def __init__(self, id=None, valid_until=None, cache_duration=None,
               protocol_support_enumeration=None, error_url=None,
               signature=None, extensions=None, key_descriptor=None,
               organization=None, contact_person=None,
               artifact_resolution_service=None,
               single_logout_service=None, manage_name_id_service=None,
               name_id_format=None, want_authn_requests_signed=None,
               single_sign_on_service=None, name_id_mapping_service=None,
               assertion_id_request_service=None, attribute_profile=None,
               attribute=None,
               text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for IDPSSODescriptor

    Args:
      id: ID attribute
      valid_until: validUntil attribute
      cache_duration: cacheDuration attribute
      protocol_support_enumeration: protocolSupportEnumeration attribute
      error_url: errorURL attribute
      signature: ds:Signature element
      extensions: Extensions element
      key_descriptor: KeyDescriptor elements
      organization: Organization element
      contact_person: ContactPerson elements
      artifact_resolution_service: ArtifactResolutionService elements
      single_logout_service: SingleLogoutService elements
      manage_name_id_service: ManageNameIDService elements
      name_id_format: NameIDFormat elements
      want_authn_requests_signed: WantAuthnRequestsSigned attribute
      single_sign_on_service: SingleSignOnService elements
      name_id_mapping_service: NameIDMappingService elements
      assertion_id_request_service: AssertionIDRequestService elements
      attribute_profile: AttributeProfile elements
      attribute: Attribute elements
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """
    SSODescriptor.__init__(
      self, id=id, valid_until=valid_until,
      cache_duration=cache_duration,
      protocol_support_enumeration=protocol_support_enumeration,
      error_url=error_url, signature=signature, extensions=extensions,
      key_descriptor=key_descriptor, organization=organization,
      contact_person=contact_person,
      artifact_resolution_service=artifact_resolution_service,
      single_logout_service=single_logout_service,
      manage_name_id_service=manage_name_id_service,
      name_id_format=name_id_format)

    self.want_authn_requests_signed = want_authn_requests_signed
    self.single_sign_on_service = single_sign_on_service or []
    self.name_id_mapping_service = name_id_mapping_service or []
    self.assertion_id_request_service = assertion_id_request_service or []
    self.attribute_profile = attribute_profile or []
    self.attribute = attribute or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

def IDPSSODescriptorFromString(xml_string):
  return saml2.CreateClassFromXMLString(IDPSSODescriptor, xml_string)


class RequestedAttribute(saml.Attribute):

  _tag = 'RequestedAttribute'
  _namespace = MD_NAMESPACE
  _children = saml.Attribute._children.copy()
  _attributes = saml.Attribute._attributes.copy()
  _attributes['isRequired'] = 'is_required'

  def __init__(self, name=None, name_format=None, friendly_name=None,
               attribute_value=None, is_required=None, text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for RequestedAttribute

    Args:
      name: Name attribute
      name_format: NameFormat attribute
      friendly_name: FriendlyName attribute
      attribute_value: AttributeValue elements
      is_required: isRequired attribute
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    saml.Attribute.__init__(self, name=name, name_format=name_format,
                            friendly_name=friendly_name,
                            attribute_value=attribute_value)

    self.is_required = is_required
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

def RequestedAttributeFromString(xml_string):
  return saml2.CreateClassFromXMLString(RequestedAttribute, xml_string)


class ServiceName(localizedName):
  """The md:ServiceName element"""
  _tag = 'ServiceName'
  _namespace = MD_NAMESPACE
  _children = localizedName._children.copy()
  _attributes = localizedName._attributes.copy()

  def __init__(self, lang=None, text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for ServiceName

    Args:
      lang: xml:lang attribute
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    localizedName.__init__(self, lang=lang)
    
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}


def ServiceNameFromString(xml_string):
  return saml2.CreateClassFromXMLString(ServiceName, xml_string)


class ServiceDescription(localizedName):
  """The md:ServiceDescription element"""
  _tag = 'ServiceDescription'
  _namespace = MD_NAMESPACE
  _children = localizedName._children.copy()
  _attributes = localizedName._attributes.copy()

  def __init__(self, lang=None, text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for ServiceDescription

    Args:
      lang: xml:lang attribute
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    localizedName.__init__(self, lang=lang)
    
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}


def ServiceDescriptionFromString(xml_string):
  return saml2.CreateClassFromXMLString(ServiceDescription, xml_string)


class AttributeConsumingService(saml2.SamlBase):
  """The md:AttributeConsumingService element"""
  
  _tag = 'AttributeConsumingService'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()
  _attributes['index'] = 'index'
  _attributes['isDefault'] = 'is_default'
  _children['{%s}ServiceName' % MD_NAMESPACE] = ('service_name', [ServiceName])
  _children['{%s}ServiceDescription' % MD_NAMESPACE] = (
    'service_description', [ServiceDescription])
  _children['{%s}RequestedAttribute' % MD_NAMESPACE] = (
    'requested_attribute', [RequestedAttribute])
  _child_order = ['service_name', 'service_description', 'requested_attribute']

  def __init__(self, index=None, is_default=None, service_name=None,
               service_description=None, requested_attribute=None,
               text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for AttributeConsumingService

    Args:
      index: index attribute
      is_default: isDefault attribute
      service_name: ServiceName elements
      service_descriptor: ServiceDescriptor elements
      requested_attribute: RequestedAttribute elements
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    self.index = index
    self.is_default = is_default
    self.service_name = service_name or []
    self.service_description = service_description or []
    self.requested_attribute = requested_attribute or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

def AttributeConsumingServiceFromString(xml_string):
  return saml2.CreateClassFromXMLString(AttributeConsumingService, xml_string)


class SPSSODescriptor(SSODescriptor):
  """The md:SPSSODescriptor element"""

  _tag = 'SPSSODescriptor'
  _namespace = MD_NAMESPACE
  _children = SSODescriptor._children.copy()
  _attributes = SSODescriptor._attributes.copy()
  _attributes['AuthnRequestsSigned'] = 'authn_requests_signed'
  _attributes['WantAssertionsSigned'] = 'want_assertions_signed'
  _children['{%s}AssertionConsumerService' % MD_NAMESPACE] = (
    'assertion_consumer_service', [AssertionConsumerService])
  _children['{%s}AttributeConsumingService' % MD_NAMESPACE] = (
    'attribute_consuming_service', [AttributeConsumingService])
  
  _child_order = ['signature', 'extensions', 'key_descriptor', 'organization',
                  'contact_person', 'artifact_resolution_service',
                  'single_logout_service', 'manage_name_id_service',
                  'name_id_format', 'assertion_consumer_service',
                  'attribute_consuming_service']

  def __init__(self, id=None, valid_until=None, cache_duration=None,
               protocol_support_enumeration=None, error_url=None,
               signature=None, extensions=None, key_descriptor=None,
               organization=None, contact_person=None,
               artifact_resolution_service=None,
               single_logout_service=None, manage_name_id_service=None,
               name_id_format=None, authn_requests_signed=None,
               want_assertions_signed=None, assertion_consumer_service=None,
               attribute_consuming_service=None,
               text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for IDPSSODescriptor

    Args:
      id: ID attribute
      valid_until: validUntil attribute
      cache_duration: cacheDuration attribute
      protocol_support_enumeration: protocolSupportEnumeration attribute
      error_url: errorURL attribute
      signature: ds:Signature element
      extensions: Extensions element
      key_descriptor: KeyDescriptor elements
      organization: Organization element
      contact_person: ContactPerson elements
      artifact_resolution_service: ArtifactResolutionService elements
      single_logout_service: SingleLogoutService elements
      manage_name_id_service: ManageNameIDService elements
      name_id_format: NameIDFormat elements
      authn_requests_signed: AuthnRequestsSigned attribute
      want_assertions_signed: WantAssertionsSigned attribute
      assertion_consumer_service: AssertionConsumerService elements
      attribute_consuming_service: AttributeConsumingService elements
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """
    SSODescriptor.__init__(
      self, id=id, valid_until=valid_until,
      cache_duration=cache_duration,
      protocol_support_enumeration=protocol_support_enumeration,
      error_url=error_url, signature=signature, extensions=extensions,
      key_descriptor=key_descriptor, organization=organization,
      contact_person=contact_person,
      artifact_resolution_service=artifact_resolution_service,
      single_logout_service=single_logout_service,
      manage_name_id_service=manage_name_id_service,
      name_id_format=name_id_format)

    self.authn_requests_signed = authn_requests_signed
    self.want_assertions_signed = want_assertions_signed
    self.assertion_consumer_service = assertion_consumer_service or []
    self.attribute_consuming_service = attribute_consuming_service or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

def SPSSODescriptorFromString(xml_string):
  return saml2.CreateClassFromXMLString(SPSSODescriptor, xml_string)


class EntityDescriptor(saml2.SamlBase):
  """The md:EntityDescriptor element"""
  #TODO: AuthnAuthorityDescriptor, AttributeAuthorityDescriptor, PDPDescriptor,
  # AffiliationDescriptor is not implemented yet

  _tag = 'EntityDescriptor'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()
  _attributes['entityID'] = 'entity_id'
  _attributes['ID'] = 'id'
  _attributes['validUntil'] = 'valid_until'
  _attributes['cacheDuration'] = 'cache_duration'
  _children['{%s}Signature' % ds.DS_NAMESPACE] = ('signature', ds.Signature)
  _children['{%s}Extensions' % MD_NAMESPACE] = ('extensions', Extensions)
  _children['{%s}RoleDescriptor' % MD_NAMESPACE] = (
    'role_descriptor', [RoleDescriptor])
  _children['{%s}IDPSSODescriptor' % MD_NAMESPACE] = (
    'idp_sso_descriptor', [IDPSSODescriptor])
  _children['{%s}SPSSODescriptor' % MD_NAMESPACE] = (
    'sp_sso_descriptor', [SPSSODescriptor])
  _children['{%s}Organization' % MD_NAMESPACE] = ('organization', Organization)
  _children['{%s}ContactPerson' % MD_NAMESPACE] = (
    'contact_person', [ContactPerson])
  _children['{%s}ContactPerson' % MD_NAMESPACE] = (
    'contact_person', [ContactPerson])
  _children['{%s}AdditionalMetadataLocation' % MD_NAMESPACE] = (
    'additional_metadata_location', [AdditionalMetadataLocation])
  _child_order = ['signature', 'extensions', 'role_descriptor',
                  'idp_sso_descriptor', 'sp_sso_descriptor',
                  'organization', 'contact_person',
                  'additional_metadata_location']

  def __init__(self, entity_id=None, id=None, valid_until=None,
               cache_duration=None,
               signature=None, extensions=None, role_descriptor=None,
               idp_sso_descriptor=None, sp_sso_descriptor=None,
               organization=None, contact_person=None,
               additional_metadata_location=None,
               text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for EntityDescriptor

    Args:
      entity_id: entityID attribute
      id: ID attribute
      valid_until: validUntil attribute
      cache_duration: cacheDuration attribute
      signature: ds:Signature element
      extensions: Extensions element
      role_descriptor: RoleDescriptor elements
      idp_sso_descriptor: IDPSSODescriptor elements
      sp_sso_descriptor: SPSSODescriptor elements
      organization: Organization element
      contact_person: ContactPerson elements
      additional_metadata_location: AdditionalMetadataLocation elements
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """
    self.entity_id = entity_id
    self.id = id
    self.valid_until = valid_until
    self.cache_duration = cache_duration
    self.signature = signature
    self.extensions = extensions
    self.role_descriptor = role_descriptor or []
    self.idp_sso_descriptor = idp_sso_descriptor or []
    self.sp_sso_descriptor = sp_sso_descriptor or []
    self.organization = organization
    self.contact_person = contact_person or []
    self.additional_metadata_location = additional_metadata_location or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
  
def EntityDescriptorFromString(xml_string):
  return saml2.CreateClassFromXMLString(EntityDescriptor, xml_string)


class EntitiesDescriptor(saml2.SamlBase):
  """The md:EntitiesDescriptor element"""

  _tag = 'EntitiesDescriptor'
  _namespace = MD_NAMESPACE
  _children = saml2.SamlBase._children.copy()
  _attributes = saml2.SamlBase._attributes.copy()
  _attributes['name'] = 'name'
  _attributes['ID'] = 'id'
  _attributes['validUntil'] = 'valid_until'
  _attributes['cacheDuration'] = 'cache_duration'
  _children['{%s}Signature' % ds.DS_NAMESPACE] = ('signature', ds.Signature)
  _children['{%s}Extensions' % MD_NAMESPACE] = ('extensions', Extensions)
  _children['{%s}EntityDescriptor' % MD_NAMESPACE] = (
    'entity_descriptor', [EntityDescriptor])
  _child_order = ['signature', 'extensions', 'entity_descriptor',
                  'entities_descriptor']

  def __init__(self, name=None, id=None, valid_until=None,
               cache_duration=None,
               signature=None, extensions=None,
               entity_descriptor=None, entities_descriptor=None,
               text=None,
               extension_elements=None, extension_attributes=None):
    """Constructor for EntitiesDescriptor

    Args:
      name: name attribute
      id: ID attribute
      valid_until: validUntil attribute
      cache_duration: cacheDuration attribute
      signature: ds:Signature element
      extensions: Extensions element
      entity_descriptor: EntityDescriptor elements
      entities_descriptor: EntitiesDescriptor elements
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """
    self.name = name
    self.id = id
    self.valid_until = valid_until
    self.cache_duration = cache_duration
    self.signature = signature
    self.extensions = extensions
    self.entity_descriptor = entity_descriptor or []
    self.entities_descriptor = entities_descriptor or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

EntitiesDescriptor._children['{%s}EntitiesDescriptor' % MD_NAMESPACE] = (
    'entities_descriptor', [EntitiesDescriptor])
  
def EntitiesDescriptorFromString(xml_string):
  return saml2.CreateClassFromXMLString(EntitiesDescriptor, xml_string)


