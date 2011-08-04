
import libxml2, sys

import xmlsec


secinit = False

def init():
    global secinit
    if secinit:
        return
    # Init libxml library
    libxml2.initParser()
    libxml2.substituteEntitiesDefault(1)

    # Init xmlsec library
    if xmlsec.init() < 0:
        print "Error: xmlsec initialization failed."
        return sys.exit(-1)
    
    # Check loaded library version
    if xmlsec.checkVersion() != 1:
	print "Error: loaded xmlsec library version is not compatible.\n"
	sys.exit(-1)

    # Init crypto library
    if xmlsec.cryptoAppInit(None) < 0:
        print "Error: crypto initialization failed."
    
    # Init xmlsec-crypto library
    if xmlsec.cryptoInit() < 0:
        print "Error: xmlsec-crypto initialization failed."
    secinit = True


def signXml(xmlStr, key_file,cert_file, id=None ):
    init()
    result = None
    doc = libxml2.parseDoc(xmlStr)
    if doc is None or doc.getRootElement() is None:
	print "Error: unable to parse file \"%s\"" % xml_file
        cleanup(doc)
        return result

    # Create signature template for RSA-SHA1 enveloped signature
    signNode = xmlsec.TmplSignature(doc, xmlsec.transformExclC14NId(),
                                    xmlsec.transformRsaSha1Id(), id)
    #signNode.setNs('ds')
    if signNode is None:
        print "Error: failed to create signature template"
        cleanup(doc)
        return result
    
    # Add <dsig:Signature/> node to the doc
    doc.getRootElement().addChild(signNode)

    # Add reference
    refNode = signNode.addReference(xmlsec.transformSha1Id(),
                                    None, None, None)
    if refNode is None:
        print "Error: failed to add reference to signature template"
        cleanup(doc)
        return result

    # Add enveloped transform
    if refNode.addTransform(xmlsec.transformEnvelopedId()) is None:
        print "Error: failed to add enveloped transform to reference"
        cleanup(doc)
        return result

    # Add <dsig:KeyInfo/> and <dsig:X509Data/>
    keyInfoNode = signNode.ensureKeyInfo(None)
    if keyInfoNode is None:
        print "Error: failed to add key info"
        cleanup(doc)
        return result
    
    if keyInfoNode.addX509Data() is None:
        print "Error: failed to add X509Data node"
        cleanup(doc)
        return result

    # Create signature context, we don't need keys manager in this example
    dsig_ctx = xmlsec.DSigCtx()
    if dsig_ctx is None:
        print "Error: failed to create signature context"
        cleanup(doc)
        return result

    # Load private key, assuming that there is not password
    key = xmlsec.cryptoAppKeyLoad(key_file, xmlsec.KeyDataFormatPem,
                                  None, None, None)
    if key is None:
        print "Error: failed to load private pem key from \"%s\"" % key_file
        cleanup(doc, dsig_ctx)
        return result
    dsig_ctx.signKey = key

    # Load certificate and add to the key
    if xmlsec.cryptoAppKeyCertLoad(key, cert_file, xmlsec.KeyDataFormatPem) < 0:
        print "Error: failed to load pem certificate \"%s\"" % cert_file
        cleanup(doc, dsig_ctx)
        return result

    # Set key name to the file name, this is just an example!
    #if key.setName(key_file) < 0:
    #   print "Error: failed to set key name for key from \"%s\"" % key_file
    #    cleanup(doc, dsig_ctx)
    #   return result

    # Sign the template
    print signNode
    if dsig_ctx.sign(signNode) < 0:
        print "Error: signature failed"
        cleanup(doc, dsig_ctx)
        return result

    # Print signed document to stdout
    #doc.dump("-")
    result = doc.serialize()
    # Success
    cleanup(doc, dsig_ctx, 1)
    return result


def cleanup(doc=None, dsig_ctx=None, res=-1):
    if dsig_ctx is not None:
        dsig_ctx.destroy()
    if doc is not None:
        doc.freeDoc()
    return res