if exists('did_coc_jedi_loaded') || v:version < 700
  finish
endif
let did_coc_jedi_loaded = 1

let s:folder = expand('<sfile>:h:h')

call coc#util#regist_extension(s:folder)

augroup coc_jedi
  autocmd!
  autocmd FileType python call coc#jedi#start_server()
augroup end

if get(v:, 'vim_did_enter', 0)
  call coc#jedi#start_server()
endif
