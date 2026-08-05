log_to_syslog() {
    if [ -n "$BASH_COMMAND" ] && [[ "$BASH_COMMAND" != "logger"* ]]; then
        logger -p local6.notice -t CLI_AUDIT "[User: $USER] [Dir: $PWD] Command: $BASH_COMMAND"
    fi
}
# Trap every command before execution
trap 'log_to_syslog' DEBUG

