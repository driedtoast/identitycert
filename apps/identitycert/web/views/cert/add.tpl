<%include file="/header.html"/>

<h1 class="fancy">${name}</h1>

<div class="span-12">

<p>
Add cert to the list.
</p>

<form action="/cert/save" >
<fieldset> 
    <p>
    <label>Cert name </label><br /><input type="text" name="name" size="90" />
    </p>
</fieldset>

<p>
<input type="submit" value="send redirect" />
</p>
</form>
</div>


<%include file="/footer.html"/>
