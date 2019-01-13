from burp import IBurpExtender
from burp import IMessageEditorTabFactory
from burp import IMessageEditorTab
from burp import IParameter
from burp import IHttpListener

# Parsia: modified "custom editor tab" https://github.com/PortSwigger/example-custom-editor-tab/.
# Parsia: for burp-exceptions - see https://github.com/securityMB/burp-exceptions

from exceptions_fix import FixBurpExceptions
import sys

from library import *

class BurpExtender(IBurpExtender, IMessageEditorTabFactory, IHttpListener):
    
    #
    # implement IBurpExtender
    #
    
    def registerExtenderCallbacks(self, callbacks):
        # keep a reference to our callbacks object
        self._callbacks = callbacks
        
        self._helpers = callbacks.getHelpers()      
        callbacks.setExtensionName("Caidao Crypto(AES)")
        
        # register ourselves as a message editor tab factory
        callbacks.registerMessageEditorTabFactory(self)
        
        # add http listener
        callbacks.registerHttpListener(self)

        # Parsia: for burp-exceptions
        sys.stdout = callbacks.getStdout()
        
        print("Caidao Crypto(AES) is ready")
        
    # 
    # implement IMessageEditorTabFactory
    #
    
    def createNewInstance(self, controller, editable):
        # create a new instance of our custom editor tab
        return CryptoTab(self, controller, editable)
        
#
    # implement IHttpListener
    #
    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        key = "0123456789012345"
        iv = "9876543210987654"
        
        # only process requests
        if messageIsRequest:
            
            info = getInfo(messageInfo, messageIsRequest, self._helpers)
            headers = info.getHeaders()
        
            # get the body
            body = getBody(messageInfo.getRequest(), messageIsRequest, self._helpers)
            
            # encrypt the caidao post body
            encryptedBody = encryptJython(body, key, iv)
        
            newMSG = self._helpers.buildHttpMessage(headers, encryptedBody)
            messageInfo.setRequest(newMSG)
        else:
        
            info = getInfo(messageInfo.getResponse(), messageIsRequest, self._helpers)
            headers = info.getHeaders()
        
            # get the body
            body = getBody(messageInfo.getResponse(), messageIsRequest, self._helpers)
            
            # decrypt the aes body
            decryptedBody = decryptJython(body, key, iv)
        
            newMSG = self._helpers.buildHttpMessage(headers, decryptedBody)
            messageInfo.setResponse(newMSG)
            
# 
# class implementing IMessageEditorTab
#

class CryptoTab(IMessageEditorTab):
    def __init__(self, extender, controller, editable):
        self._extender = extender
        self._editable = editable
        # Parsia: Burp helpers object
        self.helpers = extender._helpers

        # create an instance of Burp's text editor, to display our decrypted data
        self._txtInput = extender._callbacks.createTextEditor()
        self._txtInput.setEditable(editable)
        
    #
    # implement IMessageEditorTab
    #

    def getTabCaption(self):
        # Parsia: tab title
        return "Caidao Crypto(AES)"
        
    def getUiComponent(self):
        return self._txtInput.getComponent()
        
    def isEnabled(self, content, isRequest):
        return True
    
    def isModified(self):
        return self._txtInput.isTextModified()
    
    def getSelectedData(self):
        return self._txtInput.getSelectedText()
        
    def setMessage(self, content, isRequest):
        if content is None:
            # clear our display
            self._txtInput.setText(None)
            self._txtInput.setEditable(False)
        
        # Parsia: if tab has content
        else:
            # get the body
            body = getBody(content, isRequest, self.helpers)
            # decrypt does the base64 decoding so the extension does not have to
            key = "0123456789012345"
            iv = "9876543210987654"
            decryptedBody = encryptJython(body, key, iv)
            # set the body as text of message box
            self._txtInput.setText(decryptedBody)
            # this keeps the message box edit value to whatever it was
            self._txtInput.setEditable(self._editable)
        
        # remember the displayed content
        self._currentMessage = content
    
    def getMessage(self):
        # determine whether the user modified the data
        if self._txtInput.isTextModified():
            # Parsia: if text has changed, encode it and make it the new body of the message
            modified = self._txtInput.getText()
            # encrypt and decrypt do the base64 transformation
            key = "0123456789012345"
            iv = "9876543210987654"
            encryptedModified = encryptJython(modified, key, iv)
            
            # Parsia: create a new message with the new body and return that
            info = getInfo(self._currentMessage, True, self.helpers)
            headers = info.getHeaders()
            return self.helpers.buildHttpMessage(headers, encryptedModified)
        else:
            # Parsia: if nothing is modified, return the current message so nothing gets updated
            return self._currentMessage

# Parsia: for burp-exceptions
FixBurpExceptions()
