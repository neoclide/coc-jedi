let s:root = expand('<sfile>:h:h:h')
let s:client = v:null

function! coc#jedi#start_server()
  if !empty(s:client) | return | endif
  let prog = s:get_python_prog()
  if empty(prog) | return | endif
  let cmd = [prog, s:root.'/python/server.py']
  let s:client = coc#client#create('jedi', cmd)
  call s:client['start']()
endfunction

function! s:get_python_prog()
  let prog = get(g: ,'python3_host_prog', get(g:, 'python_host_prog', ''))
  if !empty(prog)
    return prog
  endif
  if executable('python3')
    return 'python3'
  endif
  if executable('python')
    return 'python'
  endif
  echohl Error | echon '[coc-jedi] executable python not found' | echohl None
endfunction

function! coc#jedi#request(method, args) abort
  if empty(s:client) | return | endif
  call s:client['request'](a:method, a:args)
endfunction

function! coc#jedi#notify(method, args) abort
  if empty(s:client) | return | endif
  call s:client['notify'](a:method, a:args)
endfunction

function! coc#jedi#request_async(method, args, cb) abort
  if empty(s:client) | return | endif
  call s:client['request_async'](a:method, a:args, a:cb)
endfunction

" called by server
function! coc#jedi#async_response(id, resp, isErr) abort
  if empty(s:client) | return | endif
  call s:client['on_async_response'](a:id, a:resp, a:isErr)
endfunction
