<%include file="../header.html"/>

<div class="span-16">
<h1 class="fancy">${name}</h1>

<p>
Flow supported as specified in the <a href="http://tools.ietf.org/html/draft-ietf-oauth-v2-02#section-3.5.1"> User Agent Flow Spec</a>.
</p>

<form action="/oauth2/testauthorize">
<div class="note">Required for protocol request</div>
<label>Client ID</label> <input type="text" name="client_id" size="90" /> <br />
<label>Type</label> <input type="text" name="type" value="user_agent" disabled /> <br />
<label>State</label> <input type="text" name="state" size="90" /> <br />
<label>Scope (space delimited)</label> <input type="text" name="scope" size="90" /> <br />
<label>Immediate (true or false)</label> <input type="text" name="immediate" value="false" size="20" /> <br />
<label>Redirect URI</label> <input type="text" name="redirect_uri" value="http://127.0.0.1:9080/oauth2/callback" /><br />
<label>Secret Type</label> <input type="text" name="secret_type" /><br />

<div class="note">Required for test processing</div>
<label>Shared Secret</label> <input type="text" name="shared_secret" size="90" /> <br />
<label>Base URL</label> <input type="text" name="base_url" size="40"/><br />

Example request from submission:
GET /authorize?type=user_agent&client_id=s6BhdRkqt3&
         redirect_uri=https%3A%2F%2FEexample%2Ecom%2Frd HTTP/1.1

<input type="submit" value="send redirect" />
</form>

</div>
<div class="span-7 last">
    <p>&nbsp;</p>
   <p class="fancy large"> </p>
</div>


<%include file="../footer.html"/>
