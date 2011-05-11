<%include file="../header.html"/>


<h1 class="fancy">URL in the redirect</h1>
<div class="span-24 last">

<fieldset>
% if token != UNDEFINED:
<p><label>Request Token:</label> ${token} </p>
% endif
% if secret != UNDEFINED:
<p><label>Request Token Secret:</label> ${secret} </p>
% endif
</fieldset>

<div class="info">
Click on the link below to redirect to the next step of the oauth process.
This normally will happen without a click, but this gives you a chance to review the link values.
</div>
<p>
<a href="${link}">${link}</a>
</p>

</div>

<%include file="../footer.html"/>
