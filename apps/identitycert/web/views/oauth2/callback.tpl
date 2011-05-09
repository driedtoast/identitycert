<%include file="../header.html"/>

<div class="span-16">
<h1 class="fancy">${name}</h1>


<p> user agent grants expects</p>

access_token
         REQUIRED.  The access token.

   expires_in
         OPTIONAL.  The duration in seconds of the access token
         lifetime.

   refresh_token
         OPTIONAL.  The refresh token.

   state
         REQUIRED if the "state" parameter was present in the client
         authorization request.  Set to the exact value received from
         the client.

   access_token_secret
         REQUIRED if requested by the client.  The corresponding access
         token secret as requested by the client.


<p> user agent denies expects</p>
 error
         REQUIRED.  The parameter value MUST be set to "user_denied".

   state
         REQUIRED if the "state" parameter was present in the client
         authorization request.  Set to the exact value received from
         the client.


</div>
<div class="span-7 last">
    <p>&nbsp;</p>
   <p class="fancy large"> </p>
</div>


<%include file="../footer.html"/>