% max_len = 30

<!--Falta redirecionar isto para a página anterior-->
<p><a href="asdasdasd">Back</a></p>
<p><b> Basic Ticket Properties</b></p>
<p><i>Ticket ID:</i> {{ticket['id']}}
<br><i>Queue:</i> {{ticket['queue']}}
<br><i>Owner:</i> {{ticket['owner']}}
<br><i>Creator:</i> {{ticket['creator']}}
<br><i>Status:</i> {{ticket['status']}}
<br><i>Priority:</i> {{ticket['priority']}}
<br><i>Time Worked:</i> {{ticket['timeworked']}}
<br><i>Created:</i> {{ticket['created']}}
<br><i>Due:</i> {{ticket['due']}}
<br><i>Resolved:</i> {{ticket['resolved']}}
<br><i>Requestor:</i> {{ticket['requestors']}}
<br><i>Subject:</i> {{ticket['subject']}}</p>
<p></p>
<p><b>Links</b></p>
<p>{{links}}</p>
<p><b>History</b></p>
<p>
% for d in history:
<br><i>Time Taken:</i> {{d['timetaken']}}
<br><i>Type:</i> {{d['type']}}
<br><i>Field:</i> {{d['field']}}
<br><i>Old Value:</i> {{d['oldvalue']}}
<br><i>New Value:</i> {{d['newvalue']}}
<br><i>Data:</i> {{d['data']}}
<br><i>Description:</i> {{d['description']}}
<br><i>Content:</i> {{d['content']}}
<br><i>Creator:</i> {{d['creator']}}
<br><i>Created:</i> {{d['created']}}</p>
% end
<br>
</p>
