/* Limited SSD1327 I2C framebuffer model for Cece. Implements the command
 * and data sequences emitted by the Adafruit 128x128 driver, not the complete
 * hardware. Wokwi only; not firmware for the ESP32. */
#include "wokwi-api.h"
#include <stdint.h>
#include <stdbool.h>

typedef struct {
  buffer_t fb;
  uint8_t first, data_mode, cmd, remaining, arg_index;
  uint8_t col0, col1, row0, row1, col, row;
} state_t;
static state_t s;

static bool connect_cb(void *user, uint32_t address, bool read) {
  state_t *d = user; (void)address; if (read) return false; d->first=1; return true;
}
static uint8_t argc_for(uint8_t cmd) {
  if (cmd==0x15 || cmd==0x75) return 2;
  switch(cmd) { case 0x81: case 0xA0: case 0xA1: case 0xA2: case 0xA8:
    case 0xB1: case 0xB3: case 0xAB: case 0xB6: case 0xBE: case 0xBC:
    case 0xD5: case 0xFD: return 1; default: return 0; }
}
static bool write_cb(void *user, uint8_t v) {
  state_t *d=user;
  if (d->first) { d->first=0; d->data_mode=(v & 0x40) != 0; return true; }
  if (!d->data_mode) {
    if (!d->remaining) { d->cmd=v; d->remaining=argc_for(v); d->arg_index=0; return true; }
    if (d->cmd==0x15) { if(!d->arg_index) d->col0=v; else { d->col1=v; d->col=d->col0; } }
    if (d->cmd==0x75) { if(!d->arg_index) d->row0=v; else { d->row1=v; d->row=d->row0; } }
    d->arg_index++; d->remaining--; return true;
  }
  if (d->col<64 && d->row<128) {
    uint8_t hi=(v>>4)*17, lo=(v&15)*17;
    uint8_t px[8]={hi,hi,hi,255,lo,lo,lo,255};
    buffer_write(d->fb, ((uint32_t)d->row*128 + (uint32_t)d->col*2)*4, px, 8);
  }
  if (++d->col>d->col1) { d->col=d->col0; if (++d->row>d->row1) d->row=d->row0; }
  return true;
}
void chip_init(void) {
  uint32_t w,h; s.fb=framebuffer_init(&w,&h); s.col1=63; s.row1=127;
  const i2c_config_t i2c={.address=0x3d,.scl=pin_init("SCL",INPUT_PULLUP),
    .sda=pin_init("SDA",INPUT_PULLUP),.connect=connect_cb,.write=write_cb,.user_data=&s};
  i2c_init(&i2c);
}
