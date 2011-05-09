<%include file="header.html"/>

<div class="span-16">
<h1 class="fancy">OAuth 2 Flows</h1>
OAuth 2 Flows are derived from: <a href="http://hueniverse.com/2010/05/introducing-oauth-2-0/">hueuniverse oauth intro</a>.
<ul>
<li><a href="/oauth2/useragentflow">User-Agent Flow</a> – for clients running inside a user-agent (typically a web browser).</li>
<li><a href="/oauth2/webserverflow">Web Server Flow</a> – for clients that are part of a web server application, accessible via HTTP requests. This is a simpler version of the flow provided by OAuth 1.0.</li>
<li><a href="/oauth2/deviceflow">Device Flow</a> – suitable for clients executing on limited devices, but where the end-user has separate access to a browser on another computer or device.</li>
<li><a href="/oauth2/usernamepasswordflow">Username and Password Flow</a> – used in cases where the user trusts the client to handle its credentials but it is still undesirable for the client to store the user’s username and password.  This flow is only suitable when there is a high degree of trust between the user and the client.</li>
<li><a href="/oauth2/clientcredentialsflow">Client Credentials Flow</a> – the client uses its credentials to obtain an access token. This flow supports what is known as the 2-legged scenario.</li>
<li><a href="/oauth2/assertionflow">Assertion Flow</a> – the client presents an assertion such as a SAML assertion to the authorization server in exchange for an access token.</li>
</ul>

</div>
<div class="span-7 last">
    <p>&nbsp;</p>
   <p class="fancy large"> </p>
</div>


<%include file="footer.html"/>