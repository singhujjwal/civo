#!/bin/bash

random-string() {
        cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w ${1:-32} | head -n 1
}

# run_test() {
# curl -X 'POST' \
#   'http://74.220.23.25:8121/api/v1/urls/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{"longUrl": "'$val'"}'

# }


run_test() {
  
  echo "The random string is $1"
  curl -X 'POST' \
  'http://url.vm.singhjee.in:8121/api/v1/urls/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"longUrl": "'$1'"}'

}


# The passed parameters are $1, $2, $3 … $n, corresponding to the position of the parameter after the function’s name.
# The $0 variable is reserved for the function’s name.
# The $# variable holds the number of positional parameters/arguments passed to the function.
# The $* and $@ variables hold all positional parameters/arguments passed to the function.
# When double-quoted, "$*" expands to a single string separated by space (the first character of IFS) - "$1 $2 $n".
# When double-quoted, "$@" expands to separate strings - "$1" "$2" "$n".
# When not double-quoted, $* and $@ are the same.

# for i in {1..100} 
for i in  {1..100}
  do
    func_result="https://$(random-string).com"
    run_test "$func_result"
  done
