<%include file="../header.html"/>


<h1 class="fancy">Callback Status</h1>
<div class="span-12">

<fieldset>
    <legend>return values<legend>
% if code != UNDEFINED:
 <p> <label>Code returned is:</label> ${code} </p>
% endif


% if state != UNDEFINED:
 <p><label>State</label> :  ${state} </p>
% endif

% if access_token != UNDEFINED:
 <p>Access Token :  ${access_token} </p>
% endif
% if refresh_token != UNDEFINED:
 <p>Refresh Token :  ${refresh_token} </p>
% endif

% if error != UNDEFINED:
 <p class="error">Error :  ${error} </p>
% endif
% if error_description != UNDEFINED:
 <p class="error">Error Description :  ${error_description} </p>
% endif
</fieldset>
<fieldset>
    <legend>test values<legend>
% if client_id != UNDEFINED:
  <p><label>Consumer Key used:</label>  ${client_id} </p>
% endif

</fieldset>

</div>


<%include file="../footer.html"/>
