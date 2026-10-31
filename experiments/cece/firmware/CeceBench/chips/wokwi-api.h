#include <stdint.h>
#include <stdbool.h>

#ifndef WOKWI_API_H
#define WOKWI_API_H

enum pin_value {
  LOW = 0,
  HIGH = 1
};

enum pin_mode {
  INPUT = 0,
  OUTPUT = 1,
  INPUT_PULLUP = 2,
  INPUT_PULLDOWN = 3,
  ANALOG = 4,

  OUTPUT_LOW = 16,
  OUTPUT_HIGH = 17,
};

enum edge {
  RISING = 1,
  FALLING = 2,
  BOTH = 3,
};

int __attribute__((export_name("__wokwi_api_version_1"))) __attribute__((weak)) __wokwi_api_version_1(void) { return 1; }

#ifdef __cplusplus
extern "C" {
#endif

typedef int32_t pin_t;
#define NO_PIN ((pin_t)-1)

typedef struct {
  void *user_data;
  uint32_t edge;
  void (*pin_change)(void *user_data, pin_t pin, uint32_t value);
} pin_watch_config_t;

extern __attribute__((export_name("chipInit"))) void chip_init(void);

extern __attribute__((import_name("pinInit"))) pin_t pin_init(const char *name, uint32_t mode);

extern __attribute__((import_name("pinRead"))) uint32_t pin_read(pin_t pin);
extern __attribute__((import_name("pinWrite"))) void pin_write(pin_t pin, uint32_t value);
extern __attribute__((import_name("pinWatch"))) bool pin_watch(pin_t pin, const pin_watch_config_t *config);
extern __attribute__((import_name("pinWatchStop"))) void pin_watch_stop(pin_t pin);
extern __attribute__((import_name("pinMode"))) void pin_mode(pin_t pin, uint32_t value);
extern __attribute__((import_name("pinADCRead"))) float pin_adc_read(pin_t pin);
extern __attribute__((import_name("pinDACWrite"))) float pin_dac_write(pin_t pin, float voltage);

typedef uint32_t string_t;
#define STRING_NULL 0

extern __attribute__((import_name("stringGetLength"))) uint32_t string_get_length(string_t string);
extern __attribute__((import_name("stringRead"))) uint32_t string_read(string_t string, char *buf, uint32_t buffer_size);

extern __attribute__((import_name("attrInit"))) uint32_t attr_init(const char *name, uint32_t default_value);
extern __attribute__((import_name("attrInitFloat"))) uint32_t attr_init_float(const char *name, float default_value);
extern __attribute__((import_name("attrRead"))) uint32_t attr_read(uint32_t attr_id);
extern __attribute__((import_name("attrReadFloat"))) float attr_read_float(uint32_t attr_id);
extern __attribute__((import_name("attrStringInit"))) string_t attr_string_init(const char *name);

typedef struct {
  void *user_data;
  uint32_t address;
  pin_t scl;
  pin_t sda;
  bool (*connect)(void *user_data, uint32_t address, bool connect);
  uint8_t (*read)(void *user_data);
  bool (*write)(void *user_data, uint8_t data);
  void (*disconnect)(void *user_data);
  uint32_t reserved[8];
} i2c_config_t;

typedef uint32_t i2c_dev_t;

extern __attribute__((import_name("i2cInit"))) i2c_dev_t i2c_init(const i2c_config_t *config);

typedef struct {
  void *user_data;
  pin_t rx;
  pin_t tx;
  uint32_t baud_rate;
  void (*rx_data)(void *user_data, uint8_t byte);
  void (*write_done)(void *user_data);
  uint32_t reserved[8];
} uart_config_t;

typedef uint32_t uart_dev_t;

extern __attribute__((import_name("uartInit"))) uart_dev_t uart_init(const uart_config_t *config);
extern __attribute__((import_name("uartWrite"))) bool uart_write(uart_dev_t uart, uint8_t *buffer, uint32_t count);

typedef struct {
  void *user_data;
  pin_t sck;
  pin_t mosi;
  pin_t miso;
  uint32_t mode;
  void (*done)(void *user_data, uint8_t *buffer, uint32_t count);
  uint32_t reserved[8];
} spi_config_t;
typedef uint32_t spi_dev_t;

extern __attribute__((import_name("spiInit"))) spi_dev_t spi_init(const spi_config_t *spi_config);
extern __attribute__((import_name("spiStart"))) void spi_start(const spi_dev_t spi, uint8_t *buffer, uint32_t count);
extern __attribute__((import_name("spiStop"))) void spi_stop(const spi_dev_t spi);

typedef struct {
  void *user_data;
  void (*callback)(void *user_data);
  uint32_t reserved[8];
} timer_config_t;

typedef uint32_t timer_t;

extern __attribute__((import_name("timerInit"))) timer_t timer_init(const timer_config_t *config);
extern __attribute__((import_name("timerStart"))) void timer_start(const timer_t timer, uint32_t micros, bool repeat);
extern __attribute__((import_name("timerStartNanos"))) void timer_start_ns_d(const timer_t timer, double nanos, bool repeat);
static void timer_start_ns(const timer_t timer, uint64_t nanos, bool repeat) {
  timer_start_ns_d(timer, (double)nanos, repeat);
}
extern __attribute__((import_name("timerStop"))) void timer_stop(const timer_t timer);

extern __attribute__((import_name("getSimNanos"))) double get_sim_nanos_d(void);

static uint64_t get_sim_nanos(void) {
  return (uint64_t)get_sim_nanos_d();
}

typedef uint32_t buffer_t;
extern __attribute__((import_name("framebufferInit"))) buffer_t framebuffer_init(uint32_t *pixel_width, uint32_t *pixel_height);
extern __attribute__((import_name("bufferRead"))) void buffer_read(buffer_t buffer, uint32_t offset, uint8_t *data, uint8_t data_len);
extern __attribute__((import_name("bufferWrite"))) void buffer_write(buffer_t buffer, uint32_t offset, uint8_t *data, uint8_t data_len);

#ifdef __cplusplus
}
#endif

#endif /* WOKWI_API_H */