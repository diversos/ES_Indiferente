<form action="/ticket/{{get('id_ticket', '')}}/action/forward?o={{get('username_id', '')}}&email={{get('email', '')}}" method="post">
    Comment:
    <input name="comment" type="text" value="{{get('comment', '')}}"/>
    <br>
    <input value="Submit" type="submit"/>
</form>
