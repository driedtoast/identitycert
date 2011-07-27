<%include file="/header.html"/>


<h1 class="fancy">Certification List</h1>
<div class="span-12">

<a href="/cert/add">Add a Cert</a>

<fieldset>
    <legend>List of certs<legend>
    % for cert in certs:
 <p> <label>${cert}:</label> <a href="/static/keys/${cert}/public.pem">public key</a> |  <a href="/static/keys/${cert}/private.pem">private key</a>  </p>
    % endfor
</fieldset>

</div>


<%include file="/footer.html"/>
