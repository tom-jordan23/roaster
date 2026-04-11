#ifndef ROASTER_COMMAND_H
#define ROASTER_COMMAND_H

#include <Arduino.h>

// Initialize command interface (serial)
void command_init();

// Check for and process incoming serial commands
void command_update();

// Command format (text-based, newline-terminated):
//   HEAT <0-100>     Set heater duty %
//   BLOW <0-100>     Set blower speed %
//   COOL             Enter cooling mode: heater 0%, blower 100% (DR-005)
//   STATUS           Request current state (one-shot)
//   RESET            Reset safety fault (if conditions clear)
//   STOP             Emergency stop: heater off, blower off
//
// Response format:
//   OK <echo>        Command accepted
//   ERR <message>    Command rejected
//   DATA <csv>       Status response

#endif // ROASTER_COMMAND_H
