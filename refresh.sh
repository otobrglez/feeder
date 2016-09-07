#!/usr/bin/env bash
set -ex

LOG_LEVEL=WARNING
MODE=refresh

COMMANDS=(
  "24ur -a mode=$MODE -a categories=novice/gospodarstvo -a pages=5 -L $LOG_LEVEL"
  "24ur -a mode=$MODE -a categories=novice/slovenija -a pages=5 -L $LOG_LEVEL"
  "24ur -a mode=$MODE -a categories=novice/svet -a pages=5 -L $LOG_LEVEL"
  "delo -a mode=$MODE -a categories=novice,gospodarstvo -a pages=3 -L $LOG_LEVEL"
  "delo -a mode=$MODE -a categories=novice -a pages=3 -L $LOG_LEVEL"
  "delo -a mode=$MODE -a categories=gospodarstvo -a pages=3 -L $LOG_LEVEL"
  "delo -a mode=$MODE -a categories=svet -a pages=3 -L $LOG_LEVEL"
)

parallel --verbose --progress --colsep ' ' scrapy crawl {.} ::: "${COMMANDS[@]}"
