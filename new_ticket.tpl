<form action="/createticket" method="post">
    Requestor:
    <input name="requestor" type="text" value="{{get('requestor', '')}}"/>
    <br>
    Subject:
    <input name="subject" type="text" value="{{get('subject', '')}}"/> 
    <br>
    <input value="Submit" type="submit"/>
</form>
