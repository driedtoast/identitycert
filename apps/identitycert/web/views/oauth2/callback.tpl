<%include file="/header.html"/>


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

<fieldset>
    <legend>actual response<legend>
% if actual_response != UNDEFINED:
  <p>${actual_response} </p>
% endif

</fieldset>


<fieldset>
    <legend>input values<legend>
% if url_used != UNDEFINED:
  <p><label>Request Url:</label>  ${url_used} </p>
% endif
% if assertion != UNDEFINED:
  <p><label>Assertion Value:</label>  ${assertion} </p>
% endif


% if grant_type != UNDEFINED:
  <p><label>Grant Type:</label>  ${grant_type} </p>
% endif

% if code != UNDEFINED:
  <p><label>CODE:</label>  ${code} </p>
% endif



</fieldset>

</div>


<%include file="/footer.html"/>
