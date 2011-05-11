<%include file="../header.html"/>

<h1 class="fancy">${name}</h1>

<div class="span-12">
<fieldset> 
    <legend>${name}</legend> 
    
    <p>
    Flow supported as specified in the <a href="http://tools.ietf.org/html/draft-ietf-oauth-v2-02#section-3.5.2"> Web Server Flow Spec</a>.
    </p>

    <form action="/oauth2/testauthorize">
<div class="info">Required for protocol request</div>
<p>
<label>Client id</label><br /><input type="text" name="client_id" size="90" />
</p>
<p>
<label>Type</label><br /><input type="text" name="type" value="web_server" disabled />
</p>
<p>
<label>State</label><br /><input type="text" name="state" size="90" />
</p>
<p>
<label>Scope (space delimited)</label><br /><input type="text" name="scope" size="90" />
</p>
<p>
<label>Immediate (true or false)</label><br /><input type="text" name="immediate" value="false" size="20" />
</p>
<p>
<label>Redirect URI</label><br /><input type="text" name="redirect_uri" value="http://127.0.0.1:9080/oauth2/callback" />
</p>


<div class="info">Required for test processing</div>
<p>
<label>Shared Secret</label><br /><input type="text" name="shared_secret" size="90" />
</p>
<p>
<label>Base URL</label><br /><input type="text" name="base_url" size="40"/></p>
<p>
<label>Suffix Override</label><br /><input type="text" name="suffix_override" size="40"/></p>


Example request from submission:
GET /authorize?type=web_server&client_id=s6BhdRkqt3&redirect_uri=
         https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb HTTP/1.1
<p>
<input type="submit" value="send redirect" />
</p>
</form>
</formset>
</div>



<%include file="../footer.html"/>
