#!/usr/bin/env bats

@test "init_cphp_env" {
     [ "${CONTINUOUSPHP}" = "continuousphp" ]
     [ "${TERM}" = "xterm" ]
     [ "${WHITE}" = "\x1B033[0;02m" ]
     [ "${GREEN}" = "\x1B[1;32m" ]
     [ "${RED}" = "\x1B[1;31m" ]
     [ "${YELLOW}" = "\x1B[1;33m" ]
     [ "${BLUE}" = "\x1B[1;34m" ]
     [ "${PINK}" = "\x1B[1;35m" ]
     [ "${CYAN}" = "\x1B[1;36m" ]
     [ "${NORMAL}" = "\x1B[0;39m" ]
}