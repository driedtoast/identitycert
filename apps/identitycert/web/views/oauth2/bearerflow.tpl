<%include file="../header.html"/>

<h1 class="fancy">${name}</h1>

<div class="span-12">

<p>
Bearer supported as specified in the <a href="http://self-issued.info/docs/draft-jones-json-web-token-01.html">JWT Bearer Spec</a>.
</p>

<form action="/oauth2/bearerflow/submit">
<fieldset> 
    <legend>For normal protocol request</legend> 
    <p>
    <label>Username (prn) </label><br /><input type="text" name="username" size="90" />
    </p>
    <p>
    <label>Domain (aud)</label><br /><input type="text" name="aud" size="90" value="" />
    </p>
    <p>
    <label>Client id (iss)</label><br /><input type="text" name="client_id" size="90" />
    </p>
    <p>
    <label>State</label><br /><input type="text" name="state" size="90" />
    </p>
    <p>
    <label>Scope (space delimited)</label><br /><input type="text" name="scope" size="90" />
    </p>
</fieldset>
<fieldset>
    <legend>Required for test processing</legend> 
    <p>
    <label>Shared Secret for HMAC</label><br /><input type="text" name="shared_secret" size="90" />
    </p>
    <p>
    <label>Private Key(pem) for RSA</label><br /><input type="file" name="private_key" size="90" />
    </p>
    <p>
    <label>Public Key(pem) for RSA</label><br /><input type="file" name="public_key" size="90" />
    </p>
    <p>
    <label>Bearer Token</label><br />
        <select name="token_type">
            <option value=""> none </option>
            <option value="jwt">JWT</option>
            <option value="saml">SAML Assertion</option>
        </select>
    </p>
    <p>
    <label>Base URL</label><br /><input type="text" name="base_url" size="90"/></p>
    <p>
    <label>Suffix Override</label><br /><input type="text" name="suffix_override" size="40"/></p>
</fieldset>

<p>
<input type="submit" value="send redirect" />
</p>
</form>
</div>

<div class="span-24 last">
    <div class="notice">
    Example request from submission:
    GET /authorize?type=web_server&client_id=s6BhdRkqt3&redirect_uri=
             https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb HTTP/1.1
    </div>
</div>

<%include file="../footer.html"/>
