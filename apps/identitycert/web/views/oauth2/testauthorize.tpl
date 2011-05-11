<%include file="../header.html"/>

<div class="span-16">
<h1 class="fancy">URL in the redirect</h1>

<p>
% if token != UNDEFINED:
Request Token: ${token} <br />
% endif
% if secret != UNDEFINED:
Request Token Secret: ${secret} 
% endif
</p>
<p>
Click on the link below to redirect to the next step of the oauth process.
This normally will happen without a click, but this gives you a chance to review the link values.
</p>

<a href="${link}">${link}</a>

</div>
<div class="span-7 last">
    <p>&nbsp;</p>
   <p class="fancy large"> </p>
</div>


<%include file="../footer.html"/>
