import os
import sys
import subprocess

from cffi import FFI

can_dir = os.path.dirname(os.path.abspath(__file__))
libdbc_fn = os.path.join(can_dir, "libdbc.so")
subprocess.check_call(["make"], stdout=sys.stderr, cwd=can_dir)

ffi = FFI()
ffi.cdef("""

typedef struct {
  const char* name;
  double value;
} SignalPackValue;

typedef struct {
  uint32_t address;
  const char* name;
  double default_value;
} SignalParseOptions;

typedef struct {
  uint32_t address;
  int check_frequency;
} MessageParseOptions;

typedef struct {
  uint32_t address;
  uint16_t ts;
  const char* name;
  double value;
} SignalValue;


typedef enum {
  DEFAULT,
  HONDA_CHECKSUM,
  HONDA_COUNTER,
  TOYOTA_CHECKSUM,
} SignalType;

typedef struct {
  const char* name;
  int b1, b2, bo;
  bool is_signed;
  double factor, offset;
  SignalType type;
} Signal;

typedef struct {
  const char* name;
  uint32_t address;
  unsigned int size;
  size_t num_sigs;
  const Signal *sigs;
} Msg;

typedef struct {
  const char* name;
  size_t num_msgs;
  const Msg *msgs;
} DBC;


void* can_init(int bus, const char* dbc_name,
              size_t num_message_options, const MessageParseOptions* message_options,
              size_t num_signal_options, const SignalParseOptions* signal_options);

void can_update(void* can, uint64_t sec, bool wait);

size_t can_query(void* can, uint64_t sec, bool *out_can_valid, size_t out_values_size, SignalValue* out_values);

const DBC* dbc_lookup(const char* dbc_name);

void* canpack_init(const char* dbc_name);

uint64_t canpack_pack(void* inst, uint32_t address, size_t num_vals, const SignalPackValue *vals);

""")

libdbc = ffi.dlopen(libdbc_fn)
