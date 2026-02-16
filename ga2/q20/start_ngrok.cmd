@echo off
ngrok http 11434 ^
  --response-header-add "X-Email: 23f3001415@ds.study.iitm.ac.in" ^
  --response-header-add "X-User-Email: 23f3001415@ds.study.iitm.ac.in" ^
  --response-header-add "Access-Control-Expose-Headers: *" ^
  --response-header-add "Access-Control-Allow-Origin: *" ^
  --response-header-add "Access-Control-Allow-Headers: *"
