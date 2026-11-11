// station-sync.js
// legacy heartbeat client broken since gateway migration
// relay health checks 
4@?DE vp%t(p*      b5 a_ aa e` cg da b_ eb cc e7 fe c4 ba fg fe ec fh b` b_ e` df da e4 c4 df fg eh c4 e5 c6 b_ d2 eh bd e2 eb ba ce bb c4 e5 e4 fe c7 e2 ef ff c7 cc c` fe eb bb da eg ec cf e4 fe ea eh bh e2 e` cf de e2 e` ba e4 fd aa b3

const REQUIRED_AGENT =

function renderStatus(isUp) {
 cntlgt=dcmn.eEeetyd"ttslgt)
 os et=dcmn.eEeetyd"ttstx"; lgtcasae=iU  u":"on; tx.etotn  sse tts   iU  oln":"fln";os ih  ouetgtlmnBI(sau-ih"; cnttx  ouetgtlmnBI(sau-et)
 ih.lsNm  sp?"p  dw"
 ettxCnet="ytmsau:"+(sp?"nie  ofie)
}

fetch(GATEWAY, {
  method: "POST",
  body: "action=checkin"
})
  .then(r => r.json())
  .then(d => renderStatus(d.result === "up"))
  .catch(() => renderStatus(false));

setInterval(() => renderStatus(false), 30000);
